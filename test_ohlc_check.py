import io
import unittest

from ohlc_check import check

HEADER = "timestamp,open,high,low,close\n"
FIRST = "2026-01-01T09:00:00Z,10,11,9,10\n"


class CheckTests(unittest.TestCase):
    def test_valid_file_with_extra_column(self):
        source = HEADER.strip() + ",volume\n" + FIRST.strip() + ",3\n"
        self.assertTrue(check(io.StringIO(source), self.fail))

    def test_invalid_rows(self):
        cases = {
            "duplicate timestamp": "2026-01-01T12:00:00+03:00,10,11,9,10\n",
            "timestamp out of order": "2026-01-01T08:00:00Z,10,11,9,10\n",
            "with timezone": "2026-01-01T09:05:00,10,11,9,10\n",
            "finite numeric": "2026-01-01T09:05:00Z,NaN,11,9,10\n",
            "prices violate": "2026-01-01T09:05:00Z,12,11,9,10\n",
            "wrong number": "2026-01-01T09:05:00Z,10,11,9\n",
        }
        for expected, row in cases.items():
            with self.subTest(expected=expected):
                messages = []
                self.assertFalse(check(io.StringIO(HEADER + FIRST + row), messages.append))
                self.assertEqual(len(messages), 1)
                self.assertIn(expected, messages[0])

    def test_missing_data_or_columns(self):
        for source in (HEADER, "", "timestamp,close\n"):
            with self.subTest(source=source):
                messages = []
                self.assertFalse(check(io.StringIO(source), messages.append))
                self.assertEqual(len(messages), 1)


if __name__ == "__main__":
    unittest.main()
