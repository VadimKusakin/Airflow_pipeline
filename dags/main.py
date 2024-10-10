from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import csv
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import IntegerType, StringType, FloatType, DateType
import random
from datetime import datetime, timedelta
import psycopg2
from clickhouse_connect.driver import create_client
import pendulum

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
}

dag = DAG(
    'main',
    description='A simple DAG to interact with ClickHouse and PostgreSQL',
    default_args=default_args,
    catchup=False,
    start_date=datetime(2024, 1, 1, tzinfo=pendulum.timezone("Europe/Moscow")),
    schedule_interval='45 12 * * 2',
)


file_path = "data.csv"

def generate_sales_data():
    def random_date():
        return datetime.now() - timedelta(days=random.randint(0, 365))

    num_records = 100000

    with open(file_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['sale_id', 'customer_id', 'product_id', 'quantity', 'sale_date', 'price', 'region'])
        
        for i in range(num_records):
            sale_id = i+1
            customer_id = random.randint(1, 10000)
            product_id = random.randint(1, 100)
            quantity = random.randint(1, 20)
            sale_date = random_date()
            price = random.randint(10, 1000)
            region = random.choice(["North", "South", "East", "West"])
            
            writer.writerow([sale_id, customer_id, product_id, quantity, sale_date, price, region])

    print(f"{num_records} records were generated and saved in the {file_path}")

def transform_sales_data_and_load_to_PG():
    spark = SparkSession.builder \
        .appName("SalesDataGeneration") \
        .config("spark.jars", "/opt/spark/jars/postgresql-42.7.4.jar") \
        .master("local[*]") \
        .getOrCreate()
    sales_df = spark.read.csv(file_path, header=True, inferSchema=True)
    sales_df = sales_df.withColumn("sale_amount", col("quantity") * col("price"))

    sales_df = sales_df.withColumn("sale_id", col("sale_id").cast(IntegerType())) \
                       .withColumn("customer_id", col("customer_id").cast(IntegerType())) \
                       .withColumn("product_id", col("product_id").cast(IntegerType())) \
                       .withColumn("quantity", col("quantity").cast(IntegerType())) \
                       .withColumn("sale_amount", col("sale_amount").cast(FloatType())) \
                       .withColumn("sale_date", col("sale_date").cast(DateType())) \
                       .withColumn("price", col("price").cast(IntegerType())) \
                       .withColumn("region", col("region").cast(StringType()))

    sales_df.show(12)

    sales_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://host.docker.internal:5433/test") \
        .option("dbtable", "sales_data") \
        .option("user", "user") \
        .option("password", "password") \
        .option("driver", "org.postgresql.Driver") \
        .mode("overwrite") \
        .save()

    spark.stop()

pg_conn = psycopg2.connect(
        host="host.docker.internal",
        port="5433",
        database="test",
        user="user",
        password="password"
    )
cursor = pg_conn.cursor()

def aggregate_data():
    cursor.execute("""
                CREATE TABLE IF NOT EXISTS aggregated_sales_data (
                    product_id int,
                    region varchar,
                    num_of_sales int,
                    total_sum int,
                    average_sale_amount numeric(76, 2));
                
                TRUNCATE aggregated_sales_data;

                INSERT INTO aggregated_sales_data (product_id, region, num_of_sales, total_sum, average_sale_amount)
                SELECT product_id,
                    region,
                    COUNT(*),
                    SUM(sale_amount),
                    SUM(sale_amount)/COUNT(*)
                FROM sales_data
                GROUP BY (region, product_id)
                ORDER BY product_id, region;
            """)
    pg_conn.commit()

clickhouse_client = create_client(
        host='host.docker.internal',
        port=8123,
        username='',
        password=''
    )

def create_CH_table():
    clickhouse_client.command("""
                    CREATE TABLE IF NOT EXISTS aggregated_sales_data (
                        product_id Int32,
                        region String,
                        num_of_sales Int32,
                        total_sum Int32,
                        average_sale_amount Decimal(76, 2),
                        import_time DateTime DEFAULT now()
                    ) ENGINE = MergeTree()
                    ORDER BY (import_time, product_id);
                    """)

def load_data_to_CH():
    cursor.execute("SELECT * FROM aggregated_sales_data")
    rows = cursor.fetchall()

    clickhouse_client.insert('aggregated_sales_data', rows,
                                column_names=['product_id', 'region', 'num_of_sales', 'total_sum', 'average_sale_amount'])

    cursor.close()
    pg_conn.close()


task_generate_data = PythonOperator(
    task_id='generate_sales_data',
    python_callable=generate_sales_data,
    dag=dag,
)

task_transform_and_load = PythonOperator(
    task_id='transform_data_and_load_to_PG',
    python_callable=transform_sales_data_and_load_to_PG,
    dag=dag,
)

task_aggregate_data = PythonOperator(
    task_id='aggregate_data',
    python_callable=aggregate_data,
    dag=dag,
)

task_create_CH_table = PythonOperator(
    task_id='create_CH_table',
    python_callable=create_CH_table,
    dag=dag,
)

task_load_to_CH = PythonOperator(
    task_id='load_data_to_CH',
    python_callable=load_data_to_CH,
    dag=dag,
)

task_generate_data >> task_transform_and_load >> task_aggregate_data >> task_create_CH_table >> task_load_to_CH
