class LogEntry:
    def __init__(self):
        self.date: str = ""
        self.p_in: str = ""
        self.breaks: list[list[str, str | None]] = []
        self.p_out: str = ""
    
    def __repr__(self):
        attrs = ""
        attrs += f"'{self.date}', "
        attrs += f"'{self.p_in}', "
        attrs += f"{self.breaks}, "
        attrs += f"'{self.p_out}'"
        return f"LogEntry({attrs})"
