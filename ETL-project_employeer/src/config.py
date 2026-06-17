import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env файл (если есть)
load_dotenv()

# Корневая папка проекта
ROOT_DIR = Path(__file__).parent

# ✅ Настройки PostgreSQL (совпадают с docker-compose.yml)
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'etl_db')
DB_USER = os.getenv('DB_USER', 'etl_user')          # ✅ Исправлено
DB_PASSWORD = os.getenv('DB_PASSWORD', 'etl_password')  # ✅ Исправлено

# Строка подключения
DATABASE_EMPLOYER_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Пути к данным
RAW_DATA_PATH = ROOT_DIR / 'data' / 'raw' / 'employees.csv'
PROCESSED_DATA_PATH = ROOT_DIR / 'data' / 'processed' / 'cleaned_employees.csv'

# Настройки трансформации
VALID_STATUSES = ['active']
MIN_SALARY = 0