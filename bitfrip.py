from func.b_parser import read_input_file, read_include_file
from func.b_intepreter import get_output

def main() -> None:
    b_input: tuple[int, str, int] = read_input_file()
    sub_strs: dict[str: str] = read_include_file()
    tape: list[int] = [0] * 0x100
    get_output(b_input, tape, sub_strs)
    return None

if __name__ == "__main__":
    main()