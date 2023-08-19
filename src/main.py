import sys
from src.step1.extract import extract_from_csv, extract_from_postgres
from src.step2.transform_load import load_to_postgres

import logging

from src.utils import parse_date_argument

# Configure the logging system
logging.basicConfig(level=logging.INFO)


def main():
    """
    Main function to execute the ETL process.

    Usage:
        python -m src.main [--date/-d]

    Args:
        date (str, optional): Date in 'YYYY-MM-DD' format. If not provided, today's date is used.

    Returns:
        None
    """
    input_date = parse_date_argument()

    # Extract data from CSV and Postgres sources for the input date
    if not extract_from_csv(input_date) or not extract_from_postgres(input_date):
        sys.exit("Extraction failed. Please check step1.py and try again.")

    # Load the extracted data into Postgres for the input date
    load_to_postgres(input_date)


if __name__ == "__main__":
    main()
