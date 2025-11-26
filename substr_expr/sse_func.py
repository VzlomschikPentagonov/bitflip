from bitflip.substr_expr.sse_const import *
from bitflip.func.b_misc import print_error
from re import match, split

def pick_keys(key_list: list[str],
              sub_strs: dict[str: str],
              lengths: list[int],
              starts_with: str = STR_DEFAULT,
              ends_with: str = STR_DEFAULT,
              keyword: str = STR_DEFAULT,
              all_len: bool = False,
              exclude: bool = False) -> None:
    if all_len:
        for key in sub_strs.keys():
            key_list.append(key)
        return None
    if exclude:
        for key in sub_strs.keys():
            if(not match(f"^{starts_with}", key) and
            starts_with != STR_DEFAULT):
                key_list.append(key)
            elif(not match(f".*{ends_with}$", key) and
            ends_with != STR_DEFAULT):
                key_list.append(key)
            elif key != keyword and keyword != STR_DEFAULT:
                key_list.append(key)
        return None
    for key in sub_strs.keys():
        if len(key) in lengths:
            key_list.append(key)
        elif match(f"^{starts_with}", key):
            key_list.append(key)
        elif match(f".*{ends_with}$", key):
            key_list.append(key)
        elif key == keyword:
            key_list.append(key)

def parse_digit_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[str]:
    key_list: list[str] = []
    range_: list[int] = []
    if arg == "":
        pick_keys(key_list, sub_strs, [LENGTH_DEFAULT])
        return key_list
    if match(RE_DIGIT_ARG, arg):
        split_arg: list[str] = split(RE_SPLIT_DIGIT_ARG, arg)
        if split_arg[START] == "":
            if split_arg[END] != "":
                range_ = [*range(1, int(split_arg[END]) + 1)]
            else:
                pick_keys(key_list, sub_strs, [], all_len = True)
                return key_list
            if '+' in arg:
                range_ = [*range(1, int(split_arg[END]) + 1,
                                 int(split_arg[STEP]))]
        else:
            range_ = [int(split_arg[START])]
            if '-' in arg:
                range_ = [*range(int(split_arg[START]),
                                 int(split_arg[END]) + 1)]
                if '+' in arg:
                    range_ = [*range(int(split_arg[START]),
                                     int(split_arg[END]) + 1,
                                     int(split_arg[STEP]))]
        if '^' in arg:
            range_inv: list[int] = []
            for length in [len(key) for key in sub_strs.keys()]:
                if length not in range_:
                    range_inv.append(length)
            pick_keys(key_list, sub_strs, range_inv)
            return key_list
    pick_keys(key_list, sub_strs, range_)
    return key_list

def parse_startsw_arg(arg: str,
                      sub_strs: dict[str: str]) -> list[str]:
    key_list: list[str] = []
    split_arg: list[str] = arg.split('^')
    if '^' in arg:
        pick_keys(key_list, sub_strs, [],
              starts_with = split_arg[START].lstrip('/'), exclude = True)
        return key_list
    pick_keys(key_list, sub_strs, [],
              starts_with = split_arg[START].lstrip('/'))
    return key_list

def parse_endsw_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[str]:
    key_list: list[str] = []
    split_arg: list[str] = arg.split('^')
    if '^' in arg:
        pick_keys(key_list, sub_strs, [],
              ends_with = split_arg[START].lstrip('\\'), exclude = True)
        return key_list
    pick_keys(key_list, sub_strs, [],
              ends_with = split_arg[START].lstrip('\\'))
    return key_list

def parse_keyword_arg(arg: str,
                      sub_strs: dict[str: str]) -> list[str]:
    key_list: list[str] = []
    if arg[START] == '0':
        arg = arg.replace('0', "", 1)
    split_arg: list[str] = arg.split('^')
    if '^' in arg:
        pick_keys(key_list, sub_strs, [],
              keyword = split_arg[START], exclude = True)
        return key_list
    pick_keys(key_list, sub_strs, [], keyword = split_arg[START])
    return key_list

def parse_sse_arg(arg: str,
                  sub_strs: dict[str: str]) -> list[str]:
    if arg == "":
        return parse_digit_arg(arg, sub_strs)
    match arg[START]:
        case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '-' | '^':
            key_list: list[str] = parse_digit_arg(arg, sub_strs)
        case '/':
            key_list: list[str] = parse_startsw_arg(arg, sub_strs)
        case '\\':
            key_list: list[str] = parse_endsw_arg(arg, sub_strs)
        case '0' | _:
            key_list: list[str] = parse_keyword_arg(arg, sub_strs)
    return key_list

def parse_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> tuple[int, list[str]]:
    split_expr: tuple = substr_expr.partition(':')
    key_list: list[list[str]] = []
    num_args: int = 1
    if(match(RE_SUBSTR_D1, split_expr[NUM_ARGS])
       and match(RE_SUBSTR_D2, split_expr[NUM_ARGS])):
        num_args: int = int(split_expr[NUM_ARGS])
    split_args: list[str] = split_expr[SUBSTR_ARGS].split(',')
    for arg in split_args:
        arg = arg.replace(' ', "")
        if arg != "":
            key_list.append(parse_sse_arg(arg, sub_strs))
        else:
            key_list.append(parse_digit_arg(arg, sub_strs))
    return (num_args, list({string: None for string in
                            [key for arg_keys in key_list
                                 for key in arg_keys]}.keys()))

def check_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> int | tuple[int, list[str]]:
    if substr_expr == "":
        return 1
    elif(match(RE_SUBSTR_D1, substr_expr)
         and match(RE_SUBSTR_D2, substr_expr)):
        return int(substr_expr)
    elif match(RE_SUBSTR, substr_expr):
        return parse_substr_expr(substr_expr, sub_strs)
    else:
        print_error("Invalid sub string expression")
