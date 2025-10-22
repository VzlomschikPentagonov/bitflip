from typing import TextIO
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

def clean_str(program_str: str) -> str:
    new_str: str = ""
    i: int = 0
    sub_string: str = ""
    repeat: str = ""
    while i < len(program_str):
        match program_str[i]:
            case '!' | '<' | '>' | '[' | ']':
                new_str += program_str[i]
            case '{':
                i += 1
                while program_str[i] != ',':
                    if program_str[i] in CHAR_SET:
                        sub_string += program_str[i]
                    i += 1
                while program_str[i] != '}':
                    if program_str[i].isdigit():
                        repeat += program_str[i]
                    i += 1
                new_str += sub_string * int(repeat)
                sub_string, repeat = "", ""
        i += 1
    return new_str