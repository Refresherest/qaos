"""Explicitly authorized trusted-template execution using existing file lifecycle."""

from qaos.planner.intents import PythonTemplateIntent, template_allowlist
from .python_file import PythonFileCapability
from .text_stats_template import SOURCE, SUCCESS_MARKER
from . import text_stats_cli_template, text_stats_cli_verifier


class PythonTemplateCapability(PythonFileCapability):
    name = "python_template"

    def __init__(self, workspace, *, enabled_python_templates=()):
        self._enabled_templates = template_allowlist(enabled_python_templates)
        super().__init__(workspace)

    def _execution_spec(self, intent):
        if type(intent) is not PythonTemplateIntent:
            raise TypeError("python_template capability requires PythonTemplateIntent")
        PythonTemplateIntent.from_dict(intent.to_dict())
        if intent.template_id not in self._enabled_templates:
            raise ValueError("template is not enabled")
        cli = intent.template_id == "text_stats_cli_v1"
        return (text_stats_cli_template.SOURCE if cli else SOURCE), (
            text_stats_cli_template.SUCCESS_MARKER if cli else SUCCESS_MARKER), {
            "template_id": intent.template_id, "template_version": 1,
            "verifier": "trusted_cli_cases_v1" if cli else "trusted_template_self_test_v1",
        }

    def _verify_source(self, target, source):
        if target.read_bytes() != source.encode("utf-8"):
            raise RuntimeError("generated template differs from reviewed source")

    def _verify_behavior(self, target, intent, evidence):
        if intent.template_id == "text_stats_cli_v1":
            text_stats_cli_verifier.verify(target, self._timeout, evidence)
