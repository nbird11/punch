"""Houses the `TimeLog` and `LogEntry` classes."""

import os
from datetime import datetime, timedelta
from constants import (
    LOG_FILE_NAME,
    CSV_FILE_NAME,
    DESC_FILE_NAME,
    PUNCHED_IN_STATE,
    PUNCHED_OUT_STATE,
    dprint,
)


class TimeLog:
    def __init__(self):
        """Handles operations having to do with all LogEntries currently recorded
        in the `.csv` file.
        """
        # TODO: make TimeLog add up all the time worked over each entry
        #    in the log and get the total

        self.csv_file_path: str = self.find_csv_file()
        self.entries: list[LogEntry] = self.record_entries()
        self.last_entry: LogEntry | None = None
        if self.entries:
            self.last_entry = self.entries[-1]

        dprint("TimeLog.last_entry =", self.last_entry, sep=" ")

        self.state: str = self.check_state()

    def find_csv_file(self) -> str:
        """Finds the path to the `.csv` file in win32 local appdata.

        :returns `str` - the absolute path to the `.csv` file
        """

        csv_file_path = os.path.expandvars("%LOCALAPPDATA%\\punch\\" + CSV_FILE_NAME)
        # IF no csv file, create one with heading
        if not os.path.exists(csv_file_path):
            file = open(csv_file_path, "w")
            file.write("Date,Punch in,Punch out,Time (hours),Description")
            file.close()
        # IF csv file has no heading, write heading
        else:
            with open(csv_file_path, "r") as r_file:
                if not r_file.readline().strip():
                    with open(csv_file_path, "w") as w_file:
                        w_file.write("Date,Punch in,Punch out,Time (hours),Description")
        # dprint("IN find_csv_file(): file_path =", csv_file_path, sep=" ")

        return csv_file_path

    def record_entries(self) -> list:
        """Get all the entries from the `.csv` file and record them in a list.

        :returns list[LogEntry] - the list of LogEntries
        """

        entries: list[LogEntry] = []

        with open(self.csv_file_path, "r") as file:
            # Skip header line
            next(file)
            for line in file:
                dprint(f"{line = }")
                if (not line.strip()):
                    continue
                entry: LogEntry = LogEntry(self)
                # IF entry has all 5 data
                if len(line.strip().split(",")) == 5:
                    (
                        date,
                        punch_in_time,
                        punch_out_time,
                        work_hours,
                        description,
                    ) = line.strip().split(",")

                    entry.date = date
                    entry.punch_in_time = punch_in_time
                    entry.punch_out_time = punch_out_time
                    entry.work_hours = float(work_hours)
                    entry.description = description

                # IF entry only has 2 data
                elif len(line.strip().split(",")) == 2:
                    (entry.date, entry.punch_in_time) = line.strip().split(",")
                else:
                    assert (
                        False
                    ), "Entry from the `.csv` file should have either 5 data or 2 data."

                entries.append(entry)

        return entries

    def check_state(self) -> str:
        """Checks the status of the last entry to see if it has data related
        to the state.
        """

        # IF last_entry has some data (not None) but doesn't have a
        #    punch_out_time, then the state of the program is currently punched-in
        return (
            PUNCHED_IN_STATE
            if self.last_entry and not self.last_entry.punch_out_time
            else PUNCHED_OUT_STATE
        )

    def display_state(self) -> None:
        """Outputs the current state to the screen."""
        print(f"\nCurrent state of TimeLog is {self.state}.")
        if self.state == PUNCHED_IN_STATE:
            print(
                "<in>, <upload> commands unavailable. Try 'punch out [--desc \"\"]'\n"
            )
        elif self.state == PUNCHED_OUT_STATE:
            print("<out> command unavailable. Try 'punch in [--desc \"\"]'\n")

    def get_rows(self) -> list:
        """Gets rows from `.csv` (for uploading to spreadsheet)"""
        rows = []
        with open(self.csv_file_path, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                # Skip heading
                if line.startswith("Date"):
                    continue
                date, p_i_time, p_o_time, hours, desc = line.split(",")
                rows.append([date, p_i_time, p_o_time, hours, desc])
        dprint(f"{rows=}")
        return rows

    def clear_csv(self):
        """Clears the `.csv` file of values.

        Called after uploading information to Google Sheets wks.
        """
        with open(self.csv_file_path, "w") as file:
            file.write("Date,Punch in,Punch out,Time (hours),Description")


class LogEntry:
    def __init__(self, csv_path: str) -> None:
        """Records and stores data for a single entry to be written to a log."""

        self.csv_file_path: str = csv_path
        self.log_file_path: str = self.find_log_file()

        self.date: str = ""

        self.punch_in: datetime = None
        self.punch_in_time: str = ""

        self.punch_out: datetime = None
        self.punch_out_time: str = ""

        self.work_time: timedelta = None
        self.work_hours: float = None

        self.description: str = ""

    def find_log_file(self) -> str:
        """Finds the path to the `.log` file relative to the location of the script.

        :returns `str` - the absolute path to the `.log` file
        """

        log_file_path = os.path.expandvars("%LOCALAPPDATA%\\punch\\" + LOG_FILE_NAME)

        if not os.path.exists(log_file_path):
            file = open(log_file_path, "x")
            file.close()

        # dprint("IN find_log_file(): file_path =", log_file_path, sep=" ")

        return log_file_path

    def log_punch_in(self) -> None:
        """Writes a punch-in to `.log`and `.csv` files."""

        # Write to the .log file
        with open(self.log_file_path, "a") as w_log_file:
            r_log_file = open(self.log_file_path, "r")
            if r_log_file.readline().strip():
                w_log_file.write("\n")
            r_log_file.close()
            w_log_file.write(f"Punch in:\t\t{self.date} {self.punch_in_time}")

        # Write to the .csv file
        with open(self.csv_file_path, "a") as w_csv_file:
            w_csv_file.write(f"\n{self.date},{self.punch_in_time}")

    def log_punch_out(self) -> None:
        """Writes a punch-out to `.log` and `.csv` files."""

        # Write to the .log file
        with open(self.log_file_path, "a") as log_file:
            log_file.write(f"\nPunch out:\t\t{self.date} {self.punch_out_time}")

        # Write to the .csv file
        with open(self.csv_file_path, "a") as csv_file:
            csv_file.write(f",{self.punch_out_time},")

    def get_timedelta(self) -> None:
        """Calculates and stores in self the time delta (difference) between
        self punch in/out times.
        """
        self.work_time = self.punch_out - self.punch_in

    def log_work_time(self) -> None:
        """Writes the punch in/out time difference to the log and csv files."""

        # Handle a blank description for user-friendly log file
        if not self.description:
            self.description = "(No Description)"
        # Write to the log file
        with open(self.log_file_path, "a") as log_file:
            log_file.write(
                f"\nHours worked:\t{self.work_hours:.6f}\t\t{self.description}\n"
            )

        # Handle a blank description for csv file
        if self.description == "(No Description)":
            self.description = "NULL"
        # Write to the csv file
        with open(self.csv_file_path, "a") as csv_file:
            csv_file.write(f"{self.work_hours},{self.description}")

        # Save 'NULL' as description

        # <Null Description Handling>
        # # Reset description
        # if self.description == "NULL":
        #     self.description = ''
        # </>

        try:
            self.del_desc()
        except:
            pass

    def store_desc(self) -> None:
        """Writes the punch-in description to a temporary `.txt` file, to be read later
        if the program runs from the punched-in state.
        """
        with open(
            os.path.expandvars("%LOCALAPPDATA%\\punch\\" + DESC_FILE_NAME), "w"
        ) as file:
            file.write(self.description)

    def read_desc(self) -> None:
        """Reads the punch-in description from the `.txt` file if there is one."""
        desc_file_path = os.path.expandvars("%LOCALAPPDATA%\\punch\\" + DESC_FILE_NAME)
        if os.path.exists(desc_file_path):
            with open(desc_file_path, "r") as file:
                self.description = file.readline().strip()
        else:
            self.description = "(No Description)"

    def del_desc(self) -> None:
        """Deletes the temporary description `.txt` file."""
        desc_file_path = os.path.expandvars("%LOCALAPPDATA%\\punch\\" + DESC_FILE_NAME)
        os.remove(desc_file_path)

    def convert_str_to_datetime(self, punch_time: str) -> datetime:
        """Calls the `datetime.strptime()` function to convert the str information
        contained in the `LogEntry` to a `datetime` object.
        """
        punch_datetime_str: str = f"{self.date} {punch_time}"
        return datetime.strptime(punch_datetime_str, "%m/%d/%y %H:%M")

    def __repr__(self) -> str:
        attrs = f"date='{self.date}', "
        attrs += f"punch_in_time='{self.punch_in_time}', "
        attrs += f"punch_out_time='{self.punch_out_time}', "
        attrs += f"work_hours={self.work_hours}, "
        attrs += f"description='{self.description}'"
        return f"LogEntry({attrs})"
