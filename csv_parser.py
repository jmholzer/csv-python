from typing import Iterable
from enum import Enum, auto


class RowStates(Enum):
    UNQUOTED_FIELD = auto()
    QUOTED_FIELD = auto()
    QUOTED_QUOTE = auto()


class Reader:
    """
    
    """

    def __init__(self, input_file: Iterable[str]):
        """

        """
        self.input_file = input_file
        self.header = self._init_header()

    def _init_header(self) -> None:
        """
        
        """
        try:
            first_line = next(self.input_file)
            return self._parse_line(first_line)
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
            line_values = self._parse_line(next(self.input_file))
            if len(line_values) == len(self.header):
                break

        return dict(zip(self.header, line_values))
        
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

        # Remove trailing and leading whitespace from parsed values
        values[:] = map(lambda s: s.strip(), values)
        return values