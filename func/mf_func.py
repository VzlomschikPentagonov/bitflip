from typing import TextIO
from bitflip.func.b_parser import get_code

def make_file(name: str) -> None:
    input_file: TextIO = open("input.txt")
    new_file_data: TextIO = open(f"./code/{name}.bflp", "w+t")
    input_file_data: list[str] = input_file.readlines()
    new_file_data.write(get_code(input_file_data))

def load_file(name: str) -> None:
    input_file: TextIO = open("input.txt", "w+t")
    read_file: TextIO = open(f"./code/{name}.bflp")
    load_file_data: list[str] = read_file.readlines()
    load_file_data[0:0] = [""]
    input_file.write("2\n" + get_code(load_file_data))