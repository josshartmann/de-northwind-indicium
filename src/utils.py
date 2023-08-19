import argparse
from datetime import datetime
from sqlalchemy import create_engine


def parse_date_argument():
    """
    Parses the command line argument for the date.

    Returns:
        str: The date in 'YYYY-MM-DD' format.
    """
    # Set up the argument parser
    parser = argparse.ArgumentParser()

    # Add an argument for the date in 'YYYY-MM-DD' format
    parser.add_argument(
        "--date",
        "-d",
        nargs="?",
        default=datetime.today().strftime("%Y-%m-%d"),
        help="Date in 'YYYY-MM-DD' format. If not provided, today's date is used.",
    )

    # Parse the command line arguments
    args = parser.parse_args()

    # Validate the input date format
    try:
        datetime.strptime(args.date, "%Y-%m-%d")
    except ValueError:
        exit("Invalid date. Please use 'YYYY-MM-DD' format and an existing date.")

    return args.date


def create_db_engine(host, port, database, user, password):
    """
    Create and return an SQLAlchemy engine for the specified database.

    Args:
        host (str): Database host.
        port (str): Database port.
        database (str): Database name.
        user (str): Database user.
        password (str): Database password.

    Returns:
        sqlalchemy.engine.Engine: An SQLAlchemy engine instance.
    """
    engine = create_engine(f"postgresql://{user}:{password}@{host}:{port}/{database}")

    return engine
