import logging
import os
from sqlalchemy import text


def reset_database(dest_engine):
    """
    Drop existing tables and create new ones in the destination PostgreSQL database.

    Args:
        dest_engine: SQLAlchemy database engine for the destination database.
    """
    try:
        # Drop existing tables
        with open(os.path.join("queries", "drop_tables.sql"), "r") as f:
            drop_tables_query = f.read()
        with dest_engine.begin() as conn:
            conn.execute(text(drop_tables_query))

        logging.info("Dropped existing tables.")

        # Create new tables
        with open(os.path.join("queries", "create_tables.sql"), "r") as f:
            create_tables_query = f.read()
        with dest_engine.begin() as conn:
            conn.execute(text(create_tables_query))

        logging.info("Created new tables.")

    except Exception as e:
        logging.error(f"Error resetting database: {str(e)}")


def add_constraints(dest_engine):
    """
    Add constraints to the destination PostgreSQL database.
    """
    try:
        # Read the SQL statements from the "add_constraints.sql" file
        with open(os.path.join("queries", "add_constraints.sql"), "r") as f:
            sql_statements = f.read()

        # Execute all the SQL statements in a single transaction
        with dest_engine.begin() as connection:
            connection.execute(text(sql_statements))

        # Log success message if the constraints are added successfully
        logging.info("Constraints added successfully.")

    except Exception as e:
        logging.error(f"Error adding constraints to PostgreSQL: {str(e)}")
