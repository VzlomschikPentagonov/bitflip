from bitflip.func.b_parser import read_input_file, read_include_file
from bitflip.func.b_intepreter import get_output
from bitflip.tools.func.ro_func import *
from bitflip.func.b_constants import TAPE_LEN_MAIN

def main() -> None:
    b_input: tuple[int, str, int] = read_input_file()
    sub_strs: dict[str: str] = read_include_file()
    tape: list[int] = [0] * b_input[TAPE_LEN_MAIN]
    get_output(b_input, tape, sub_strs,
               breakpoint_ = -1,
               verify = False,
               track_runtime = False,
               observe_runtime = True,
               start = 128, end = 191)
    dummy_func()
    return None

if __name__ == "__main__":
   main()