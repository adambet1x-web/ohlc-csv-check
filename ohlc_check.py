"""Validate an OHLC CSV locally with the Python standard library."""
import argparse
import csv
import sys
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

PRICES = ("open", "high", "low", "close")
COLUMNS = ("timestamp", *PRICES)


def check(source, report):
    reader = csv.DictReader(source, strict=True)
    headers = reader.fieldnames or []
    if len(headers) != len(set(headers)) or not set(COLUMNS).issubset(headers):
        report("Expected unique headers including timestamp,open,high,low,close")
        return False

    seen = set()
    previous = None
    valid = True
    rows = 0
    for row in reader:
        rows += 1
        line = reader.line_num
        if None in row or None in row.values():
            report(f"Line {line}: wrong number of columns")
            valid = False
            continue

        try:
            timestamp = datetime.fromisoformat(row["timestamp"].strip())
            if timestamp.utcoffset() is None:
                raise ValueError
            instant = timestamp.astimezone(timezone.utc)
        except (ValueError, OverflowError):
            report(f"Line {line}: expected an ISO 8601 timestamp with timezone")
            valid = False
        else:
            if instant in seen:
                report(f"Line {line}: duplicate timestamp")
                valid = False
            elif previous is not None and instant < previous:
                report(f"Line {line}: timestamp out of order")
                valid = False
            seen.add(instant)
            previous = instant

        try:
            opening, high, low, closing = (
                Decimal(row[column].strip()) for column in PRICES
            )
            if not all(value.is_finite() for value in (opening, high, low, closing)):
                raise InvalidOperation
        except InvalidOperation:
            report(f"Line {line}: expected finite numeric OHLC values")
            valid = False
            continue
        if low > min(opening, closing) or high < max(opening, closing):
            report(f"Line {line}: prices violate low <= open/close <= high")
            valid = False

    if rows == 0:
        report("Expected at least one data row")
        return False
    return valid


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", help="path to a UTF-8 OHLC CSV")
    args = parser.parse_args()
    try:
        with open(args.csv_file, encoding="utf-8-sig", newline="") as source:
            valid = check(source, lambda message: print(message, file=sys.stderr))
    except (OSError, UnicodeError, csv.Error) as error:
        print(f"Unable to read CSV ({type(error).__name__})", file=sys.stderr)
        return 2
    if valid:
        print("OHLC CSV passed validation")
    return 0 if valid else 1


if __name__ == "__main__":
    sys.exit(main())
