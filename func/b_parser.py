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

def get_sub_string(program_str: str,
                   pos: int) -> tuple(int, str):
    sub_string: str = ""
    code: str = ""
    repeat: str = ""
    i: int = pos + 1
    while program_str[i] != '}':
        sub_string += program_str[i]
        i += 1
    if match("^([!<>\\[\\]]+,\\d+)$", sub_string):
        for char in sub_string:
            if char in CHAR_SET:
                code += char
            if char.isdigit():
                repeat += char
    elif match("^(\\w+,\\d+)$", sub_string, ASCII):
        for char in sub_string:
            if char in CHAR_SET:
                code += char
            if char.isdigit():
                repeat += char
    return i, code * int(repeat)

def clean_str(program_str: str) -> str:
    new_str: str = ""
    i: int = 0
    while i < len(program_str):
        match program_str[i]:
            case '!' | '<' | '>' | '[' | ']':
                new_str += program_str[i]
            case '{':
                i, sub_str = get_sub_string(program_str, program_str[i])
                new_str += sub_str
        i += 1
    return new_str
