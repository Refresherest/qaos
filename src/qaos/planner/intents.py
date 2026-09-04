"""Provider-neutral executable intent contracts."""

import ast
import re
from dataclasses import dataclass

MAX_SOURCE_BYTES = 65_536
MAX_EXPECTED_OUTPUT_BYTES = 4_096


@dataclass(frozen=True)
class PythonFileIntent:
    """Write and directly verify one deterministic Python source file."""

    relative_path: str
    source: str
    expected_stdout: str
    type: str = "python_file"
    version: int = 1

    def __post_init__(self):
        if self.type != "python_file" or self.version != 1:
            raise ValueError("unsupported executable intent type or version")
        if not isinstance(self.relative_path, str) or not self.relative_path:
            raise ValueError("relative_path must be a non-empty string")
        if not isinstance(self.source, str) or not self.source.strip():
            raise ValueError("source must contain non-blank text")
        if len(self.source.encode("utf-8")) > MAX_SOURCE_BYTES:
            raise ValueError("source exceeds the executable intent limit")
        if not isinstance(self.expected_stdout, str):
            raise TypeError("expected_stdout must be a string")
        if len(self.expected_stdout.encode("utf-8")) > MAX_EXPECTED_OUTPUT_BYTES:
            raise ValueError("expected_stdout exceeds the executable intent limit")
        self._validate_first_fixture()

    def _validate_first_fixture(self):
        """Permit only the approved deterministic print-only first fixture."""
        try:
            tree = ast.parse(self.source, mode="exec")
        except SyntaxError as error:
            raise ValueError("source must be valid Python") from error
        if len(tree.body) != 1 or not isinstance(tree.body[0], ast.Expr):
            raise ValueError("source exceeds the approved print-only fixture")
        call = tree.body[0].value
        if (
            not isinstance(call, ast.Call)
            or not isinstance(call.func, ast.Name)
            or call.func.id != "print"
            or len(call.args) != 1
            or call.keywords
            or not isinstance(call.args[0], ast.Constant)
            or not isinstance(call.args[0].value, str)
            or self.expected_stdout != call.args[0].value + "\n"
        ):
            raise ValueError("source exceeds the approved print-only fixture")

    def to_dict(self):
        return {
            "type": self.type, "version": self.version,
            "relative_path": self.relative_path, "source": self.source,
            "expected_stdout": self.expected_stdout,
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise TypeError("executable intent must be an object")
        allowed = {"type", "version", "relative_path", "source", "expected_stdout"}
        if set(data) != allowed:
            raise ValueError("executable intent fields do not match the contract")
        return cls(**data)


SUPPORTED_TEMPLATE_IDS = frozenset({"text_stats_v1", "text_stats_cli_v1"})


def template_allowlist(values):
    if not isinstance(values, (tuple, list, set, frozenset)):
        raise TypeError("enabled_python_templates must be a collection of template IDs")
    if any(not isinstance(value, str) or value not in SUPPORTED_TEMPLATE_IDS for value in values):
        raise ValueError("unsupported template in allowlist")
    return frozenset(values)


@dataclass(frozen=True)
class PythonTemplateIntent:
    """Select reviewed source by identity; never accept caller-supplied code."""

    relative_path: str
    template_id: str = "text_stats_v1"
    type: str = "python_template"
    version: int = 1

    def __post_init__(self):
        if self.type != "python_template" or type(self.version) is not int or self.version != 1:
            raise ValueError("unsupported template intent type or version")
        if not isinstance(self.template_id, str) or self.template_id not in SUPPORTED_TEMPLATE_IDS:
            raise ValueError("unsupported template ID")
        if not isinstance(self.relative_path, str) or not self.relative_path.strip():
            raise ValueError("relative_path must be a non-blank string")

    def to_dict(self):
        return {"type": self.type, "version": self.version,
                "template_id": self.template_id, "relative_path": self.relative_path}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or set(data) != {"type", "version", "template_id", "relative_path"}:
            raise ValueError("template intent fields do not match the contract")
        return cls(**data)


def intent_from_dict(data):
    if not isinstance(data, dict):
        raise TypeError("executable intent must be an object")
    if data.get("type") == "python_template":
        return PythonTemplateIntent.from_dict(data)
    if data.get("type") == "python_project":
        if type(data.get("version")) is int and data["version"] == 2:
            return PythonProjectIntentV2.from_dict(data)
        return PythonProjectIntent.from_dict(data)
    if data.get("type") != "python_file" or data.get("version") != 1:
        raise ValueError("unsupported executable intent type or version")
    return PythonFileIntent.from_dict(data)


def project_allowlist(values):
    if not isinstance(values, (tuple, list, set, frozenset)):
        raise TypeError("enabled_python_projects must be a collection of project IDs")
    if any(not isinstance(value, str) or value not in ("text_stats_project_v1", "text_stats_project_v2") for value in values):
        raise ValueError("unsupported project template")
    return frozenset(values)


@dataclass(frozen=True)
class PythonProjectIntent:
    relative_directory: str
    template_id: str = "text_stats_project_v1"
    type: str = "python_project"
    version: int = 1

    def __post_init__(self):
        if self.type != "python_project" or type(self.version) is not int or self.version != 1:
            raise ValueError("unsupported project intent version/type")
        if self.template_id != "text_stats_project_v1":
            raise ValueError("unsupported project template")
        name = self.relative_directory
        reserved = {"CON", "PRN", "AUX", "NUL", *(f"COM{i}" for i in range(1, 10)),
                    *(f"LPT{i}" for i in range(1, 10))}
        if (not isinstance(name, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_-]{0,63}", name)
                or name.upper() in reserved):
            raise ValueError("invalid project directory name")

    def to_dict(self):
        return {"type": self.type, "version": self.version, "template_id": self.template_id,
                "relative_directory": self.relative_directory}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or set(data) != {"type", "version", "template_id", "relative_directory"}:
            raise ValueError("project intent fields do not match contract")
        return cls(**data)


METRIC_ORDER = ("characters", "words", "lines")


def normalize_metrics(values):
    if not isinstance(values, (list, tuple)):
        raise TypeError("metrics must be a list or tuple")
    if not values or any(not isinstance(v, str) or v not in METRIC_ORDER for v in values):
        raise ValueError("metrics must select supported values")
    if len(set(values)) != len(values):
        raise ValueError("duplicate metrics are not allowed")
    return tuple(v for v in METRIC_ORDER if v in values)


@dataclass(frozen=True)
class PythonProjectIntentV2:
    relative_directory: str
    metrics: tuple[str, ...]
    template_id: str = "text_stats_project_v2"
    type: str = "python_project"
    version: int = 2

    def __post_init__(self):
        if self.type != "python_project" or type(self.version) is not int or self.version != 2:
            raise ValueError("unsupported project intent version/type")
        if self.template_id != "text_stats_project_v2":
            raise ValueError("unsupported project template")
        PythonProjectIntent(self.relative_directory)  # unchanged directory contract
        object.__setattr__(self, "metrics", normalize_metrics(self.metrics))

    def to_dict(self):
        return {"type": self.type, "version": self.version, "template_id": self.template_id,
                "relative_directory": self.relative_directory, "metrics": list(self.metrics)}

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict) or set(data) != {"type", "version", "template_id", "relative_directory", "metrics"}:
            raise ValueError("project v2 intent fields do not match contract")
        if not isinstance(data["metrics"], list):
            raise TypeError("serialized metrics must be an array")
        return cls(**data)
