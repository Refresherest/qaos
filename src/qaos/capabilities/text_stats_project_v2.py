"""Render only validated metric enums into reviewed project v2 source."""
from types import MappingProxyType
from qaos.planner.intents import normalize_metrics
from .text_stats_project import MEMBERS


def render(metrics):
    metrics = normalize_metrics(metrics)
    members = dict(MEMBERS)
    members["app.py"] = ("SELECTED_METRICS = " + repr(metrics) + "\n" + members["app.py"]).replace(
        "json.dumps(text_stats(text), sort_keys=True)",
        "json.dumps({key: text_stats(text)[key] for key in SELECTED_METRICS}, sort_keys=True)",
    )
    expected = {key: value for key, value in (("characters", 7), ("words", 2), ("lines", 1)) if key in metrics}
    test = '''    def test_selected_output(self):
        import contextlib
        import json
        captured = io.StringIO()
        with contextlib.redirect_stdout(captured):
            self.assertEqual(app.main(["--text", "one two"]), 0)
        self.assertEqual(json.loads(captured.getvalue()), EXPECTED_LITERAL)

'''.replace("EXPECTED_LITERAL", repr(expected))
    members["test_stats.py"] = members["test_stats.py"].replace(
        'if __name__ == "__main__":', test + '\nif __name__ == "__main__":')
    members["README.md"] = members["README.md"].replace("text_stats_project_v1", "text_stats_project_v2")
    members["README.md"] += "Selected CLI metrics: " + ", ".join(metrics) + ".\n"
    return MappingProxyType(members)
