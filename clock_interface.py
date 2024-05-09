from datetime import datetime, timedelta
from utils import (
    dprint,
    get_clock_file,
    time_as_datetime,
    convert_24_to_12,
    add_day_of_week,
    PUNCHED_IN_STATE,
    PUNCHED_OUT_STATE,
    BREAK_IN_STATE,
    BREAK_OUT_STATE,
    WORK_DAY_HOURS,
)
from log_entry import LogEntry


class ClockInterface:
    def __init__(self):
        """Reads from and writes to the .clock file."""

        self.clock_file: str = get_clock_file()

        self.entries: list = self.parse_entries()
        self.focus_entry: LogEntry = None
        if self.entries:
            self.focus_entry = self.entries[-1]

        self.work_hours = WORK_DAY_HOURS

        dprint(f"{self.entries = }")
        dprint(f"{self.focus_entry = }")

    def parse_entries(self) -> list:
        """Get all the entries from the `.clock` file and add them to a list.

        RETURNS: the list of LogEntries
        """

        entries: list[LogEntry] = []

        with open(self.clock_file, "r") as file:
            entry = LogEntry()
            for line_num, line in enumerate(file, 1):
                # dprint(f"{line = }")

                line = line.strip()

                if line.startswith("P_IN::"):
                    entry.p_in = line.split("::")[1]
                elif line.startswith("B_"):
                    if "IN" in line:
                        entry.breaks.append([line.split("::")[1], None])
                    elif "OUT" in line:
                        entry.breaks[-1][1] = line.split("::")[1]
                    else:
                        raise RuntimeError(
                            f"Invalid time prefix in .clock file @ {line_num}: `{line}`"
                        )
                elif line.startswith("P_OUT::"):
                    entry.p_out = line.split("::")[1]
                elif line.startswith("TIME::"):
                    continue
                elif line.startswith("#"):
                    continue
                elif line == "":
                    entries.append(entry)
                    entry = LogEntry()
                else:
                    try:
                        datetime.strptime(line, "%b %d, %Y")
                        entry.date = line
                    except:
                        raise RuntimeError(
                            f"Invalid date format in .clock file @ {line_num}: `{line}`"
                        )
            if entry.date:
                entries.append(entry)
        return entries

    def write_punch_in(self):
        now: datetime = datetime.now()
        date = datetime.strftime(now, "%b %d, %Y")
        time = datetime.strftime(now, "%H:%M")
        with open(self.clock_file, "a") as cf:
            cf.write(f"\n{date}\n  P_IN::{time}\n")
        self.focus_entry.date = date
        self.focus_entry.p_in = time

    def write_break_in(self):
        time = datetime.now().strftime("%H:%M")
        with open(self.clock_file, "a") as cf:
            cf.write(f"  B_IN::{time}\n")
        self.focus_entry.breaks.append([time, None])

    def write_break_out(self):
        time = datetime.now().strftime("%H:%M")
        with open(self.clock_file, "a") as cf:
            cf.write(f"  B_OUT::{time}\n")
        self.focus_entry.breaks[-1][1] = time

    def write_punch_out(self):
        time = datetime.now().strftime("%H:%M")
        with open(self.clock_file, "a") as cf:
            cf.write(f"  P_OUT::{time}\n")
            self.focus_entry.p_out = time
            _, _, total = self._get_total_time()
            cf.write(f"  TIME::{total:.2f}H\n")

    def check_punch_state(self) -> str:
        """IF last_entry has some data (not None) but doesn't have a
        p_out datum, then the state of the program is currently punched-in.
        """
        state: str
        if self.focus_entry and not self.focus_entry.p_out:
            state = PUNCHED_IN_STATE
        else:
            state = PUNCHED_OUT_STATE
        return state

    def check_break_state(self) -> str:
        state: str
        if (
            self.focus_entry
            and self.focus_entry.breaks
            and not self.focus_entry.breaks[-1][1]
        ):
            state = BREAK_IN_STATE
        else:
            state = BREAK_OUT_STATE
        return state

    def display_state(self):
        punch_state = self.check_punch_state()
        break_state = self.check_break_state()
        available_commands = ["in", "out", "break in", "break out", "state"]
        if punch_state == PUNCHED_IN_STATE:
            available_commands.remove("in")
            if break_state == BREAK_IN_STATE:
                available_commands.remove("break in")
                available_commands.remove("out")
            elif break_state == BREAK_OUT_STATE:
                available_commands.remove("break out")
            print(f"\nCurrent state of TimeLog is {punch_state}: {break_state}.")
            print(f"Available commmands are: {available_commands}\n")

        elif punch_state == PUNCHED_OUT_STATE:
            available_commands.remove("out")
            available_commands.remove("break in")
            available_commands.remove("break out")
            print(f"\nCurrent state of TimeLog is {punch_state}.")
            print(f"Available commmands are: {available_commands}\n")

    def display_last_clock_event(self):
        print("Time entries from last clock event:")
        if self.focus_entry.date:
            print(f"  {add_day_of_week(self.focus_entry.date)}")
        if self.focus_entry.p_in:
            print(f"  Punch In:\t{convert_24_to_12(self.focus_entry.p_in)}")
        if self.focus_entry.breaks:
            for b in self.focus_entry.breaks:
                if b[0]:
                    print(f"  Break Start:\t{convert_24_to_12(b[0])}")
                if b[1]:
                    print(f"  Break End:\t{convert_24_to_12(b[1])}")
        if self.focus_entry.p_out:
            print(f"  Punch Out:\t{convert_24_to_12(self.focus_entry.p_out)}")
        print()

    def display_total_time(self):
        assert self.focus_entry.p_out, "Can't get total if incomplete clock event."
        total, breaks, total_minus_breaks = self._get_total_time()
        print(
            f"Total ({total:.2f}H) - breaks ({breaks}m) = {total_minus_breaks:.2f}H\n"
        )

    def disply_time_until_8_hours(self):
        assert not self.focus_entry.p_out, "Shoudn't be clocked out."
        total_minus_breaks, remaining, time = self._get_time_until_8_hours()
        print(f"Total so far is {total_minus_breaks:.2f}H. {remaining} remaining.")
        if self.check_break_state() == BREAK_OUT_STATE:
            print(f"Punch out at {time} to achieve {self.work_hours} hours today.\n")
        else:
            print(
                "End your break and",
                f"punch out at {time} to achieve {self.work_hours} hours today.",
            )

    def _get_total_time(self):
        break_minutes = 0
        for b in self.focus_entry.breaks:
            assert b[0] and b[1], "All breaks should have in and out time."
            break_delta = time_as_datetime(b[1]) - time_as_datetime(b[0])
            break_minutes += break_delta.seconds // 60

        punch_delta = time_as_datetime(self.focus_entry.p_out) - time_as_datetime(
            self.focus_entry.p_in
        )
        punch_minutes = punch_delta.seconds / 60.0
        punch_hours = punch_minutes / 60.0
        return punch_hours, break_minutes, (punch_minutes - break_minutes) / 60.0

    def _get_time_until_8_hours(self):
        break_minutes = 0
        for b in self.focus_entry.breaks:
            if b[1]:
                break_delta = time_as_datetime(b[1]) - time_as_datetime(b[0])
            else:
                break_delta = datetime.now() - time_as_datetime(b[0])
            break_minutes += break_delta.seconds // 60

        punch_delta = datetime.now() - time_as_datetime(self.focus_entry.p_in)
        punch_minutes = punch_delta.seconds // 60
        hours_so_far = (punch_minutes - break_minutes) / 60.0

        minutes_remaining = int(self.work_hours * 60 - punch_minutes + break_minutes)
        time_remaining: str
        if minutes_remaining <= 60:
            time_remaining = f"{minutes_remaining}m"
        else:
            hours_remaining = minutes_remaining // 60
            time_remaining = f"{hours_remaining}H:{minutes_remaining % 60}m"
        eight_hours_time_str = (
            datetime.now() + timedelta(minutes=minutes_remaining)
        ).strftime("%I:%M%p")

        return hours_so_far, time_remaining, eight_hours_time_str
