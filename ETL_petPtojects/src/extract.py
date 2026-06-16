import pandas as pd
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)


def extract_data(file_path: str) -> pd.DataFrame:
    logging.info(f'Загрузка данных {file_path}')

    try:
        # Проверяем, существует ли файл
        if not Path(file_path).exists():
            raise FileNotFoundError(f'File not found: {file_path}')

        # Читаем CSV
        df = pd.read_csv(file_path)

        logging.info(f'Загружено {len(df)} строк, {len(df.columns)} колонок')
        logging.info(f'Колонки: {list(df.columns)}')
        logging.info(f'Пропуски: {df.isna().sum().sum()}')
        return df

    except FileNotFoundError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        raise


if __name__ == '__main__':
    script_dir = Path(__file__).parent.parent
    file_path = script_dir / 'data' / 'raw' / 'sales.csv'
    df = extract_data(str(file_path))
    print('\n📊 Данные:')
    print(df.head())