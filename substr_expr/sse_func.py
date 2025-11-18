from bitflip.substr_expr.sse_const import *
from bitflip.substr_expr.sse_classes import *
from bitflip.func.b_misc import print_error
from re import match, split

def pick_keys(key_list: list[Key],
              sub_strs: dict[str: str],
              lengths: list[int],
              starts_with: str = STR_DEFAULT,
              ends_with: str = STR_DEFAULT,
              keyword: str = STR_DEFAULT,
              entries_: int = ENTRIES_DEFAULT) -> None:
    if entries_ == 0:
        return None
    for key in sub_strs.keys():
        if len(key) in lengths:
            key_list.append(Key(key, entries = entries_))
        elif match(f"^{starts_with}", key):
            key_list.append(Key(key, entries = entries_))
        elif match(f".*{ends_with}$", key):
            key_list.append(Key(key, entries = entries_))
        elif key == keyword:
            key_list.append(Key(key, entries = entries_))

def parse_digit_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    range_: list[int] = []
    entries: int = ENTRIES_DEFAULT
    if arg == "":
        pick_keys(key_list, sub_strs, [1])
        return key_list
    if match(RE_DIGIT_ARG, arg):
        split_arg: list[str] = split(RE_SPLIT_DIGIT_ARG, arg)
        if '^' in arg:
            if split_arg[ENTRIES_NUM] != "":
                entries = int(arg[ENTRIES_NUM])
            else:
                entries = 0
        if split_arg[START] == "":
            if split_arg[END] == "":
                split_arg[END] = "0"
            range_ = [*range(1, int(split_arg[END]) + 1)]
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
    pick_keys(key_list, sub_strs, lengths = range_, entries_ = entries)
    return key_list

def parse_startsw_arg(arg: str,
                      sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    entries: int = ENTRIES_DEFAULT
    split_arg: list[str] = arg.split('^')
    print(split_arg)
    if len(split_arg) > 1:
        if split_arg[ENTRIES_NUM] != "":
            entries = int(arg[ENTRIES_NUM])
        else:
            entries = 0
    pick_keys(key_list, sub_strs, [], starts_with = arg.lstrip('/'),
              entries_ = entries, )
    return key_list

def parse_endsw_arg(arg: str,
                    sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    entries: int = ENTRIES_DEFAULT
    split_arg: list[str] = arg.split('^')
    if len(split_arg) > 1:
        if split_arg[ENTRIES_NUM] != "":
            entries = int(arg[ENTRIES_NUM])
        else:
            entries = 0
    pick_keys(key_list, sub_strs, [], starts_with = arg.lstrip('\\'),
              entries_ = entries)
    return key_list

def parse_keyword_arg(arg: str,
                      sub_strs: dict[str: str]) -> list[Key]:
    key_list: list[Key] = []
    entries: int = ENTRIES_DEFAULT
    split_arg: list[str] = arg.split('^')
    if arg[START] == '0':
        arg = arg.replace('0', "", 1)
    if split_arg[ENTRIES_NUM] != "":
        entries = int(arg[ENTRIES_NUM])
    pick_keys(key_list, sub_strs, [], keyword = arg, entries_ = entries)
    return key_list

def parse_sse_arg(arg: str,
                  sub_strs: dict[str: str]) -> list[Key]:
    if arg == "":
        return parse_digit_arg(arg, sub_strs)
    match arg[START]:
        case '1' | '2' | '3' | '4' | '5' | '6' | '7' | '8' | '9' | '-' | '^':
            key_list: list[Key]  = parse_digit_arg(arg, sub_strs)
        case '/':
            key_list: list[Key]  = parse_startsw_arg(arg, sub_strs)
        case '\\':
            key_list: list[Key]  = parse_endsw_arg(arg, sub_strs)
        case '0' | _:
            key_list: list[Key]  = parse_keyword_arg(arg, sub_strs)
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
            key_list: list[Key] = parse_sse_arg(arg, sub_strs)
        else:
            parse_digit_arg(arg, sub_strs)
    return num_args, key_list

def check_substr_expr(substr_expr: str,
                      sub_strs: dict[str: str]) -> int | tuple[int, list[Key]]:
    if substr_expr == "":
        return 1
    elif(match(RE_SUBSTR_D1, substr_expr)
         and match(RE_SUBSTR_D2, substr_expr)):
        return int(substr_expr)
    elif match(RE_SUBSTR, substr_expr):
        return parse_substr_expr(substr_expr, sub_strs)
    else:
        print_error("Invalid sub string expression")
