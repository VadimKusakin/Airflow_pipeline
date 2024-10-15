# Пайплайн обработки данных о продажах

Задача — создать автоматизированный пайплайн обработки и анализа данных о продажах, используя стек технологий: **PostgreSQL**, **ClickHouse**, **Apache Airflow** и **PySpark**. Пайплайн предназначен для обработки 1 миллиона записей о продажах, очистки данных, выполнения агрегаций и сохранения результатов в PostgreSQL и ClickHouse для дальнейшего анализа.

### Основные технологии

- **PostgreSQL**
- **ClickHouse**
- **Apache Airflow**
- **PySpark**
- **Docker**

### Работа пайплайна

1. **Запуск DAG**: DAG Airflow запускается в 12:45 по московскому времени каждый вторник.
2. **Генерация данных**: Пайплайн генерирует 1 миллион реалистичных записей о продажах со следующими полями:
   - `sale_id` (Уникальный идентификатор продажи)
   - `customer_id` (Идентификатор покупателя)
   - `product_id` (Идентификатор продукта)
   - `quantity` (Количество проданных товаров)
   - `sale_date` (Дата продажи)
   - `price` (Случайная цена товара)
   - `region` (Регион покупателя: Север, Юг, Восток или Запад)
3. **Очистка данных**: Проверка, что все поля данных имеют правильный формат для дальнейшей обработки.
4. **Вставка в PostgreSQL**: Очищенные данные загружаются в таблицу PostgreSQL для хранения сырых данных о продажах.
5. **Агрегация данных**: С использованием группировок рассчитываются следующие метрики:
   - Общие продажи и суммы продаж по регионам и продуктам.
   - Средняя сумма продаж (`average_sale_amount`) по регионам и продуктам.
6. **Миграция данных в ClickHouse**: Агрегированные данные мигрируются из PostgreSQL в ClickHouse с добавлением поля `import_date` для отслеживания времени импорта.

### Просмотр данных через DBeaver

После успешной загрузки данных в PostgreSQL и ClickHouse можно использовать **DBeaver** для подключения и просмотра данных.

#### Подключение к PostgreSQL:

   - **Хост**: `localhost`
   - **Порт**: `5433`
   - **База данных**: `test`
   - **Имя пользователя**: `user`
   - **Пароль**: `password`

#### Подключение к ClickHouse:

   - **Хост**: `localhost`
   - **Порт**: `8123`


## Инструкции по установке

Этот проект был разработан на Mac с процессором серии M (архитектура ARM). Он не был протестирован на других архитектурах, поэтому нет гарантии, что образ Docker и контейнеры будут корректно работать на других системах.

   ```bash
   git clone https://github.com/VadimKusakin/Airflow_pipeline.git
   cd Airflow_pipeline
   docker build -t airflow-with-java .
   docker-compose up
   ```

## Контакты
https://t.me/KusakinVadim



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



## Setup Instructions

This project was developed on a MacBook with an M-series processor (ARM architecture). It has not been tested on other architectures, so there is no guarantee that the Docker image and containers will run correctly on different systems.

   ```bash
   git clone https://github.com/VadimKusakin/Airflow_pipeline.git
   cd Airflow_pipeline
   docker build -t airflow-with-java .
   docker-compose up
   ```

## Contact
https://t.me/KusakinVadim
