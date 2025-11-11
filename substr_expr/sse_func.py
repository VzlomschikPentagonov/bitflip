from bitflip.substr_expr.sse_const import *
from bitflip.substr_expr.sse_classes import *
from bitflip.func.b_misc import print_error
from re import match, strip

def pick_keys(key_list: list[Key],
              sub_strs: dict[str: str],
              length: int = LENGTH_DEFAULT,
              starts_with: str = "%",
              ends_with: str = "%",
              keyword: str = "%",
              entries_: int = -1) -> None:
    for key in sub_strs.keys():
        if len(key) == length:
            key_list.append(Key(key, entries = entries_))
        elif match(f"^{starts_with}", key):
            key_list.append(Key(key, entries = entries_))
        elif match(f".*{ends_with}$", key):
            key_list.append(Key(key, entries = entries_))
        elif key = keyword:
            key_list.append(Key(key, entries = entries_))
        

def parse_digit_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    if arg == "":
        pick_keys(key_list, sub_strs)
    if match(RE_DIGIT_ARG, arg):
        split_arg: list[str] = split(RE_SPLIT_DIGIT_ARG)
        if split_arg[PICK_LENGTH_N] == "":
            if len(key) == 1:
                key_list.append(Key(key, entries = -1))
    return key_list

def parse_startsw_arg(arg: str,
                      sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    return key_list

def parse_endsw_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    return key_list

def parse_keyword_arg(arg: str,
                      sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    return key_list

def parse_sse_arg(arg: str,
                  sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    match arg[START]:
        case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '-' | '^':
            key_list = parse_digit_arg(arg, sub_strs)
        case '/':
            key_list = parse_startsw_arg(arg, sub_strs)
        case '\\':
            key_list = parse_endsw_arg(arg, sub_strs)
        case '0' | _:
            key_list = parse_keyword_arg(arg, sub_strs)
    return key_list

def parse_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> tuple[int, list[Key]]:
    split_expr: tuple = substr_expr.partition('|')
    key_list: list[Key] = []
    num_args: int = 1
    if(match(RE_SUBSTR_D1, split_expr[NUM_ARGS])
       and match(RE_SUBSTR_D2, split_expr[NUM_ARGS])):
        num_args: int = int(split_expr[NUM_ARGS])
    split_args: list[str] = split_expr[SUBSTR_ARGS].split(',')
    for arg in split_args:
        arg = arg.replace(' ', "")
        if arg != "":
            key_list = parse_sse_arg(arg, sub_strs)
        else:
            parse_digit_arg(arg, sub_strs)
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
