import unittest
from pathlib import Path

from csv_fsm import Reader

RESOURCES_PATH = Path(__file__).parent / "resources"


class TestReader(unittest.TestCase):
    """
    Tests for the Reader class defined in csv_reader.py.
    """

    def setUp(self) -> None:
        """
        Open a file with test data before each test is run.
        """
        self.test_file = open(RESOURCES_PATH / "test.csv", "r")
        self.reader = Reader(self.test_file)

    def tearDown(self) -> None:
        """
        Close the open test date file after each test is run.
        """
        self.test_file.close()

    def test_empty_file(self) -> None:
        """
        Assert that giving an empty file as input raises an exception.
        """
        with open(RESOURCES_PATH / "empty.csv", "r") as empty_file:
            with self.assertRaises(Exception):
                self.reader = Reader(empty_file)

    def test_init_header(self) -> None:
        """
        Assert that header initialisation is performed correctly.
        """
        expected = ["header1", "header2", "header,3", '"header4""']
        result = self.reader.header
        self.assertEqual(expected, result)

    def test_next(self) -> None:
        """
        Assert that the next valid line in the input file is parsed.
        """
        expected = {
            "header1": "value1",
            "header2": "value2",
            "header,3": "value3",
            '"header4""': "value4",
        }
        result = next(self.reader)
        self.assertEqual(expected, result)

    def test_parse_line(self) -> None:
        """
        Assert that CSV lines are being parsed correctly.
        """
        expected = [
            ["value1", "value2", "value3", "value4"],
            ["value5", "value6", "value,7", '"value8"'],
            [""],
            ["value9", "", "", ""],
            ["value10", "value11", "value12", "value 14"],
        ]
        result = [self.reader._parse_line(line.strip()) for line in self.test_file]
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
