import re

_HTML_ESCAPE = (
    ("&", "&amp;"),
    ("<", "&lt;"),
    (">", "&gt;"),
)

_MD_PATTERNS = [
    (re.compile(r"\*\*(.*?)\*\*"), r"\1"),     # **bold**
    (re.compile(r"__(.*?)__"), r"\1"),         # __bold__
    (re.compile(r"_(.*?)_"), r"\1"),           # _italic_
    (re.compile(r"\*(.*?)\*"), r"\1"),         # *italic*
    (re.compile(r"`{1,3}(.*?)`{1,3}", re.S), r"\1"),  # `code` or ```block```
    (re.compile(r"^#+\s+", re.M), ""),         # # headers
]

def escape_html(text: str) -> str:
    out = text
    for src, dst in _HTML_ESCAPE:
        out = out.replace(src, dst)
    return out

def strip_markdown(text: str) -> str:
    out = text
    for pat, repl in _MD_PATTERNS:
        out = pat.sub(repl, out)
    return out

def normalize_for_telegram(text: str) -> str:
    # Plain text for HTML parse mode: no markdown, escaped HTML
    return escape_html(strip_markdown(text)).strip()