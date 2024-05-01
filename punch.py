import sys
from datetime import datetime

from timelog import TimeLog, LogEntry
from uploading import Upload
import constants as c
from constants import PUNCHED_IN_STATE, PUNCHED_OUT_STATE, dprint, eprint


def display_usage() -> None:
    print(
        """
Usage: punch <command> [options]

Commands:
  in        Record punch-in time
  out       Record punch-out time
  state     Output the current state of the TimeLog
  upload    Upload current .csv file to Google Sheets worksheet
  show csv  Output the contents of the csv file
  email     Display the service email account

Coming soon:
  show log          TODO - Output the contents of either the csv or log file
  edit [csv|log]    TODO - Open a program to manually edit the contents of either file

Options:
  -h, --help                Show this usage menu
  --desc "[description]"    Add or replace existing work description
  --debug                   Run with debug messages
"""
    )


def show_csv(log: TimeLog) -> bool:
    """Outputs uncommitted entries in the csv file.

    :returns `bool` - Whether there were any uncommited entries.
    """

    rows = log.get_rows()
    if rows:
        print("\nUncommitted timelog entries:")
        for row in rows:
            print("\t", end="")
            for i, item in enumerate(row):
                print(item, end=", " if i != len(row) - 1 else "\n")
        print()
        return True
    else:
        print("\nNo uncommitted entries in timelog.\n")
        return False


def main() -> None:
    """Main function."""
    if "--debug" in sys.argv:
        c._debug = True
    dprint(f"{sys.argv=}")

    log = TimeLog()
    entry = LogEntry(log.csv_file_path)

    try:
        if "--desc" in sys.argv and sys.argv[sys.argv.index("--desc") + 1]:
            # Descriptions with commas cause a bug with getting the entries from `.csv` TODO better solution
            entry.description = sys.argv[sys.argv.index("--desc") + 1].replace(",", ";")
        else:
            entry.read_desc()

        if "--help" in sys.argv or "-h" in sys.argv or len(sys.argv) == 1:
            display_usage()
            sys.exit(0)

        elif sys.argv[1] == "in":
            if log.state == PUNCHED_OUT_STATE:
                # Record Punch-in datetime
                time_in: datetime = datetime.now()
                # Enter Punch-in datetime
                entry.punch_in = time_in
                # Enter date str
                entry.date = entry.punch_in.strftime("%D")
                # Enter Punch-in time str
                entry.punch_in_time = entry.punch_in.strftime("%H:%M")
                # Write to log and csv
                entry.log_punch_in()
                # Display to user
                print(f"\nPUNCH IN AT {entry.date} {entry.punch_in_time}\n")
                # Store the description
                if entry.description:
                    entry.store_desc()
            else:
                log.display_state()
                print()
            sys.exit(0)

        elif sys.argv[1] == "out":
            dprint(f"{entry = }")
            if log.state == PUNCHED_IN_STATE:
                # Enter date str
                entry.date = log.last_entry.date
                # Enter Punch-in time str
                entry.punch_in_time = log.last_entry.punch_in_time
                # Convert to datetime object and enter
                entry.punch_in = entry.convert_str_to_datetime(entry.punch_in_time)

                # Record Punch-out datetime
                time_out: datetime = datetime.now()
                # Enter Punch-out datetime
                entry.punch_out = time_out
                # Enter Punch-out time str
                entry.punch_out_time = entry.punch_out.strftime("%H:%M")
                # Write to log and next value in csv line
                entry.log_punch_out()
                # Display to user
                print(f"\nPUNCH OUT AT {entry.date} {entry.punch_out_time}")

                # Calculate and enter timedelta
                entry.get_timedelta()
                # Calculate and enter time-hours
                entry.work_hours = entry.work_time.seconds / (60 * 60)
                # Calculate time-minutes
                work_mins = entry.work_time.seconds / 60
                # Write to log and rest of line in csv
                entry.log_work_time()
                # Display to user
                print(f"Time delta: H:{entry.work_hours:.2f} / M:{work_mins:.1f}\n")
            else:
                log.display_state()
                print()
            sys.exit(0)

        elif sys.argv[1] == "state":
            log.display_state()
            if log.state == PUNCHED_IN_STATE:
                print(
                    "Data from last entry:",
                    f"\n{log.last_entry.date}, punched in at {log.last_entry.punch_in_time} :",
                    (
                        f"'{entry.description}'"
                        if entry.description != "(No Description)"
                        else f"{entry.description}"
                    ),
                )
            if log.state == PUNCHED_OUT_STATE:
                if log.last_entry:
                    print(
                        "Data from last entry:",
                        f"{log.last_entry.date}, {log.last_entry.punch_in_time} - {log.last_entry.punch_out_time} = {log.last_entry.work_hours} : '{log.last_entry.description}'",
                        sep="\n",
                    )
            print()
            sys.exit(0)

        elif sys.argv[1] == "upload":
            if log.state == PUNCHED_IN_STATE:
                eprint(
                    "<upload> command unavailable while punched-in.",
                    "Punch out before attempting to upload timelog data.",
                    sep="\n\t",
                    end="\n",
                )
                log.display_state()
                sys.exit(0)

            dprint("Checking if timelog has entries...")
            rows = log.get_rows()
            if not rows:
                print("\nNothing to upload: no entries in timelog.\n")
                sys.exit(0)

            show_csv(log)

            dprint("Checking if service account is linked with speadsheet(s)...")
            try:
                upload = Upload()
                upload.get_available_spreadsheets()
                if not upload.spreadsheet:
                    eprint(
                        "<upload> command unavailable when no spreadsheets are\n\t"
                        "accessible to Google Service Account.",
                        "To use this feature, please share the spreadsheet\n\t"
                        "with Service Account email:\n\t"
                        f"{upload.gc.auth.signer_email}\n",
                        sep="\n\t",
                    )
                    sys.exit(0)

                dprint(f"Appending to {upload.spreadsheet=}")
                upload.append(rows)
                log.clear_csv()
                dprint("Appended and cleared csv file.")
                print("\nSuccessfully uploaded all uncommitted timelog data.\n")
                sys.exit(0)
            except Exception as err:
                dprint(err)
                eprint("Please connect to the internet to use the upload function.")
                sys.exit(1)

        elif sys.argv[1] == "show":
            if len(sys.argv) <= 2:
                raise Exception

            if sys.argv[2] == "csv":
                entries_shown: bool = show_csv(log)
                if entries_shown:
                    print("<upload> to push rows to google spreadsheet.\n")
                sys.exit(0)
            elif sys.argv[2] == "log":
                ...
            else:
                raise Exception

        elif sys.argv[1] == "email":
            print(f"\nService account email:\n{Upload().gc.auth.signer_email}\n")
        else:
            raise Exception
    except Exception as err:
        eprint("Invalid syntax.", err, sep="\n")
        display_usage()
        sys.exit(1)


if __name__ == "__main__":
    main()
