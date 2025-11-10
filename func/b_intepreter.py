from bitflip.func.b_parser import compile_program
from bitflip.func.b_misc import *

def move_address(program_str: str,
                 addresses: dict[int, int],
                 char: str) -> dict[int, int]:
    keys: list[int] = list(addresses.keys())
    for address in keys:
        while program_str[addresses[address]] == char:
            addresses[address] += 1
    return addresses

def get_addresses(program_str: str) -> tuple[dict[int, int],
                                             dict[int, int]]:
    open_br: dict[int, int] = {}
    closed_br: dict[int, int] = {}
    for char in range(len(program_str)):
        if program_str[char] == '[':
            i: int = char + NEXT
            bracket_sum: int = 0
            while bracket_sum != LOOP_END:
                match program_str[i]:
                    case '[':
                        bracket_sum += 1
                    case ']':
                        bracket_sum -= 1
                i += 1
            if bracket_sum != LOOP_END:
                print_error(f"Unmatched bracket at position {char}")
            open_br[char] = i
            closed_br[i + PREV] = char + NEXT
    move_address(program_str, open_br, ']')
    move_address(program_str, closed_br, '[')
    return open_br, closed_br

def goto(address_list: dict[int: int],
         addresses_start: dict[int: int],
         pos_p: int) -> tuple[int, bool]:
    for address in addresses_start:
        if address == pos_p:
            pos_p = address_list[address]
            return pos_p, True

def get_output(b_input: tuple[int, str, int],
               tape: list[int],
               sub_strs: dict[str: str],
               track_runtime: bool = False,
               verify: bool = False,
               observe_runtime: bool = False,
               breakpoint: int = -1) -> None | int:
    num_states: int = b_input[NUM_STATES]
    program_str: str = compile_program(b_input[PROGRAM_STR], sub_strs) + HALT
    program_str_len: int = len(program_str)
    pointer_t: int = len(tape) >> 1
    pointer_p: int = 0
    flag: bool = False
    runtime: int = 0
    open_br, closed_br = get_addresses(program_str)
    open_br_keys: list[int] = list(open_br.keys())
    closed_br_keys: list[int] = list(closed_br.keys())
    if not verify:
        print(program_str)
    while program_str[pointer_p] != HALT:
        match program_str[pointer_p]:
            case '!':
                tape[pointer_t] += 1
                tape[pointer_t] %= num_states
            case '<':
                pointer_t -= 1
            case '>':
                pointer_t += 1
            case '[':
                if tape[pointer_t] == 0:
                    pointer_p, flag = goto(open_br, open_br_keys, pointer_p)
            case ']':
                if tape[pointer_t] != 0:
                    pointer_p, flag = goto(closed_br,
                                           closed_br_keys, pointer_p)
        if runtime == breakpoint:
            break
        if observe_runtime:
            print_tape(tape, 128, 191, observe_runtime = True)
        if not flag:
            pointer_p += 1
        flag = False
        runtime += 1
    if not verify:
        print_data(program_str_len, pointer_p, pointer_t,
                   tape[pointer_t], runtime, len(tape) >> 1)
        print_tape(tape, 128, 191, chunk_size = 7)
    if track_runtime:
        return runtime
    return None
