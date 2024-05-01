"""Houses the `Upload` class."""

import sys
from lib.gspread import service_account, Client, Spreadsheet, Worksheet
from constants import SERVICE_ACCT_JSON, dprint, eprint


class Upload:
    """Responsible for operations relating to uploading the `.csv` file to the
    selected google sheet.
    """

    def __init__(self):
        """Constructs an instance of `Upload`"""

        # Service account client.
        self.gc: Client = service_account(filename=SERVICE_ACCT_JSON)
        # List of available spreadsheets.
        self.spreadsheets: list[Spreadsheet] = self.gc.openall()
        # The current working spreadsheet
        self.spreadsheet: Spreadsheet = None
        self.wks: Worksheet = None
        
    def get_available_spreadsheets(self):
        # Show available spreadsheets to update.
        if self.spreadsheets:
            print("Available spreadsheets:")
            for index, wks in enumerate(self.spreadsheets):
                print(f"\n{{{index}}}\tTitle:\t{wks.title}\n\tURL:\t{wks.url}\n")
            self.spreadsheet = self.spreadsheets[self._get_wks_index()]
            self.wks = self.spreadsheet.sheet1

    def _get_wks_index(self) -> int:
        """Get which spreadsheet to update."""

        # Default spreadsheet to update is the first one in spreadsheets (list).
        i_wks_to_update: int = -1

        # For displaying spreadsheet index options:
        wks_indexes: list[int] = [i for i in range(len(self.spreadsheets))]
        while not (0 <= i_wks_to_update < len(wks_indexes)):
            try:
                i_wks_to_update = int(
                    input(
                        f"Which spreadsheet do you want to update? {tuple(wks_indexes)}"
                        "\n(Enter q to cancel.)"
                        "\n> "
                    )
                )
            except Exception as err:
                dprint(err)
                print("\nINFO:   Upload cancelled.\n")
                sys.exit(1)
        return i_wks_to_update

    def clear_wks(self):
        action = input("Are you sure you want to clear the entire worksheet? (y/n)\n>")
        if action == "y":
            try:
                self.wks.clear()
            except:
                print("")

    def append(self, values: list[str] | list[list[str]]):
        # IF just one row values[0] will be a str
        dprint(f"Appending {values}...")
        if type(values[0]) == str:
            self.wks.append_row(values, value_input_option="USER_ENTERED")
        # IF multiple rows values[0] will be a list of type str
        elif type(values[0]) == list:
            self.wks.append_rows(values, value_input_option="USER_ENTERED")

    def __repr__(self) -> str:
        """Representation of the `Upload` instance object"""
        attrs = f"spreadsheets={self.spreadsheets}, "
        attrs += f"spreadsheet={self.spreadsheet}, "
        attrs += f"wks={self.wks}"
        return f"Upload({attrs})"
