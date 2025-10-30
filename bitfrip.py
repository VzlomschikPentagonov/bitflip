from func.b_parser import read_input_file
from func.b_intepreter import get_output
from func.b_misc import print_tape

def main() -> None:
    b_input: tuple[int, str] = read_input_file()
    tape: list[int] = [0] * 0x100
    get_output(b_input, tape)
    print_tape(tape)
    return None

if __name__ == "__main__":
   main()