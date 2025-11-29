from typing import TextIO
from re import match, split
from os import getcwd, chdir
from bitflip.func.b_constants import *
from bitflip.func.b_misc import print_error

def return_to_main_dir():
    curr_dir: list[str] = getcwd().split('\\')
    dir_level: int = 1
    for dir_ in reversed(curr_dir):
        match dir_:
            case "bitflip":
                chdir('.' * dir_level + '/')
                break
            case _:
                dir_level += 1

def get_code(input_file_data: list[str]) -> str:
    program_str: str = "".join(input_file_data[STRIP_1ST_LINE:])
    return program_str

def read_input_file() -> tuple[int, str, int]:
    return_to_main_dir()
    input_file: TextIO = open("input.txt")
    input_file_data: list[str] = input_file.readlines()
    config_str: list[str] = input_file_data[0].split(',')
    return (int(config_str[NUM_STATES]),
            get_code(input_file_data),
            int(config_str[TAPE_LEN]))

def count_brackets(line: str) -> int:
    br_sum: int = 0
    max_nest_lvl: int = 0
    for char in line:
        match char:
            case '{':
                br_sum += 1
                if br_sum > max_nest_lvl:
                    max_nest_lvl = br_sum
            case '}':
                br_sum -= 1
        if br_sum < 0:
            return -1
    if br_sum == 0:
        return max_nest_lvl

def parse_substr_line(line: str) -> tuple[str, str]:
    split_line: list[str] = line.split(':')
    key: str = split_line[KEY]
    value: str = split_line[VALUE]
    return key, value.rstrip('\n')

def parse_substr_w_expr(sub_strs: dict[str, str]) -> str:

    return ""

def parse_bracket_str(string: str,
                      sub_strs: dict[str, str]) -> str:
    value: str = ""
    repeat: str = ""
    if match(RE_REPSTR, string):
        for char in string:
            if char in CHAR_SET:
                value += char
            if char.isdigit():
                repeat += char
        return value * int(repeat)
    elif match(RE_DEFINE, string):
        for key in sub_strs.keys():
            if string == key:
                return sub_strs[key]
        return parse_substr_w_expr(sub_strs)

def remove_brackets(value: str,
                    sub_strs: dict[str, str],
                    nest_lvl: int) -> str:
    br_sum: int = 0
    string: str = ""
    value_new: str = ""
    for char in value:
        match char:
            case '{':
                br_sum += 1
                if br_sum != nest_lvl:
                    value_new += char
                continue
            case '}':
                br_sum -= 1
                if br_sum == nest_lvl - 1:
                    value_new += parse_bracket_str(string, sub_strs)
                    string = ""
                    continue
        if br_sum == nest_lvl:
            string += char
        else:
            value_new += char
    return value_new

def read_include_file() -> dict[str, str]:
    return_to_main_dir()
    input_file: TextIO = open("include.txt")
    input_file_data: list[str] = input_file.readlines()
    sub_strs: dict[str, str] = {}
    for line in input_file_data:
        line_nc: str = line.partition('#')[SUBSTR].replace(' ', "")
        if match(RE_DEFFILE_BR, line):
            key, value = parse_substr_line(line_nc)
            if '{' in key or '}' in key:
                if count_brackets(key) != 1:
                    print_error("Invalid sub string key")
                for token in split(r"/{%s/}" % RE_SUBSTR_CHARSET, key):
                    if not token.isidentifier() and token != "":
                        print_error("Invalid sub string key")
            else:
                if not key.isidentifier():
                    print_error("Invalid sub string key")
                max_nest_lvl: int = count_brackets(value)
                for nest_lvl in range(max_nest_lvl, 0, -1):
                    value = remove_brackets(value, sub_strs, nest_lvl)
            sub_strs[key] = value
    return sub_strs

def compile_program(program_str: str,
                    sub_strs: dict[str: str]) -> str:
    new_str: str = ""
    max_nest_lvl: int = count_brackets(program_str)
    for nest_lvl in range(max_nest_lvl, 0, -1):
        program_str = remove_brackets(program_str, sub_strs, nest_lvl)
    for char in program_str:
        match char:
            case '!' | '<' | '>' | '[' | ']':
                new_str += char
    return new_str
