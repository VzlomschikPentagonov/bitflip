# various constants
SUBSTR_ARGS: int = 0
NUM_ARGS: int = 2
START: int = 0

# regex strings
RE_SUBSTR_D1: str = r"^[1-9].*\d*$"
RE_SUBSTR_D2: str = r"^\d+$"
RE_SUBSTR: str = r"^([\w\-+\^/\\,\s]*\|\d*)$"
RE_DIGIT_ARG: str = r"^(\d*(-\d+(\+\d+)?)?\^?\d*)$"
RE_STARTW_ARG: str = r"^(/\w+)$"
RE_ENDSW_ARG: str = r"^([\]\w+)$"
RE_KEYWORD_ARG: str = r"^(\w+)$"
