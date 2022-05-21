from typing import Iterable
from enum import Enum, auto


class RowStates(Enum):
    UNQUOTED_FIELD = auto()
    QUOTED_FIELD = auto()
    QUOTED_QUOTE = auto()


class Reader:
    """
    
    """

    def __init__(self, csv_file: Iterable[str]):
        """
        """
        self.csv_file = csv_file
        self._init_header()

    def _init_header(self) -> None:
        """
        """
        try:
            first_line = next(self.csv_file)
            self._header = self._parse_line(first_line)
        except StopIteration:
            raise Exception("file is empty")

    def __iter__(self):
        """
        """
        return self
    
    def __next__(self):
        """
        """
        while True:
            line = next(self.csv_file).strip()
            line_values = self._parse_line(line)
            if len(line_values) == len(self._header):
                break

        # remove leading and trailing whitespace from fields
        line_values = list(map(lambda s: s.strip(), line_values))

        return dict(zip(self._header, line_values))
        
    def _parse_line(self, line: str) -> None:
        """
        """
        values = [""]
        state = RowStates.UNQUOTED_FIELD
        for c in line:
            if state == RowStates.UNQUOTED_FIELD:
                if c == ',':
                    values.append("")
                elif c == '"':
                    state = RowStates.QUOTED_FIELD
                else:
                    values[-1] += c
            elif state == RowStates.QUOTED_FIELD:
                if c == '"':
                    state = RowStates.QUOTED_QUOTE
                else:
                    values[-1] += c
            elif state == RowStates.QUOTED_QUOTE:
                if c == ',':
                    values.append("")
                    state = RowStates.UNQUOTED_FIELD
                elif c == '"':
                    values[-1] += '"'
                    state = RowStates.QUOTED_FIELD
                else:
                    state = RowStates.UNQUOTED_FIELD
        return values