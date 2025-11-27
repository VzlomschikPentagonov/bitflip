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
               **kwargs: bool | int) -> None | int | list[list[bytes]]:
    program_str: str = compile_program(b_input[PROGRAM_STR], sub_strs) + HALT
    var: list[int | bool] = [len(program_str), len(tape) >> 1, 0, False, 0]
    open_br, closed_br = get_addresses(program_str)
    open_br_keys: list[int] = list(open_br.keys())
    closed_br_keys: list[int] = list(closed_br.keys())
    if(not kwargs["verify"] and not kwargs["observe_runtime"]
       and not kwargs["track_runtime"]):
        print(program_str)
    image_data: list[list[bytes]] = []
    while program_str[var[POINTER_P]] != HALT:
        match program_str[var[POINTER_P]]:
            case '!':
                tape[var[POINTER_T]] += 1
                tape[var[POINTER_T]] %= b_input[NUM_STATES]
            case '<':
                var[POINTER_T] -= 1
            case '>':
                var[POINTER_T] += 1
            case '[':
                if tape[var[POINTER_T]] == 0:
                    var[POINTER_P], var[FLAG] = goto(open_br, open_br_keys,
                                                     var[POINTER_P])
            case ']':
                if tape[var[POINTER_T]] != 0:
                    var[POINTER_P], var[FLAG] = goto(closed_br,
                                                     closed_br_keys,
                                                     var[POINTER_P])
        if var[RUNTIME] == kwargs["breakpoint_"]:
            break
        if kwargs["observe_runtime"]:
            if kwargs["get_image_data"]:
                scanline: list[bytes] = [bytes([cell * GRAY] * 3)
                                         for cell in tape[
                                         kwargs["start"]: kwargs["end"]]]
                scanline[var[POINTER_T] - kwargs["start"]] = (bytes(
                        [WHITE, tape[var[POINTER_T]] * GRAY,
                         tape[var[POINTER_T]] * GRAY]))
                padding: int = (kwargs["end"] - kwargs["start"]) % 4
                scanline.append(bytes(padding))
                image_data.append(scanline)
            else:
                print_tape(tape, kwargs["start"], kwargs["end"],
                           observe_runtime = kwargs["observe_runtime"],
                           pos_t = var[POINTER_T] - (len(tape) >> 1),
                           runtime = var[RUNTIME])
        if not var[FLAG]:
            var[POINTER_P] += 1
        var[FLAG] = False
        var[RUNTIME] += 1
    if(not kwargs["verify"] and not kwargs["observe_runtime"]
       and not kwargs["track_runtime"]):
        print_data(var[PROGRAM_STR_LEN], var[POINTER_P], var[POINTER_T],
                   tape[var[POINTER_T]], var[RUNTIME], len(tape) >> 1)
        print_tape(tape, kwargs["start"], kwargs["end"],
                   chunk_size = kwargs["chunk_size"])
    if kwargs["track_runtime"]:
        return var[RUNTIME]
    if kwargs["observe_runtime"]:
        if kwargs["get_image_data"]:
            return image_data
    return None