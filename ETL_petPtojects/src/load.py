import os
import sys
from pathlib import Path  # ❌ БЫЛО ПРОПУЩЕНО!

import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from config import DATABASE_URL
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Добавляем путь для импорта config
sys.path.append(str(Path(__file__).parent.parent))


def create_table_if_not_exists(engine, table_name: str = 'sales'):
    """
    Создает таблицу, если она не существует.
    """
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        order_id INTEGER PRIMARY KEY,
        customer_name VARCHAR(255),  -- ❌ БЫЛО: customer_id VARCHAR(255, (пропущена скобка!)
        product VARCHAR(100),
        quantity INTEGER,
        price DECIMAL(10, 2),
        order_date DATE,
        status VARCHAR(50),
        total_amount DECIMAL(10, 2),
        etl_processed_at TIMESTAMP
    );
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(create_table_query))  # ❌ БЫЛО: conn.excute (опечатка!)
            conn.commit()
        logging.info("✅ Таблица создана/проверена")
    except SQLAlchemyError as e:
        logging.error(f"Ошибка создания таблицы: {e}")
        raise


def load_data(df: pd.DataFrame, table_name: str = 'sales'):
    """
    Загружает данные в PostgreSQL.
    """
    logging.info(f"Начинаю загрузку данных в таблицу '{table_name}'")

    # Проверяем, что данные не пустые
    if df.empty:
        error_msg = "DataFrame пустой, загрузка невозможна"
        logging.error(error_msg)
        raise ValueError(error_msg)  # ❌ БЫЛО: raise Exception (лучше использовать конкретный тип)

    try:
        # Создаем подключение
        engine = create_engine(DATABASE_URL)
        logging.info(f"Подключение к БД: {DATABASE_URL}")

        # Создаем таблицу
        create_table_if_not_exists(engine, table_name)  # ❌ БЫЛО: create_tables_if_not_exist (неправильное имя)

        # Загружаем данные
        df.to_sql(
            table_name,
            engine,
            index=False,
            if_exists='replace',
            chunksize=100,
            method='multi'
        )
        logging.info("Данные успешно загружены")

        # Проверяем количество загруженных строк
        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            logging.info(f"✅ Загружено {count} записей в таблицу '{table_name}'")

        # Статистика по загруженным данным
        stats_query = f"""
            SELECT 
                COUNT(*) as total_orders,
                SUM(total_amount) as total_revenue,
                AVG(total_amount) as avg_order_value,
                MIN(total_amount) as min_order_value,
                MAX(total_amount) as max_order_value
            FROM {table_name}
        """

        stats_df = pd.read_sql(stats_query, con=engine)
        logging.info(f"📊 Статистика:\n{stats_df.to_string(index=False)}")

    except SQLAlchemyError as e:
        logging.error(f"Ошибка базы данных: {e}")
        raise
    except Exception as e:
        logging.error(f"Неожиданная ошибка: {e}")
        raise


if __name__ == "__main__":
    try:
        # Путь к очищенным данным
        clean_data_path = Path(__file__).parent.parent / 'data' / 'processed' / 'cleaned_sales.csv'

        # Проверяем, существует ли файл
        if not clean_data_path.exists():
            raise FileNotFoundError(f"Файл не найден: {clean_data_path}")

        # Загружаем данные
        df = pd.read_csv(clean_data_path)
        logging.info(f"Загружено {len(df)} строк для вставки")

        # Загружаем в БД
        load_data(df)  # ❌ БЫЛО: load_data (функция называется load_data, а не load_data? У вас в коде load_data)

        print("\n✅ Загрузка успешно завершена!")

    except FileNotFoundError as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Сначала запустите transform.py для создания cleaned_sales.csv")
    except Exception as e:
        print(f"❌ Ошибка: {e}")