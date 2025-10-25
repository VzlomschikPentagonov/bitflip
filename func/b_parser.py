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

def count_brackets(line: str) -> bool:
    br_sum: int = 0
    for char in line:
        match char:
            case '{':
                br_sum += 1
            case '}':
                br_sum -= 1
        if 2 <= br_sum <= -1:
            return False
    if br_sum == 0:
        return True
    return False

def parse_define_line(line: str) -> tuple[str, str]:
    define: str = ""
    code: str = ""
    char: int = 0
    while line[char] != ':':
        define += line[char]
        char += 1
    char += 1
    for c_char in range(char + 1, len(line)):
        code += line[c_char]
    if code[-1] == '\n':
        code = code[:-1]
    return define, code

def remove_brackets(code: str,
                    defines: dict[str, str]) -> str:
    string: str = ""
    br_sum: int = 0
    new_code: str = ""
    nest_code: str = ""
    repeat: str = ""
    for char in code:
        match char:
            case '{' | '}':
                br_sum ^= 1
                if br_sum == 0:
                    string = string[1:]
                    if match(RM_REPSTR, string):
                        for s_char in string:
                            if s_char in CHAR_SET:
                                nest_code += s_char
                            if s_char.isdigit():
                                repeat += s_char
                        new_code += nest_code * int(repeat)
                    elif match(RM_DEFINE, string):
                        for define in defines.keys():
                            if string == define:
                                new_code += defines[define]
                    string, nest_code, repeat = "", "", ""
        if br_sum == 1:
            string += char
        if br_sum == 0 and char != '}':
            new_code += char
    return new_code

def read_defines_file() -> dict[str, str]:
    input_file: TextIO = open("defines.txt")
    input_file_data: list[str] = input_file.readlines()
    defines: dict[str, str] = {}
    for line in input_file_data:
        if match(RM_DEFFILE, line):
            define, code = parse_define_line(line)
            defines[define] = code
        elif match(RM_DEFFILE_BR, line):
            define, code = parse_define_line(line)
            if count_brackets(code):
                code = remove_brackets(code, defines)
            defines[define] = code
    return defines

def get_sub_string(program_str: str,
                   pos: int,
                   defines: dict[str, str]) -> tuple[int, str]:
    sub_string: str = ""
    code: str = ""
    repeat: str = ""
    i: int = pos + 1
    while program_str[i] != '}':
        sub_string += program_str[i]
        i += 1
    if match(RM_REPSTR, sub_string):
        for char in sub_string:
            if char in CHAR_SET:
                code += char
            if char.isdigit():
                repeat += char
        return i, code * int(repeat)
    elif match(RM_DEFINE, sub_string):
        for define in defines.keys():
            if sub_string == define:
                return i, defines[define]

def compile_program(program_str: str) -> str:
    new_str: str = ""
    i: int = 0
    defines: dict[str, str] = read_defines_file()
    while i < len(program_str):
        match program_str[i]:
            case '!' | '<' | '>' | '[' | ']':
                new_str += program_str[i]
            case '{':
                i, sub_str = get_sub_string(program_str, i, defines)
                new_str += sub_str
        i += 1
    return new_str