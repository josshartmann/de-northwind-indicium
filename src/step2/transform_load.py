import os
import logging
import pandas as pd

from .utils import reset_database, add_constraints
from src.utils import parse_date_argument, create_db_engine


# Configure the logging system
logging.basicConfig(level=logging.INFO)


def load_to_postgres(input_date):
    """
    Load data from CSV files to a destination PostgreSQL database.

    Args:
        date (str, optional): Date in 'YYYY-MM-DD' format. If not provided, today's date is used.

    Returns:
        None
    """
    try:
        # Establish a connection to the destination PostgreSQL database
        dest_db_config = {
            "host": "localhost",
            "port": "5433",
            "database": "destination_db",
            "user": "destination_user",
            "password": "destination_password",
        }
        dest_engine = create_db_engine(**dest_db_config)

        # Drop existing tables and create new ones in the destination PostgreSQL database.
        reset_database(dest_engine)

        # List of table names to load
        table_names = [
            "categories",
            "customer_customer_demo",
            "customer_demographics",
            "customers",
            "employee_territories",
            "employees",
            "orders",
            "order_details",
            "products",
            "region",
            "shippers",
            "suppliers",
            "territories",
            "us_states",
        ]

        for table_name in table_names:
            try:
                # Special case for 'order_details.csv'
                if table_name == "order_details":
                    input_folder = f"data/csv/{input_date}"
                    input_file = os.path.join(input_folder, "order_details.csv")
                else:
                    input_folder = f"data/postgres/{table_name}/{input_date}"
                    input_file = os.path.join(
                        input_folder, f"{table_name}_{input_date}.csv"
                    )

                # Read data from the CSV file
                df = pd.read_csv(input_file)

                # Load data into the destination PostgreSQL database using pandas and SQLAlchemy
                with dest_engine.begin() as conn:
                    df.to_sql(table_name, conn, if_exists="append", index=False)

                logging.info(f"Data loaded successfully for table {table_name}")

            except FileNotFoundError:
                logging.error(
                    f"Error loading data for table {table_name}: No data found for {input_date}."
                )

        # Add constraints to the destination PostgreSQL database
        add_constraints(dest_engine)

    except Exception as e:
        logging.error(f"Error loading data to PostgreSQL: {str(e)}")


def main():
    input_date = parse_date_argument()

    if load_to_postgres(input_date):
        logging.info("Isolated loading process completed successfully.")
    else:
        logging.error("Isolated loading process failed.")


if __name__ == "__main__":
    main()
