from typing import TextIO
from b_constants import *

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

def get_addresses(program_str: str) -> tuple[dict[int, int], dict[int, int]]:
    open_br: dict[int, int] = {}
    closed_br: dict[int, int] = {}
    for char in range(len(program_str)):
        if program_str[char] == '[':
            i: int = char + NEXT
            bracket_sum = 0
            while bracket_sum != LOOP_END:
                match program_str[i]:
                    case '[':
                        bracket_sum += 1
                    case ']':
                        bracket_sum -= 1
                i += 1
            open_br[char] = i
            closed_br[i + PREV] = char + NEXT
    return open_br, closed_br

def display_program_pointer(length: int,
                            pos: int) -> str:
    return ' ' * pos + '^' + ' ' * (length - pos - 1)

def print_data(program_str: str,
               length: int,
               pos_p: int,
               pos_t: int,
               cell: int,
               steps: int) -> None:
    print('\n', program_str, '\n',
          display_program_pointer(length, pos_p), '\n',
          f'{chr(OFF + cell)}, {pos_t}, {pos_p}, {steps}, ', sep='')

def clean_str(program_str: str) -> str:
    new_str: str = ""
    for char in program_str:
        match char:
            case '!' | '<' | '>' | '[' | ']':
                new_str += char
    return new_str

def get_output(b_input: tuple[int, str],
               tape: list[int]) -> None:
    num_states: int = b_input[NUM_STATES]
    program_str: str = clean_str(b_input[PROGRAM_STR]) + HALT
    program_str_len: int = len(program_str)
    tape_pointer: int = len(tape) >> 1
    program_pointer: int = 0
    flag: bool = False
    steps: int = 0
    open_br, closed_br = get_addresses(program_str)
    open_br_keys: list[int] = list(open_br.keys())
    closed_br_keys: list[int] = list(closed_br.keys())
    print(open_br, closed_br)
    while program_str[program_pointer] != HALT:
        print_data(program_str, program_str_len, program_pointer,
                   tape_pointer, tape[tape_pointer], steps)
        match program_str[program_pointer]:
            case '!':
                tape[tape_pointer] += 1
                tape[tape_pointer] %= num_states
            case '<':
                tape_pointer -= 1
            case '>':
                tape_pointer += 1
            case '[':
                if tape[tape_pointer] == 0:
                    for address in open_br_keys:
                        if address == program_pointer:
                            program_pointer = open_br[address]
                            flag = True
                            break
            case ']':
                if tape[tape_pointer] != 0:
                    for address in closed_br_keys:
                        if address == program_pointer:
                            program_pointer = closed_br[address]
                            flag = True
                            break
        if not flag:
            program_pointer += 1
        flag = False
        steps += 1
    print_data(program_str, program_str_len, program_pointer,
               tape_pointer, tape[tape_pointer], steps)
    return None