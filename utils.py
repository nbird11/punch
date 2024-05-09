"""Constants and other super-global variables."""

import os
from datetime import datetime
from time import sleep

_debug = False

CLOCK_FILE = ".clock"

PUNCHED_IN_STATE = "punched in"
PUNCHED_OUT_STATE = "punched out"
BREAK_IN_STATE = "on break"
BREAK_OUT_STATE = "off break"

WORK_DAY_HOURS = 8


def get_clock_file() -> str:
    """Finds the path to the `.clock` file in unix ~/. If doesn't exist, make one.

    RETURNS: the absolute path to the `.clock` file
    """

    clock_file = os.path.expandvars(f"$HOME/{CLOCK_FILE}")
    # IF no .clock file, create one
    if not os.path.exists(clock_file):
        file = open(clock_file, "w")
        file.close()

    return clock_file

def time_as_datetime(time: str):
    return datetime.strptime(time, "%H:%M")


def convert_24_to_12(time: str):
    return time_as_datetime(time).strftime("%I:%M%p")


def add_day_of_week(date: str):
    return datetime.strptime(date, "%b %d, %Y").strftime("%a. %b %d, %Y")


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
    sleep(1)
