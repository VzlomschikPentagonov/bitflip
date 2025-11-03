from func.b_parser import read_input_file, read_defines_file
from func.b_intepreter import get_output

def main() -> None:
    b_input: tuple[int, str] = read_input_file()
    defines: dict[str: str] = read_defines_file()
    tape: list[int] = [0] * 0x100
    get_output(b_input, tape, defines)
    return None

if __name__ == "__main__":
   main()
