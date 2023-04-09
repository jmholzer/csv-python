import unittest
from pathlib import Path

from csv_fsm import Writer

RESOURCES_PATH = Path(__file__).parent / "resources"


class TestWriter(unittest.TestCase):
    """
    Tests for the Reader class defined in csv_reader.py.
    """

    def setUp(self) -> None:
        """
        Open a file with test data before each test is run.
        """
        self.test_file = open(RESOURCES_PATH / "test.csv", "r")

    def tearDown(self) -> None:
        """
        Close the open test date file after each test is run.
        """
        self.test_file.close()

    def test_writing(self) -> None:
        """
        Assert that header initialisation is performed correctly.
        """
        with open(RESOURCES_PATH / "test.csv", "r") as expected_file:
            expected = expected_file.read()

        header = ["header1", "header2", "header,3", '"header4""']
        with open("temp.csv", "w+") as test_file:
            self.writer = Writer(test_file, header)
            self.writer.write_row(
                {
                    "header1": "value1",
                    "header2": "value2",
                    "header,3": "value3",
                    '"header4""': "value4",
                }
            )
            self.writer.write_row(
                {
                    "header1": "value5",
                    "header2": "value6",
                    "header,3": "value,7",
                    '"header4""': '""value8""',
                }
            )
            self.writer.write_row(
                {"header1": "", "header2": "", "header,3": "", '"header4""': ""}
            )
            self.writer.write_row(
                {"header1": "value9", "header2": "", "header,3": "", '"header4""': ""}
            )
            self.writer.write_row(
                {
                    "header1": "value10",
                    "header2": "value11",
                    "header,3": "value12",
                    '"header4""': "value 14",
                }
            )

        with open("temp.csv", "r") as test_file:
            result = test_file.read()

        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()
