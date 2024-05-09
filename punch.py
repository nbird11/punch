import sys
from datetime import datetime

from timelog import ClockInterface
import utils
from utils import (
    PUNCHED_IN_STATE,
    PUNCHED_OUT_STATE,
    BREAK_IN_STATE,
    BREAK_OUT_STATE,
    dprint,
    eprint,
)


def display_usage() -> None:
    print(
        """
Usage: punch <command> [options]

Commands:
  in                Record punch-in time
  break             Start or stop a break
    start             Record break start time
    end               Record break end time
  out               Record punch-out time
  state             Output the current state of the TimeLog
    --index           Default index=1. Index from the head entry
    --hours           Default hours=8. How long the work day is

Coming soon:
  reveal            Open a program to manually edit the contents of .clock

Removed:
  show                      Output the contents of the .clock file
  upload                    Upload current .csv file to Google Sheets worksheet
  email                     Display the service email account
  --desc "[description]"    Add or replace existing work description

Options:
  -h, --help        Show this usage menu
  --debug           Run with debug messages
"""
    )


def get_now():
    now = datetime.now()
    date = now.strftime("%b %d, %Y")
    time = now.strftime("%H:%M")
    return f"{time}, {date}"


def main() -> None:
    """Main function."""
    dprint(f"{sys.argv = }")

    if "--debug" in sys.argv:
        utils._debug = True
        sys.argv.remove("--debug")

    try:
        ci = ClockInterface()

        if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
            display_usage()
            sys.exit(0)

        elif sys.argv[1] == "in":
            if ci.check_punch_state() == PUNCHED_OUT_STATE:
                ci.write_punch_in()
                print(f"\nPUNCH IN AT {get_now()}\n")
            else:
                ci.display_state()
            sys.exit(0)

        elif sys.argv[1] == "break":
            if len(sys.argv) < 3:
                raise SyntaxError("Not enough arguments for this command.")
            if ci.check_punch_state() == PUNCHED_IN_STATE:
                if sys.argv[2] == "start":
                    if ci.check_break_state() == BREAK_OUT_STATE:
                        ci.write_break_in()
                        print(f"\nBREAK START AT {get_now()}\n")
                    else:
                        ci.display_state()
                    sys.exit(0)
                elif sys.argv[2] == "end":
                    if ci.check_break_state() == BREAK_IN_STATE:
                        ci.write_break_out()
                        print(f"\nBREAK END AT {get_now()}\n")
                    else:
                        ci.display_state()
                else:
                    raise SyntaxError("Invalid subcommand for <break>.")
            else:
                ci.display_state()

        elif sys.argv[1] == "out":
            if (
                ci.check_punch_state() == PUNCHED_IN_STATE
                and ci.check_break_state() == BREAK_OUT_STATE
            ):
                ci.write_punch_out()
                print(f"\nPUNCH OUT AT {get_now()}\n")
            else:
                ci.display_state()
            sys.exit(0)

        elif sys.argv[1] == "state":
            if len(sys.argv) > 2:
                if "--index" in sys.argv:
                    try:
                        index_from_head = int(sys.argv[sys.argv.index("--index") + 1])
                        if 1 <= index_from_head <= len(ci.entries):
                            ci.focus_entry = ci.entries[-index_from_head]
                        else:
                            raise SyntaxError(f"<state> index must be a number from 1 to {len(ci.entries)}")
                    except IndexError:
                        raise SyntaxError("No argument given to --index option.")
                    except ValueError:
                        raise SyntaxError("<state> index must be a number.")
                    
                if "--hours" in sys.argv:
                    try:
                        work_hours = float(sys.argv[sys.argv.index("--hours") + 1])
                        if 1 <= work_hours <= 24:
                            ci.work_hours = work_hours
                        else:
                            raise SyntaxError(f"<state> --hours must be a number from 1 to 24")
                    except IndexError:
                        raise SyntaxError("No argument given to --index option.")
                    except ValueError:
                        raise SyntaxError("<state> --index must be a number.")

            ci.display_state()
            ci.display_last_clock_event()
            if ci.check_punch_state() == PUNCHED_IN_STATE:
                ci.disply_time_until_8_hours()

            elif ci.check_punch_state() == PUNCHED_OUT_STATE:
                ci.display_total_time()

            else:
                assert False, "`punch_state` should be one of only 2 values."
            sys.exit(0)

        elif sys.argv[1] == "upload":
            raise SyntaxError("Upload feature has been removed for simplicity.")

        elif sys.argv[1] == "show":
            raise SyntaxError("Show feature has been removed for simplicity.")

        elif sys.argv[1] == "email":
            raise SyntaxError("Email feature has been removed for simplicity.")

        else:
            raise SyntaxError("No recognized command was given.")
    except SyntaxError as err:
        eprint("Invalid syntax:", err, sep=" ")
        display_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
