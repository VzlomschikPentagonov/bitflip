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

def get_sub_string(program_str: str,
                   pos: int) -> tuple(int, str):
    sub_string: str = ""
    repeat: str = ""
    i: int = pos + 1
    if program_str[i].isidentifier():
        while program_str[i] != '}':
            if program_str[i].isidentifier():
                sub_string += program_str[i]
            # else:
            #     ...
            i += 1
        if ',' in sub_string:
            i_s: int = sub_string.index(',')
    while program_str[i] != ',':
        if program_str[i] in CHAR_SET:
            sub_string += program_str[i]
        # else:
        #     ...
        i += 1
    while program_str[i] != '}':
        if program_str[i].isdigit():
            repeat += program_str[i]
        # else:
        #     ...
        i += 1
    return i, sub_string * int(repeat)

def clean_str(program_str: str) -> str:
    new_str: str = ""
    i: int = 0
    while i < len(program_str):
        match program_str[i]:
            case '!' | '<' | '>' | '[' | ']':
                new_str += program_str[i]
            case '{':
                i, new_str += get_sub_string(program_str, program_str[i])
        i += 1
    return new_str
