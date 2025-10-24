from typing import TextIO
from bitflip.func.b_parser import get_code
from os import listdir

def read_file(file: TextIO) -> list[str]:
    file.seek(0)
    file_data: list[str] = file.readlines()
    file_data[0:0] = [""]
    return file_data

def make_file(name: str) -> None:
    input_file: TextIO = open("input.txt")
    defines_file: TextIO = open("defines.txt")
    new_file: TextIO = open(f"./code/{name}.bflp", "w+t")
    input_file_data: list[str] = input_file.readlines()
    if len(defines_file.readlines()) != 0:
        header_file: TextIO = open(f"./code/{name}.hbflp", "w+t")
        header_file_data: list[str] = read_file(defines_file)
        header_file.write(get_code(header_file_data))
    new_file.write(get_code(input_file_data))

def load_file(name: str) -> None:
    input_file: TextIO = open("input.txt", "w+t")
    defines_file: TextIO = open("defines.txt", "w+t")
    code_file: TextIO = open(f"./code/{name}.bflp")
    header_file_data: list[str] = ["", ""]
    if f"{name}.hbflp" in listdir("./code/"):
        header_file: TextIO = open(f"./code/{name}.hbflp")
        header_file_data: list[str] = read_file(header_file)
    code_file_data: list[str] = read_file(code_file)
    input_file.write("2\n" + get_code(code_file_data))
    defines_file.write(get_code(header_file_data))