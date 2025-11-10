# various constants
NUM_STATES: int = 0
PROGRAM_STR: int = 1
TAPE_LEN: int = 1
STRIP_1ST_LINE: int = 1
SUBSTR: int = 0
PROJNAME: int = 1
NEXT: int = 1
PREV: int = -1
LOOP_END: int = -1
KEY: int = 0
VALUE: int = 1
SIZEOF_UINT64: int = 8
CONFIG_LINE: int = 0
NAME: int = 0
FILE_EXT: int = 1
OFF: int = 46
ON: int = 18
CHR_ZERO: int = 48
DEFAULT_CHUNK_SIZE: int = -1
HALT: str = 'h'

# regex strings
CHAR_SET: str = r"!<>[]"
RE_CHARSET: str = r"!<>\[\]"
RE_REPSTR: str = r"^([%s]+,\s*\d+)$" % RE_CHARSET
RE_DEFINE: str = r"^(\w+)$"
RE_DEFFILE: str = r"^(\w+:\s*[%s]*)$" % RE_CHARSET
RE_DEFFILE_BR: str = r"^(\w+:\s*[%s{}\s\w,]+)$" % RE_CHARSET
RE_FILENAME: str = r"^[^\\/*\"<>?.]+$"
RE_PROJNAME: str = r"^\.[^\\/*\"<>?.]+$"
