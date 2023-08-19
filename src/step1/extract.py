import os
import pandas as pd
import shutil
import logging

from src.utils import parse_date_argument, create_db_engine

# Configure the logging system
logging.basicConfig(level=logging.INFO)


def extract_from_csv(input_date):
    """
    Extract data from a source CSV file and write to a staging area.

    Args:
        date (str, optional): Date in 'YYYY-MM-DD' format. If not provided, today's date is used.

    Returns:
        bool: True if extraction is successful, False otherwise.
    """

    try:
        # Define the path to the source CSV file
        source_file = "data/order_details.csv"

        # Define the output folder path using the input_date
        output_folder = f"data/csv/{input_date}"

        # Define the output file path using the output_folder and file name
        output_file = f"{output_folder}/order_details.csv"

        # Create the output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)

        # Copy the source file to the output file
        shutil.copyfile(source_file, output_file)

        logging.info("Data extraction from CSV successful.")

        return True

    except Exception as e:
        logging.error(f"step1.extract_from_csv failed: {str(e)}")
        return False


def extract_from_postgres(input_date):
    """
    Extract data from Postgres tables and save to appropriate folders.

    Args:
        date (str, optional): Date in 'YYYY-MM-DD' format. If not provided, today's date is used.

    Returns:
        bool: True if extraction is successful, False otherwise.
    """
    try:
        # Postgres database configuration
        db_config = {
            "host": "localhost",
            "port": "5432",
            "database": "northwind",
            "user": "northwind_user",
            "password": "thewindisblowing",
        }

        # Create an SQLAlchemy engine
        engine = create_db_engine(**db_config)

        # Get a list of all table names in the database
        with engine.connect() as connection:
            query = """
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """
            table_names = pd.read_sql(query, connection)["table_name"]

            # Iterate through each table, extract data, and save to output folder
            for table_name in table_names:
                try:
                    # Read data from the table into a DataFrame
                    query = f"SELECT * FROM {table_name}"
                    data = pd.read_sql(query, connection)

                    # Create subfolder for each table name
                    table_output_folder = os.path.join(
                        "data", "postgres", table_name, input_date
                    )
                    os.makedirs(table_output_folder, exist_ok=True)

                    # Write data to output file
                    output_file = os.path.join(
                        table_output_folder, f"{table_name}_{input_date}.csv"
                    )
                    data.to_csv(output_file, index=False)

                    logging.info(
                        f"Data extraction from Postgres table {table_name.upper()} completed successfully."
                    )

                except Exception as e:
                    logging.error(
                        f"Error extracting data from table {table_name}: {str(e)}"
                    )

        logging.info("Data extraction from Postgres completed successfully.")

        return True

    except Exception as e:
        logging.error(f"Error extracting from Postgres: {str(e)}")
        return False


def main():
    input_date = parse_date_argument()

    if extract_from_csv(input_date) and extract_from_postgres(input_date):
        logging.info("Isolated extraction process completed successfully.")
    else:
        logging.error("Isolated extraction process failed.")


if __name__ == "__main__":
    main()
