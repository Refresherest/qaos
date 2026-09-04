"""Pure grammar-v1 interpretation; returning an intent grants no authority."""
import re

from .intents import PythonProjectIntentV2


def interpret(directory, brief):
    if not isinstance(brief, str):
        raise TypeError("brief must be a string")
    if not 1 <= len(brief) <= 256 or re.fullmatch(r"[A-Za-z ]+", brief) is None:
        raise ValueError("unsupported brief")
    words = brief.lower().split()
    if (len(words) not in (2, 4, 6) or words[0] != "count"
            or any(word != "and" for word in words[2::2])):
        raise ValueError("unsupported brief grammar")
    return PythonProjectIntentV2(directory, words[1::2])
