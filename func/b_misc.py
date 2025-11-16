from bitflip.func.b_constants import *

def display_cell(cell: int) -> str:
    return chr(OFF + cell * ON)

def display_pointer_p(length: int,
                      pos: int) -> str:
    return ' ' * pos + '^' + ' ' * (length - pos - 1)

def print_data(length: int,
               pos_p: int,
               pos_t: int,
               cell: int,
               steps: int,
               tape_lh: int) -> None:
    print(display_pointer_p(length, pos_p), '\n',
          f"{display_cell(cell)}, {pos_t - tape_lh}, {pos_p}, {steps}",
          sep = '')

def print_tape(tape: list[int],
               start: int,
               end: int,
               chunk_size: int = DEFAULT_CHUNK_SIZE,
               observe_runtime = False,
               pos_t: int = -1,
               runtime: int = -1) -> None:
    tape_str_arr: list[str] = [display_cell(cell) for cell in tape]
    tape_str: str = "".join(tape_str_arr)
    if not observe_runtime:
        print("  " + "".join([chr(CHR_ZERO + digit)
                              for digit in range(chunk_size)]))
    chunk_index: int = 0
    if chunk_size == DEFAULT_CHUNK_SIZE:
        chunk_size = end - start
    for chunk in range(start, end, chunk_size):
        if not observe_runtime:
            print(chunk_index & 15, end = ' ')
        print(tape_str[chunk: chunk + chunk_size], end = "")
        if not observe_runtime:
            print()
        chunk_index += 1
        if runtime >= 0:
            print(f" [{runtime}]")
        if observe_runtime:
            print(display_pointer_p(chunk_size, pos_t))

def print_error(message: str) -> None:
    raise Exception(f"[Error] {message}")