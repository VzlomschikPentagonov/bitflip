from bitflip.func.b_parser import read_input_file, read_include_file
from bitflip.func.b_intepreter import get_output
from bitflip.tools.func.v_func import *
from bitflip.func.b_misc import display_cell
from bitflip.func.b_constants import TAPE_LEN_MAIN

def main() -> None:
    b_input: tuple[int, str, int] = read_input_file()
    sub_strs: dict[str: str] = read_include_file()
    tape: list[int] = [0] * b_input[TAPE_LEN_MAIN]
    status: bool = True
    for input_a in range(16):
        for input_b in range(16):
            change_inputs(sub_strs, input_a, input_b)
            get_output(b_input, tape, sub_strs,
                       breakpoint_ = -1,
                       verify = True,
                       track_runtime = False,
                       observe_runtime = False)
            status = verify(tape, input_a, input_b)
            check_sum: int = calculate_check_sum(tape)
            print(display_cell(check_sum), end = "")
            tape: list[int] = [0] * b_input[TAPE_LEN_MAIN]
        print()
    if status:
        print("Program verified successfully!")
    return None

if __name__ == "__main__":
   main()