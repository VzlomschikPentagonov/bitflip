from typing import TextIO
from re import match
from bitflip.func.b_constants import *

def get_code(input_file_data: list[str]) -> str:
    program_str: str = ""
    for line in input_file_data[STRIP_1ST_LINE:]:
        program_str += line
    return program_str

def read_input_file() -> tuple[int, str]:
    input_file: TextIO = open("input.txt")
    input_file_data: list[str] = input_file.readlines()
    return (int(input_file_data[NUM_STATES]),
            get_code(input_file_data))

def count_brackets(line: str) -> int:
    br_sum: int = 0
    nest: int = 0
    for char in line:
        match char:
            case '{':
                br_sum += 1
                if br_sum > nest:
                    nest = br_sum
            case '}':
                br_sum -= 1
        if br_sum < 0:
            return -1
    if br_sum == 0:
        return nest
    return -1

def parse_define_line(line: str) -> tuple[str, str]:
    define: str = ""
    code: str = ""
    char: int = 0
    while line[char] != ':':
        define += line[char]
        char += 1
    for c_char in range(char + 2, len(line)):
        code += line[c_char]
    if code[-1] == '\n':
        code = code[:-1]
    return define, code

def parse_bracket_string(string: str,
                         defines: dict[str, str]) -> str:
    if match(RM_REPSTR, string):
        for char in string:
            if s_char in CHAR_SET:
                code += char
            if s_char.isdigit():
                repeat += char
        return code * int(repeat)
    elif match(RM_DEFINE, string):
        for define in defines.keys():
            if string == define:
                return defines[define]

def remove_brackets(code: str,
                    defines: dict[str, str],
                    nest_lvl: int) -> str:
    br_sum: int = 0
    string: str = ""
    new_code: str = ""
    for char in code:
        match char:
            case '{':
                br_sum += 1
                continue
            case '}':
                br_sum -= 1
                if br_sum == nest_lvl - 1:
                    new_code += parse_bracket_string(string, defines)
                    continue
        if br_sum == nest_lvl:
            string += char
        else:
            new_code += char
    return new_code

def read_defines_file() -> dict[str, str]:
    input_file: TextIO = open("defines.txt")
    max_nest_lvl: int = count_brackets(program_str)
    input_file_data: list[str] = input_file.readlines()
    defines: dict[str, str] = {}
    for line in input_file_data:
        if match(RM_DEFFILE, line):
            define, code = parse_define_line(line)
            defines[define] = code
        elif match(RM_DEFFILE_BR, line):
            define, code = parse_define_line(line)
            for nest_lvl in range(max_nest_lvl, 0, -1):
                code = remove_brackets(code, defines, nest_lvl)
            defines[define] = code
    return defines

def get_br_string(program_str: str,
                  pos: int,
                  defines: dict[str, str]) -> tuple[int, str]:
    sub_string: str = ""
    i: int = pos + 1
    while program_str[i] != '}':
        sub_string += program_str[i]
        i += 1
    return parse_bracket_string(string, defines)

def compile_program(program_str: str) -> str:
    new_str: str = ""
    # i: int = 0
    defines: dict[str, str] = read_defines_file()
    max_nest_lvl: int = count_brackets(program_str)
    for nest_lvl in range(max_nest_lvl, 0, -1):
        program_str = remove_brackets(program_str, defines, nest_lvl)
    # while i < len(program_str):
        # match program_str[i]:
        #     case '!' | '<' | '>' | '[' | ']':
        #         new_str += program_str[i]
            # case '{':
            #     br_sum += 1
            #     if br_sum == nest_lvl:
            #         i, br_str = get_br_string(program_str, i, defines)
            #     new_str += br_str
        # i += 1
    for char in program_str:
        match char:
            case '!' | '<' | '>' | '[' | ']':
                new_str += char
    return new_str
