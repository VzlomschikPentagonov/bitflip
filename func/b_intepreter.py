from bitflip.func.b_parser import compile_program
from bitflip.func.b_misc import *

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
            open_br[char] = i
            closed_br[i + PREV] = char + NEXT
    return open_br, closed_br

def goto(address_list: dict[int: int],
         addresses_start: dict[int: int],
         pos_p: int) -> tuple[int, bool]:
    for address in addresses_start:
        if address == pos_p:
            pos_p = address_list[address]
            return pos_p, True

def get_output(b_input: tuple[int, str],
               tape: list[int]) -> None:
    num_states: int = b_input[NUM_STATES]
    program_str: str = compile_program(b_input[PROGRAM_STR]) + HALT
    program_str_len: int = len(program_str)
    pointer_t: int = len(tape) >> 1
    pointer_p: int = 0
    flag: bool = False
    steps: int = 0
    open_br, closed_br = get_addresses(program_str)
    open_br_keys: list[int] = list(open_br.keys())
    closed_br_keys: list[int] = list(closed_br.keys())
    # print(open_br, closed_br)
    while program_str[pointer_p] != HALT:
        # print_data(program_str, program_str_len, pointer_p,
        #            pointer_t, tape[pointer_t], steps, len(tape) >> 1)
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
        # if steps > 228: # set breakpoint
        #     break
        if not flag:
            pointer_p += 1
        flag = False
        steps += 1
    print_data(program_str, program_str_len, pointer_p,
               pointer_t, tape[pointer_t], steps, len(tape) >> 1)
    print_tape(tape, 128, 191, 7)
    return None
