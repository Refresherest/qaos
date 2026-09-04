"""Read-only controlled-language preview, never a build authorization."""
import json
import sys

from qaos.planner.controlled_brief import interpret


USAGE = ('Usage: python -m qaos.main preview-project --directory <name> '
         '--brief "count words and lines"')
DIAGNOSTIC = (USAGE + "\nGrammar: count METRIC (and METRIC)*; unique characters, words, "
              "lines; 1-256 ASCII letters/spaces only.")


def execute(args):
    try:
        if len(args) != 4:
            raise ValueError("invalid option count")
        values = {}
        for key, value in zip(args[::2], args[1::2]):
            if (key not in ("--directory", "--brief") or key in values
                    or not isinstance(value, str) or not value.strip() or value.startswith("--")):
                raise ValueError("invalid option")
            values[key] = value
        intent = interpret(values["--directory"], values["--brief"])
        payload = json.dumps({"status": "preview", "grammar_version": 1,
                              "intent": intent.to_dict()})
    except (TypeError, ValueError):
        print(DIAGNOSTIC, file=sys.stderr)
        return 2
    except Exception as exc:
        print(f"Project preview failed ({type(exc).__name__}).", file=sys.stderr)
        return 1
    print(payload)
    return 0
