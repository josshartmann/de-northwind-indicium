import logging
import os
import pandas as pd
from src.utils import create_db_engine


# Configure the logging system
logging.basicConfig(level=logging.INFO)


def join_orders_and_order_details_to_csv():
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

        # Read query from file
        with open(os.path.join("queries", "final_query.sql"), "r") as f:
            query = f.read()

        # Execute the query and fetch the result into a pandas DataFrame
        result_df = pd.read_sql(query, dest_engine)

        # Create subfolder
        table_output_folder = os.path.join("data", "detailed_orders")
        os.makedirs(table_output_folder, exist_ok=True)

        # Write data to output file
        output_file = os.path.join(table_output_folder, f"detailed_orders.csv")

        # Export the DataFrame to a CSV file
        result_df.to_csv(output_file, index=False)

        logging.info(f"Joined data exported to a .csv file on {table_output_folder}")

    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    join_orders_and_order_details_to_csv()
