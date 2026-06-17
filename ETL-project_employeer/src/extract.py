import pandas as pd
import logging
from pathlib import Path


logging.basicConfig(level=logging.INFO)

def extract_employ(file_path: str) -> pd.DataFrame:
    logging.info('Data load')
    try:
        if not Path(file_path).exists():
            raise FileExistsError(f'File not found {file_path}')
        df = pd.read_csv(file_path)
        logging.info(f'Len {len(df)} rows, {len(df.columns)} columns')
        logging.info(f'Колоник {list(df.columns)}')
        logging.info(f'Пропуски: {df.isnull().sum().sum()}')
        return df
    except FileNotFoundError as e:
        logging.error(e)
        raise
    except Exception as e:
        logging.error(e)
        raise
if __name__ == '__main__':
    script_dir = Path(__file__).parent.parent
    file_path = script_dir / 'data' / 'raw' / 'employees.csv'
    df = extract_employ(str(file_path))
    print(df.head())
