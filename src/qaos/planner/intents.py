"""Provider-neutral executable intent contracts."""

import ast
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


def intent_from_dict(data):
    if not isinstance(data, dict):
        raise TypeError("executable intent must be an object")
    if data.get("type") != "python_file" or data.get("version") != 1:
        raise ValueError("unsupported executable intent type or version")
    return PythonFileIntent.from_dict(data)
