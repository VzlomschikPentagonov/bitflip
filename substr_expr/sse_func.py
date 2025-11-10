from bitflip.substr_expr.sse_const import *
from bitflip.substr_expr.sse_classes import *
from bitflip.func.b_misc import print_error
from re import match

def parse_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> tuple[int, list[Key]]:
    split_expr: tuple = substr_expr.partition('|')
    if split_expr[2] == "":
        num_args: int = 1
    elif(match(RE_SUBSTR_D1, split_expr[2])
       and match(RE_SUBSTR_D2, split_expr[2])):
        num_args: int = int(split_expr[2])
    ...
    return num_args, Key()

def check_substr_expr(substr_expr: str) -> int | tuple[int, list[Key]]:
    if substr_expr == "":
        return 1
    elif(match(RE_SUBSTR_D1, substr_expr)
         and match(RE_SUBSTR_D2, substr_expr)):
        return int(substr_expr)
    elif match(RE_SUBSTR, substr_expr):
        return parse_substr_expr(substr_expr)
    else:
        print_error("Invalid sub string expression")
