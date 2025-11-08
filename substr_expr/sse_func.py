from bitflip.substr_expr.sse_const import *
from bitflip.substr_expr.sse_classes import *
from re import match

def parse_substr_expr(substr_expr: str) -> list[Key]:
    a: Key = Key(substr_expr)
    return [a]

def check_substr_expr(substr_expr: str) -> int | list[Key]:
    if substr_expr == "":
        return 1
    elif (match(RE_SUBSTR_D1, substr_expr)
          and match(RE_SUBSTR_D2, substr_expr)):
        return int(substr_expr)
    elif match(RE_SUBSTR, substr_expr):
        return parse_substr_expr(substr_expr)
    else:
        return 0