from bitflip.substr_expr.sse_const import *
from bitflip.func.b_misc import print_error
from re import match, split

def pick_keys(key_list: list[str],
              sub_strs: dict[str: str],
              lengths: list[int],
              all_len: bool = False,
              exclude: bool = False,
              **kwargs: str) -> None:
    if all_len:
        for key in sub_strs.keys():
            key_list.append(key)
        return None
    match_str: str = STR_DEFAULT
    if kwargs["starts_w"] != STR_DEFAULT:
        match_str = f"^{kwargs['starts_w']}"
    elif kwargs["ends_w"] != STR_DEFAULT:
        match_str = f".*{kwargs['ends_w']}$"
    elif kwargs["keyword"] != STR_DEFAULT:
        match_str = f"^{kwargs['keyword']}$"
    for key in sub_strs.keys():
        if len(key) in lengths:
            key_list.append(key)
        elif match(match_str, key):
            if exclude:
                continue
            key_list.append(key)
        if exclude:
            key_list.append(key)

def parse_digit_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[str]:
    key_list: list[str] = []
    range_: list[int] = []
    if arg == "":
        pick_keys(key_list, sub_strs, [LENGTH_DEFAULT], ends_w = STR_DEFAULT,
                  starts_w = STR_DEFAULT, keyword = STR_DEFAULT)
        return key_list
    if match(RE_DIGIT_ARG, arg):
        split_arg: list[str] = split(RE_SPLIT_DIGIT_ARG, arg)
        if '~' in arg:
            split_arg = split_arg[1:]
        if split_arg[START] == "":
            if split_arg[END] != "":
                range_ = [*range(1, int(split_arg[END]) + 1)]
            else:
                pick_keys(key_list, sub_strs, [], all_len = True,
                ends_w = STR_DEFAULT, starts_w = STR_DEFAULT,
                keyword = STR_DEFAULT)
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
        if '~' in arg:
            range_inv: list[int] = []
            for length in [len(key) for key in sub_strs.keys()]:
                if length not in range_:
                    range_inv.append(length)
            pick_keys(key_list, sub_strs, range_inv, ends_w = STR_DEFAULT,
                      starts_w = STR_DEFAULT, keyword = STR_DEFAULT)
            return key_list
    else:
        print_error("Invalid sub string expression")
    pick_keys(key_list, sub_strs, range_, ends_w = STR_DEFAULT,
              starts_w = STR_DEFAULT, keyword = STR_DEFAULT)
    return key_list

def parse_str_arg(arg: str,
                  sub_strs: dict[str: str],
                  strip: str = "",
                  **kwargs: str | bool) -> list[str]:
    if not match(RE_KEYWORD_ARG, arg):
        print_error("Invalid sub string expression")
    key_list: list[kwargs["strip"]] = []
    exclude: bool = False
    arg = arg.lstrip(strip)
    if '~' in arg:
        print(arg)
        arg = arg.rstrip('~')
        exclude = True
    if arg[0] == '0' and kwargs["keyword"] == True:
        arg = arg.replace('0', "", 1)
    if kwargs["starts_w"]:
        pick_keys(key_list, sub_strs, [], starts_w = arg,
                  ends_w = STR_DEFAULT, keyword = STR_DEFAULT)
    elif kwargs["ends_w"]:
        pick_keys(key_list, sub_strs, [], ends_w = arg,
                  starts_w = STR_DEFAULT, keyword = STR_DEFAULT)
    elif kwargs["keyword"]:
        pick_keys(key_list, sub_strs, [], keyword = arg,
                  starts_w = STR_DEFAULT, ends_w = STR_DEFAULT)
    return key_list

def parse_sse_arg(arg: str,
                  sub_strs: dict[str: str]) -> list[str]:
    if arg == "":
        return parse_digit_arg(arg, sub_strs)
    match arg[START]:
        case ('1' | '2' | '3' | '4' | '5' | '6' |
              '7' | '8' | '9' | '-' | '~'):
            key_list: list[str] = parse_digit_arg(arg, sub_strs)
        case '/' | '~':
            key_list: list[str] = parse_str_arg(arg, sub_strs,
                                                strip = '/', starts_w = True,
                                                ends_w = False,
                                                keyword = False)
        case '\\' | '~':
            key_list: list[str] = parse_str_arg(arg, sub_strs,
                                                strip = '\\', ends_w = True,
                                                starts_w = False,
                                                keyword = False)
        case '0' | '~' | _:
            key_list: list[str] = parse_str_arg(arg, sub_strs, keyword = True,
                                                starts_w = False,
                                                ends_w = False)
    return key_list

def parse_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> tuple[int, list[str]]:
    split_expr: tuple = substr_expr.partition(';')
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
