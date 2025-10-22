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
    for char in program_str:
        match char:
            case '!' | '<' | '>' | '[' | ']':
                new_str += char
    return new_str