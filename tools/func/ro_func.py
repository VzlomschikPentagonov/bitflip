from bitflip.tools.func.ro_const import *
from typing import BinaryIO

def get_header(img_data: list[list[bytes]]) -> bytes:
    header_file: BinaryIO = open("./bin/header.dat", "r+b")
    header_data: list[int] = list(header_file.read())
    width: int = len(img_data[0]) - 1
    height: int = len(img_data)
    num_pixels: int = width * height * 3
    padding: int = width % 4 * height
    var: dict[int: int] = {TOTAL_SIZE_OFF: num_pixels + padding + HEADER_SIZE,
                           DATA_SIZE_OFF: num_pixels + padding,
                           WIDTH_OFF: width, HEIGHT_OFF: height}
    offsets: dict[int: int] = {TOTAL_SIZE_OFF: S_LONG, DATA_SIZE_OFF: S_LONG,
                               WIDTH_OFF: S_SHORT, HEIGHT_OFF: S_SHORT}
    for offset in offsets.keys():
        header_data[offset: offset + offsets[offset]] = [
        byte for byte in var[offset].to_bytes(offsets[offset], "little")]
    return bytes(header_data)

def get_image(header_data: bytes,
              img_data: list[list[bytes]]) -> None:
    img_file: BinaryIO = open("./runtime.bmp", "w+b")
    img_file.write(header_data + b"".join([b"".join(scanline)
                                           for scanline in reversed(img_data)]))