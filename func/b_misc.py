from bitflip.func.b_constants import *

def display_pointer_p(length: int,
                      pos: int) -> str:
    return ' ' * pos + '^' + ' ' * (length - pos - 1)

def print_data(program_str: str,
               length: int,
               pos_p: int,
               pos_t: int,
               cell: int,
               steps: int,
               tape_lh: int) -> None:
    print('\n', program_str, '\n',
          display_pointer_p(length, pos_p), '\n',
          f"{chr(OFF + cell)}, {pos_t - tape_lh}, {pos_p}, {steps}",
          sep = '')

def print_tape(tape: list[int],
               start: int,
               end: int,
               chunk_size: int):
    tape_str_arr: list[str] = [chr(OFF + cell) for cell in tape]
    tape_str: str = "".join(tape_str_arr)
    print("  " + "".join([chr(48 + digit) for digit in range(chunk_size)]))
    chunk_index: int = 0
    for chunk in range(start, end, chunk_size):
        print(chunk_index & 15, tape_str[chunk: chunk + chunk_size])
        chunk_index += 1