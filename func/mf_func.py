from bitflip.func.b_parser import get_code
from bitflip.func.b_constants import *
from bitflip.func.b_misc import print_error
from typing import TextIO, BinaryIO
from os import listdir, mkdir, chdir
from re import match
from ctypes import c_uint64

def read_file(file: TextIO) -> list[str]:
    file.seek(0)
    file_data: list[str] = file.readlines()
    file_data[0:0] = [""]
    return file_data

def make_project(name: str,
                 input_file: TextIO) -> None:
    chdir("./code")
    name = name.split('.')[PROJNAME]
    mkdir(name)
    chdir(name)
    main: TextIO = open("main.bflp", "w+t")
    config: BinaryIO = open("config", "w+b")
    tokens: list[str] = ["include.hbflp", "docs.txt"]
    input_file_data: list[str] = input_file.readlines()
    main.write(get_code(input_file_data))
    config_data: list[str] = input_file_data[0].split(',')
    num_states: c_uint64 = c_uint64(int(config_data[NUM_STATES]))
    tape_len: c_uint64 = c_uint64(int(config_data[TAPE_LEN]))
    config_byte_str: bytes = b""
    config_byte_str += bytes(num_states) + bytes(tape_len)
    config.write(config_byte_str)
    queue: TextIO = open("queue.txt", "w+t")
    queue.write("include")
    for token in tokens:
        split_token: list[str] = token.split('.')
        mkdir(split_token[0])
        open(f"./{split_token[0]}/{split_token[0]}"
             + '.' + split_token[1], "w+t")

def load_project(name: str,
                 input_file: TextIO,
                 include_file: TextIO) -> None:
    name = name.split('.')[PROJNAME]
    chdir(f"./code/{name}")
    config: BinaryIO = open("config", "r+b")
    queue: TextIO = open("queue.txt")
    num_states: int = int.from_bytes(config.read(SIZEOF_UINT64),
                                     byteorder = "little")
    tape_len: int = int.from_bytes(config.read(SIZEOF_UINT64),
                                   byteorder = "little")
    input_file.write(f"{num_states},{tape_len}\n"
                     + get_code(code_file_data))
    chdir("./include")
    for include in queue.readlines():
        pj_include_file: TextIO = open(f"{include.rstrip('\n')}.hbflp")
        include_file.write(pj_include_file.readlines() + '\n')

def make_file(name: str) -> None:
    input_file: TextIO = open("input.txt")
    include_file: TextIO = open("include.txt")
    if match(RE_FILENAME, name):
        new_file: TextIO = open(f"./code/{name}.bflp", "w+t")
        input_file_data: list[str] = input_file.readlines()
        if len(include_file.readlines()) != 0:
            header_file: TextIO = open(f"./code/{name}.hbflp", "w+t")
            header_file_data: list[str] = read_file(include_file)
            header_file.write(get_code(header_file_data))
        new_file.write(get_code(input_file_data))
    elif match(RE_PROJNAME, name):
        make_project(name, input_file)
    else:
        print_error("Invalid filename")

def load_file(name: str) -> None:
    input_file: TextIO = open("input.txt", "w+t")
    include_file: TextIO = open("include.txt", "w+t")
    if match(RE_FILENAME, name):
        code_file: TextIO = open(f"./code/{name}.bflp")
        header_file_data: list[str] = ["", ""]
        if f"{name}.hbflp" in listdir("./code/"):
            header_file: TextIO = open(f"./code/{name}.hbflp")
            header_file_data: list[str] = read_file(header_file)
        code_file_data: list[str] = read_file(code_file)
        input_file.write("2\n" + get_code(code_file_data))
        include_file.write(get_code(header_file_data))
    elif match(RE_PROJNAME, name):
        load_project(name, input_file, include_file)
    else:
        print_error("Invalid filename")
