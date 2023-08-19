# Northwind ETL Pipeline

This project demonstrates an ETL (Extract, Transform, Load) pipeline to extract data from various sources, transform it, and load it into a PostgreSQL database. The data is sourced from CSV files and a PostgreSQL database schema representing the Northwind database.

## Setup

1. Clone the repository.

2. Start by setting up PostgreSQL databases using Docker Compose:

```
docker-compose up
```

This will launch two PostgreSQL databases: one for the source and another one for the destination. I have chosen PostgreSQL as the destination database due to its familiarity and as a continuation of the choice made for the source database.

3. Create a virtual environment using the following commands (optional but recommended):

```
python -m venv venv
source venv/bin/activate # For Linux/Mac
venv\Scripts\activate # For Windows
```

3. Install project dependencies using the following command:

```
pip install -r requirements.txt
```

These dependencies include:

- **Pandas**: A versatile data manipulation library that facilitates efficient data handling and analysis during the ETL process.

- **SQLAlchemy**: A powerful SQL toolkit and Object-Relational Mapping (ORM) library, offering database portability to interact with various database types seamlessly.

## Running the ETL Pipeline

To run the entire ETL pipeline, use the following command:

```
python -m src.main
```

By default, the pipeline uses today's date. Provide a custom date in 'YYYY-MM-DD' format using the `--date` or `-d` flag:

```
python -m src.main --date 2023-08-01
```

To run only the **extract** part of the ETL, use:

```
python -m src.step1.extract [--date/-d]
```

To run only the **transform and load** part of the ETL, use:

```
python -m src.step2.transform_load [--date/-d]
```

## Running Final Queries

To view detailed orders, run the following command:

```
python -m src.final_query.detailed_orders
```

This command will execute a query that combines orders and their details, showing the order information along with the associated details from the provided CSV files. The data will be exported to a .csv file on data/detailed_orders.

## Output

- Extracted data is stored in CSV files under the `data` folder.
- Transformed data is loaded into the PostgreSQL database.
- Logs are generated in the project root.

## ETL Process Flowchart

![etl](https://github.com/josshartmann/de-northwind-indicium/assets/52213416/da6d3c2a-633a-463d-8fa2-ffde8663c311)

## Entity-Relationship Diagram (ERD)

The following Entity-Relationship Diagram (ERD) represents the structure of the final database, which is the result of the ETL process. This diagram was exported from PgAdmin, providing a visual overview of the relationships between different entities and their attributes.

![erd](https://github.com/josshartmann/de-northwind-indicium/assets/52213416/eab4fdfd-8c1d-4d8b-80b8-8e7372a210f2)

## Troubleshooting

- Ensure your PostgreSQL databases are properly configured in `docker-compose.yml`.
- If you encounter dependency issues, refer to `requirements.txt` for required packages.

## Acknowledgements

This project is based on the Northwind database schema.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
