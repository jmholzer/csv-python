import unittest
from csv_parser import Reader


class TestReader(unittest.TestCase):
    """
    
    """
    def setUp(self) -> None:
        self.test_file = open("resources/test.csv", "r")
        self.reader = Reader(self.test_file)

    def tearDown(self) -> None:
        self.test_file.close()

    def test_empty_file(self) -> None:
        """
        
        """
        with open("test_csv_parser/empty.csv", "r") as empty_file:
            with self.assertRaises(Exception):
                self.reader = Reader(empty_file)

    def test_init_header(self) -> None:
        """

        """
        expected = ['header1','header2','header,3','"header4""']
        result = self.reader._header
        self.assertEqual(expected, result)

    def test_next(self) -> None:
        """
        
        """
        expected = {
            "header1": "value1",
            "header2": "value2",
            "header,3": "value3",
            "\"header4\"\"": "value4"
        }
        result = next(self.reader)
        self.assertEqual(expected, result)

    def test_parse_line(self) -> None:
        """
        
        """
        expected = [
            ["value1","value2","value3","value4"],
            ["value5","value6","value,7","\"value8\""],
            [""],
            ["value9","","",""],
            ["value10","value11","value12","value 14"] 
        ]
        result = [self.reader._parse_line(line.strip()) for line in self.test_file]
        pprint(result)
        self.assertEqual(expected, result)


if __name__ == "__main__":
    unittest.main()