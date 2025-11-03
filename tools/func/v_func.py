from bitflip.tools.func.v_const import *

def change_inputs(defines: dict[str, str],
                  *inputs) -> None:
    defines['a'] = defines[str(inputs[0])]
    defines['b'] = defines[str(inputs[1])]

def calculate_check_sum(tape: list[int]) -> int:
    check_sum: int = 0
    for cell in CELLS_ON:
        check_sum += tape[cell]
    for cell in CELLS_OFF:
        check_sum += tape[cell]
    check_sum += tape[OUT_CELL]
    return check_sum - 3

def verify(tape: list[int],
           *inputs) -> bool:
    status: bool = True
    for cell in CELLS_ON:
        if tape[cell] == 0:
            status = False
    for cell in CELLS_OFF:
        if tape[cell] == 1:
            status = False
    if inputs[0] <= inputs[1] and tape[OUT_CELL] == 1:
        status = False
    if inputs[0] > inputs[1] and tape[OUT_CELL] == 0:
        status = False
    if status:
        return status
    else:
        print(f"Verification failed! ({inputs[0]}, {inputs[1]})")
        return status