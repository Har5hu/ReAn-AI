import re


def normalize_whitespace(text: str) -> str:
    """Collapse runs of whitespace and trim the text's outer edges.

    This treats spaces, tabs, and line breaks consistently, so pasted job
    descriptions are tokenized and scored from one predictable representation.
    """
    return re.sub(r"\s+", " ", text or "").strip()
