"""Reviewed single-file CLI source; the original template remains unchanged."""

from .text_stats_template import SOURCE as MODULE_SOURCE

SUCCESS_MARKER = "QAOS text_stats_cli_v1 PASS\n"
SOURCE = MODULE_SOURCE.split('if __name__ == "__main__":', 1)[0] + '''def main(argv):
    import json
    import sys

    if not argv:
        _self_test()
        print("QAOS text_stats_cli_v1 PASS")
        return 0
    text = None
    if len(argv) == 2 and argv[0] == "--text" and not argv[1].startswith("-"):
        text = argv[1]
    elif len(argv) == 1 and argv[0].startswith("--text="):
        text = argv[0][7:]
    if text is None or len(text) > 4096:
        print("Invalid text arguments", file=sys.stderr)
        return 2
    print(json.dumps(text_stats(text), sort_keys=True))
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main(sys.argv[1:]))
'''
