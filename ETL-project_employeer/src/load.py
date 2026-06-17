import sys
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import logging

from config import DATABASE_EMPLOYER_URL

# Убираем лишний импорт: from sympy.core.random import rng

logging.basicConfig(level=logging.INFO)

def create_tables(engine, table_name: str = 'employees'):
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        employee_id INTEGER PRIMARY KEY,
        full_name VARCHAR(255),
        department VARCHAR(50),
        salary FLOAT,
        hire_date DATE,
        status VARCHAR(50),
        performance_rating FLOAT,
        annual_bonus FLOAT,
        etl_processed_at TIMESTAMP
    );
    """

    try:
        with engine.connect() as conn:
            conn.execute(text(create_table_query))
            conn.commit()
            logging.info("✅ Table 'employees' created/checked")
    except SQLAlchemyError as e:
        logging.error(f"Error creating table: {e}")
        raise

def load_data(df: pd.DataFrame, table_name: str = 'employees'):
    logging.info(f"Loading data into {table_name}")

    if df.empty:
        error_msg = "Data is empty"
        logging.error(error_msg)
        raise ValueError(error_msg)

    try:
        engine = create_engine(DATABASE_EMPLOYER_URL)
        logging.info("✅ Connected to database")

        create_tables(engine, table_name)

        df.to_sql(table_name, engine, index=False, if_exists='replace', chunksize=10000)
        logging.info('✅ Data loaded successfully')

        with engine.connect() as conn:
            result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
            count = result.scalar()
            logging.info(f"Total rows in table: {count}")

        stats_query = f"""
            SELECT 
                department,
                COUNT(*) as employee_count,
                ROUND(AVG(salary)::numeric, 2) as avg_salary,
                ROUND(SUM(annual_bonus)::numeric, 2) as total_bonus,
                ROUND(AVG(performance_rating)::numeric, 2) as avg_rating
            FROM {table_name}
            GROUP BY department
            ORDER BY avg_salary DESC
        """
        stats_df = pd.read_sql(stats_query, con=engine)
        logging.info(f"📊 Statistics by department:\n{stats_df.to_string(index=False)}")

    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        raise
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise

if __name__ == '__main__':
    try:
        script_dir = Path(__file__).parent.parent
        clean_data_path = script_dir / 'data' / 'employees_processed' / 'cleaned_employees.csv'

        if not clean_data_path.exists():
            error_msg = f"File not found: {clean_data_path}"
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

        df = pd.read_csv(clean_data_path)
        logging.info(f"✅ Loaded {len(df)} rows from CSV")

        load_data(df)

        print("\n" + "="*50)
        print("✅ ETL PIPELINE COMPLETED SUCCESSFULLY!")
        print(f"📊 Processed: {len(df)} rows")
        print("📁 Data loaded to PostgreSQL")
        print("="*50)

    except FileNotFoundError as e:
        logging.error(f"File error: {e}")
        print(f"\n❌ Error: {e}")
        print("💡 First run: python src/transform.py")
    except SQLAlchemyError as e:
        logging.error(f"Database error: {e}")
        print(f"\n❌ Database error: {e}")
        print("💡 Check PostgreSQL: docker-compose up -d")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        print(f"\n❌ Error: {e}")