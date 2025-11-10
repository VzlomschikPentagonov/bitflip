from bitflip.substr_expr.sse_const import *
from bitflip.substr_expr.sse_classes import *
from bitflip.func.b_misc import print_error
from re import match

def parse_sse_arg(arg: str,
                  sub_strs: dict[str: str]) -> list[Key]:
    match arg[START]:
        case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9':
            ...
        case '-':
            ...
        case '^':
            ...
        case '/':
            ...
        case '\\':
            ...
        case '0':
            ...
        case _:
            ...
    return [Key()]

def parse_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> tuple[int, list[Key]]:
    split_expr: tuple = substr_expr.partition('|')
    key_list: list[Key] = []
    if split_expr[NUM_ARGS] == "":
        num_args: int = 1
    elif(match(RE_SUBSTR_D1, split_expr[NUM_ARGS])
       and match(RE_SUBSTR_D2, split_expr[NUM_ARGS])):
        num_args: int = int(split_expr[NUM_ARGS])
    split_args: list[int] = split_expr[SUBSTR_ARGS].split(',')
    for arg in split_args:
        arg = param.replace(' ', "")
        key_list = parse_sse_arg(arg, sub_strs)
    return num_args, [Key()]

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
