from bitflip.func.b_parser import read_input_file, read_defines_file
from bitflip.func.b_intepreter import get_output
from bitflip.tools.func.v_func import change_inputs
from bitflip.tools.func.da_func import *

def main() -> None:
    b_input: tuple[int, str] = read_input_file()
    defines: dict[str: str] = read_defines_file()
    tape: list[int] = [0] * 0x100
    runtime_result: list[int] = []
    for input_a in range(16):
        for input_b in range(16):
            change_inputs(defines, input_a, input_b)
            runtime_result.append(get_output(b_input, tape,
                                             defines, track_runtime = True))
            tape: list[int] = [0] * 0x100
    get_runtime_data(runtime_result)
    return None

if __name__ == "__main__":
   main()
