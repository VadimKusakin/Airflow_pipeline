# Sales Data Pipeline

This project implements an automated pipeline for generating, processing, analyzing, and migrating sales data using a combination of **PostgreSQL**, **ClickHouse**, **Apache Airflow**, and **PySpark**. The pipeline is designed to handle 1 million sales records, clean the data, perform aggregations, and store the results in both PostgreSQL and ClickHouse for further analysis.


### Key Technologies

- **PostgreSQL**: Used for storing raw and processed sales data.
- **ClickHouse**: Used for storing aggregated data for fast analytical queries.
- **Apache Airflow**: Orchestrates the pipeline, schedules and automates tasks.
- **PySpark**: Used for large-scale data processing, cleaning, and analysis.
- **Docker**: Manages the multi-service architecture, including adding PySpark to the Airflow container.

### Pipeline Workflow

1. **DAG Execution**: The Airflow DAG starts at 12:45 Moscow time every Tuesday.
2. **Data Generation**: The pipeline generates 1 million realistic sales records with the following fields:
   - `sale_id` (Unique sale identifier)
   - `customer_id` (Customer identifier)
   - `product_id` (Product identifier)
   - `quantity` (Number of products sold)
   - `sale_date` (Date of the sale)
   - `price` (Random product price)
   - `region` (Customer's region: North, South, East, or West)
3. **Data Cleaning**: The pipeline ensures all data fields are in the correct format for further processing.
4. **PostgreSQL Insertion**: Cleaned data is loaded into a PostgreSQL table for raw sales data.
5. **Data Aggregation**: Using window functions and groupings, the following metrics are calculated:
   - Total sales and sales amounts per region and product.
   - Average sale amount (`average_sale_amount`) per region and product.
6. **Data Migration to ClickHouse**: Aggregated data is migrated from PostgreSQL to ClickHouse, with an additional `import_date` field to track the import time.

### Viewing Data via DBeaver

After the data has been successfully loaded into PostgreSQL and ClickHouse, you can use **DBeaver** to connect and view the data.

#### Connecting to PostgreSQL:

   - **Host**: `localhost`
   - **Port**: `5433`
   - **Database**: `test`
   - **Username**: `user`
   - **Password**: `password`

#### Connecting to ClickHouse:

   - **Host**: `localhost`
   - **Port**: `8123`

![image](https://github.com/user-attachments/assets/43a43e30-2324-4d09-a5e5-b002d2f48b01)
![image](https://github.com/user-attachments/assets/11e0fb42-6c6e-4334-a688-bcd111fd68f7)
![image](https://github.com/user-attachments/assets/058d690f-2a58-4fe3-afe0-9513ca6d6c4d)


## Setup Instructions

This project was developed on a MacBook with an M-series processor (ARM architecture). It has not been tested on other architectures, so there is no guarantee that the Docker image and containers will run correctly on different systems.

   ```bash
   git clone https://github.com/VadimKusakin/Airflow_pipeline.git
   cd Airflow_pipeline
   docker build -t airflow-with-java .
   docker-compose up
   ```

# Contact
https://t.me/KusakinVadim

For any questions or issues regarding the project, feel free to contact the repository owner.
