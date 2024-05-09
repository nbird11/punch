"""Houses the `TimeLog` class."""

import os
from utils import (
    CLOCK_FILE,
    PUNCHED_IN_STATE,
    PUNCHED_OUT_STATE,
    dprint,
)
from clock_interface import ClockInterface


class TimeLog:
    def __init__(self):
        ...

    def parse_entries(self) -> list:
        """Get all the entries from the `.clock` file and record them in a list.

        :returns list[LogEntry] - the list of LogEntries
        """

        entries: list[ClockInterface] = []

        with open(self.clock_file_path, "r") as file:
            for line in file:
                dprint(f"{line = }")
                if not line.strip():
                    continue
                entry: ClockInterface = ClockInterface(self.clock_file_path)
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
                    entry.total_hours = float(work_hours)
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
        with open(self.clock_file_path, "r") as file:
            lines = file.read().splitlines()
            for line in lines:
                # Skip heading
                if line.startswith("Date"):
                    continue
                date, p_i_time, p_o_time, hours, desc = line.split(",")
                rows.append([date, p_i_time, p_o_time, hours, desc])
        dprint(f"{rows=}")
        return rows
