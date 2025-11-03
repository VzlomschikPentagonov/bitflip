from func.b_parser import read_input_file, read_defines_file
from func.b_intepreter import get_output

def verify(b_input: tuple[int, str],
           defines: dict[str: str], *args) -> None:
    if args[0] > args[1]:
        print(f"Verification failed! ({args[0]}, {args[1]}")
    print("Program verified successfully!")

def main() -> None:
    b_input: tuple[int, str] = read_input_file()
    defines: dict[str: str] = read_defines_file()
    tape: list[int] = [0] * 0x100
    get_output(b_input, tape)
    return None

if __name__ == "__main__":
   main()
