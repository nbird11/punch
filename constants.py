"""Constants and other super-global variables."""

_debug = False

LOG_FILE_NAME: str = "punch.log"
CSV_FILE_NAME: str = "punch.csv"
DESC_FILE_NAME: str = "description.txt"

PUNCHED_IN_STATE: str = "punched-in"
PUNCHED_OUT_STATE: str = "punched-out"

SERVICE_ACCT_JSON = "C:\\Users\\natha\\AppData\\Local\\punch\\keys\\timesheet-project-372700-6d95058d5340.json"


def dprint(*args, **kwargs):
    """Debug print wrapper."""
    if _debug:
        colored_debug: str = "\u001b[38;5;208mDEBUG:\u001b[0m  "
        if "sep" not in kwargs:
            kwargs["sep"] = f"\n{colored_debug}"
        print(f"{colored_debug}" + str(*args[:1]), *args[1:], **kwargs)


def eprint(*args, **kwargs):
    """Error print wrapper."""
    if "end" not in kwargs:
        kwargs["end"] = "\n\n"
    colored_error: str = "\u001b[31;1mERROR:\u001b[0m  "
    if "sep" not in kwargs:
        kwargs["sep"] = f"\n{colored_error}"
    print(f"\n{colored_error}" + str(*args[:1]), *args[1:], **kwargs)
