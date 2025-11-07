from re import match
from bitflip.substr_expr.sse_const import *

def check_substr_expr(substr_expr: str) -> int | None:
    if substr_expr == "":
        return 1
    elif match(RE_SUBSTR_DIGIT, substr_expr):
        return int(substr_expr)
    elif match(RE_SUBSTR, substr_expr):
        ...
    else:
        return 0