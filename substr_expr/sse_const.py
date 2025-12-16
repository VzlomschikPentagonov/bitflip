# various constants
SUBSTR_ARGS: int = 0
NUM_ARGS: int = 2
START: int = 0
END: int = 1
STEP: int = 2
LENGTH_DEFAULT: int = 1
STR_DEFAULT: str = "%"

# regex strings
RE_SUBSTR_D1: str = r"^[1-9].*\d*$"
RE_SUBSTR_D2: str = r"^\d+$"
RE_SUBSTR_CHARSET: str = r"\^\-\w+,/\s\\"
RE_SUBSTR: str = r"^([%s]*;\d*)$" % RE_SUBSTR_CHARSET
RE_DIGIT_ARG: str = r"^(\d*(-\d+(\+\d+)?)?\^?)$"
RE_KEYWORD_ARG: str = r"^([/\\]\w+)$"
RE_SPLIT_DIGIT_ARG: str = r"[\-+\^]"
