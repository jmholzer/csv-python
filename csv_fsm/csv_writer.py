import re
from typing import Dict, List, TextIO


class Writer:
    """
    A class to write CSV files, using a header containing column names
    (as a list) and rows (as dictionaries of column name / value pairs).

    Writer writes the header to the output file when initialised, and writes
    rows to the output file when the write_row method is called.

    Attributes:
        _output_file -- the file object to write the result to.
        _header -- a list containing column names in order.

    Methods:
        __init__
        _write_header
        write_row
        _format_field
    """

    def __init__(self, output_file: TextIO, header: List[str]) -> None:
        """
        Initialise an object of the Writer class.

        Arguments:
            output_file -- the file object to write to.
            header -- a list containing the column names of the output
                CSV file in order.
        """
        self._output_file = output_file
        self._header = header
        self._write_header()

    def _write_header(self):
        """
        Write the header of the csv file to the output file.
        """
        header = [self._format_field(col_name) for col_name in self._header]
        header = ",".join(header) + "\n"
        self._output_file.write(header)

    def write_row(self, row: Dict[str, str]) -> None:
        """
        Write a row to the output file.

        Arguments:
            row -- the row to write represented as a dictionary.
        """
        line = (
            ",".join([self._format_field(row[col_name]) for col_name in self._header])
            + "\n"
        )
        self._output_file.write(line)

    def _format_field(self, field: str) -> str:
        """
        Formats a given field for writing. If it contains a comma, the entire
        field is encapsulated in double quotes. If it contains double quotes, entire
        contiguous blocks of quotes are encapsulated in double quotes.

        Arguments:
            field -- the field to format for writing.
        """
        if type(field) != str:
            return field
        field = re.sub(r"(\"+)", r'"\1"', field)
        if "," in field:
            field = '"' + field + '"'
        return field
