import os
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent.parent


DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'user': os.getenv('DB_USER', 'etl_user'),
    'password': os.getenv('DB_PASSWORD', 'etl_password'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_DATABASE', 'etl_db')
}

DATABASE_URL = f"postgresql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"


RAW_DATA_DIR = PROJECT_DIR / 'data' / 'raw' / 'sales.csv'
PROCESSED_DATA_DIR = PROJECT_DIR / 'data' / 'processed' / 'cleaned_sales.csv'

