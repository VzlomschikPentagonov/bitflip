from typing import TextIO
from b_func import get_code

def make_file(name: str) -> None:
    input_file: TextIO = open("input.txt")
    new_file_data: TextIO = open(f"./code/{name}.bflp", "w+t")
    input_file_data: list[str] = input_file.readlines()
    new_file_data.write(get_code(input_file_data))