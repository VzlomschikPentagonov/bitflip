from b_func import *

def main() -> None:
    b_input: tuple[int, str] = read_input_file()
    tape: list[int] = [0] * 0x100
    get_output(b_input, tape)
    print(tape)
    return None

if __name__ == "__main__":
   main()