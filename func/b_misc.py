from bitflip.func.b_constants import *

def display_pointer_p(length: int,
                            pos: int) -> str:
    return ' ' * pos + '^' + ' ' * (length - pos - 1)

def print_data(program_str: str,
               length: int,
               pos_p: int,
               pos_t: int,
               cell: int,
               steps: int) -> None:
    print('\n', program_str, '\n',
          display_pointer_p(length, pos_p), '\n',
          f'{chr(OFF + cell)}, {pos_t}, {pos_p}, {steps}', sep='')