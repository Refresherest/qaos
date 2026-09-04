"""Reviewed source for the immutable text_stats_v1 workload."""

SUCCESS_MARKER = "QAOS text_stats_v1 PASS\n"

# Literal expected values are independent of the generated implementation.
SOURCE = '''"""Deterministic text statistics; no I/O when imported."""


def text_stats(text):
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    return {"characters": len(text), "words": len(text.split()),
            "lines": len(text.splitlines())}


def _self_test():
    cases = (
        ("", {"characters": 0, "words": 0, "lines": 0}),
        ("hello world", {"characters": 11, "words": 2, "lines": 1}),
        (" a\\t b  ", {"characters": 7, "words": 2, "lines": 1}),
        ("one\\ntwo", {"characters": 7, "words": 2, "lines": 2}),
        ("a\\r\\nb\\r\\n", {"characters": 6, "words": 2, "lines": 2}),
        ("end\\n", {"characters": 4, "words": 1, "lines": 1}),
        ("猫 café", {"characters": 6, "words": 2, "lines": 1}),
        ("e\\u0301", {"characters": 2, "words": 1, "lines": 1}),
    )
    for text, expected in cases:
        if text_stats(text) != expected:
            raise RuntimeError("text statistics acceptance failed")
    for value in (None, 12, []):
        try:
            text_stats(value)
        except TypeError:
            pass
        else:
            raise RuntimeError("non-string acceptance failed")


if __name__ == "__main__":
    _self_test()
    print("QAOS text_stats_v1 PASS")
'''
