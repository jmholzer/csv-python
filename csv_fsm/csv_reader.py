from typing import Iterable, List
from enum import Enum, auto


class RowStates(Enum):
    """
    A class to contain the states of the finite-state machine used to parse
    lines of CSV input in Reader (see Reader._parse_line).
    Attributes:
        UNQUOTED_FIELD -- the current position is unquoted.
        QUOTED_FIELD -- the current position is quoted.
        QUOTED_QUOTE -- the current position is a quoted quote.
    """
    UNQUOTED_FIELD = auto()
    QUOTED_FIELD = auto()
    QUOTED_QUOTE = auto()


class Reader:
    """
    A class to read a CSV file using a finite-state machine approach to handle
    commas and quotes embedded in field values. CSV files are assumed to use ','
    as a separator, and '"' as quotes. Commas enclosed in quotes are parsed as
    part of the value. Quotes enclosed in quotes are parsed as part of the value.

    Attributes:
        _input_file -- the file object to read from.
        header -- an in-order list of the column names of the input file.

    Methods:
        __init__
        _init_header
        __iter__
        __next__
        _parse_line
    """

    def __init__(self, input_file: Iterable[str]):
        """Initialise an object of the Reader class.

        Args:
            input_file -- the file object to read from.
        """
        self._input_file = input_file
        self.header = self._init_header()

    def _init_header(self) -> List[str]:
        """Read the header of the input file, if there is no first line, raise an exception
        that an empty file was given as input.
        """
        try:
            first_line = next(self._input_file)
            return self._parse_line(first_line)
        except StopIteration:
            raise Exception("file is empty")

    def __iter__(self):
        """Make the class iterable."""
        return self

    def __next__(self):
        """Return the result of parsing the next valid line in the input file.
        A line is considered to be invalid if it does not contain the same
        number of fields as column names in the header.
        """
        while True:
            line_values = self._parse_line(next(self._input_file))
            if len(line_values) == len(self.header):
                break

        return dict(zip(self.header, line_values))

    def _parse_line(self, line: str) -> List[str]:
        """Transform a line of the input file into a list of values separated by commas using
        a finite-state machine approach.

        Args:
            line: the line of the input file to transform into a list of values.

        Returns:
            A list of strings representing the values in the line.
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
