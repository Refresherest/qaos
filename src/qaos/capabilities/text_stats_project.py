"""Repository-owned four-file project; no caller-selected members."""
from types import MappingProxyType
from .text_stats_template import SOURCE as STATS_SOURCE
from .text_stats_cli_template import SOURCE as CLI_SOURCE

MEMBERS = MappingProxyType({
    "stats.py": STATS_SOURCE.split('if __name__ == "__main__":', 1)[0],
    "app.py": "from stats import text_stats, _self_test\n\n" + "def main(argv):" + CLI_SOURCE.split("def main(argv):", 1)[1],
    "test_stats.py": '''import io
import unittest
from stats import text_stats
import app


class Acceptance(unittest.TestCase):
    def test_counts(self):
        self.assertIs(app.text_stats, text_stats)
        self.assertEqual(text_stats(""), {"characters": 0, "words": 0, "lines": 0})
        self.assertEqual(text_stats("one\\ntwo"), {"characters": 7, "words": 2, "lines": 2})
        self.assertEqual(text_stats("猫 café"), {"characters": 6, "words": 2, "lines": 1})
        with self.assertRaises(TypeError):
            text_stats(None)


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(Acceptance)
    result = unittest.TextTestRunner(stream=io.StringIO()).run(suite)
    if not result.wasSuccessful():
        raise SystemExit(1)
    print("QAOS project tests PASS")
''',
    "README.md": "# text_stats_project_v1\n\nRun: python app.py --text \"hello world\"\n"
                 "Run tests: python test_stats.py\nNo arguments runs CLI self-tests.\n"
                 "Counts are Unicode code points, whitespace tokens and splitlines entries.\n"
                 "Maximum input: 4096 code points. Use --text=VALUE for leading dashes.\n"
                 "Use non-sensitive text only: arguments can appear in process lists/history.\n",
})
