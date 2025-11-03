from bitflip.func.b_parser import read_input_file, read_defines_file
from bitflip.func.b_intepreter import get_output
from bitflip.verificator.v_func import *
from bitflip.func.b_misc import display_cell
def main() -> None:
    b_input: tuple[int, str] = read_input_file()
    defines: dict[str: str] = read_defines_file()
    tape: list[int] = [0] * 0x100
    status: bool = True
    for input_a in range(16):
        for input_b in range(16):
            change_inputs(defines, input_a, input_b)
            get_output(b_input, tape, defines)
            status = verify(tape, input_a, input_b)
            check_sum: int = calculate_check_sum(tape)
            print(display_cell(check_sum), end = "")
            tape: list[int] = [0] * 0x100
        print()
    if status:
        print("Program verified successfully!")
    return None

if __name__ == "__main__":
   main()