from typing import TextIO
from re import match, ASCII
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

def read_defines_file() -> dict[str, str]:
    input_file: TextIO = open("defines.txt")
    input_file_data: list[str] = input_file.readlines()
    defines: dict[str, str] = {}
    for line in input_file_data:
        if match(RM_DEFFILE, line):
            define: str = ""
            code: str = ""
            char: int = 0
            while line[char] != ':':
                define += line[char]
                char += 1
            char += 1
            for c_char in range(char + 1, len(line)):
                code += line[c_char]
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
    elif match(RM_DEFINE, sub_string, ASCII):
        for define in defines.keys():
            if sub_string == define:
                return i, defines[define]

def clean_str(program_str: str) -> str:
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