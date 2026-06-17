import pandas as pd
from pathlib import Path
import logging
from datetime import datetime

from extract import extract_employ


logging.basicConfig(level=logging.INFO)

def transform_employees(df: pd.DataFrame) -> pd.DataFrame:
    logging.info('Transforming employees data')

    df_clean = df.copy()
    df_clean.columns = df_clean.columns.str.strip()
    df_clean['status'] = df_clean['status'].str.strip()

    empl_dupl = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset='employee_id')
    logging.info(f'Duplicate employee ids: {empl_dupl - len(df_clean)}')

    salary_count = len(df_clean)
    df_clean = df_clean[df_clean['salary'] > 0]
    logging.info(f'Salary count: {salary_count - len(df_clean)}')


    status_count = len(df_clean)
    df_clean = df_clean[df_clean['status'] == 'active']
    logging.info(f'Status count: {status_count - len(df_clean)}')


    df_clean['annual_bonus'] = df_clean['salary'] * 0.10
    logging.info(f'Annual bonus count')
    df_clean['hire_date'] = pd.to_datetime(df_clean['hire_date'])

    df_clean['etl_processed_at'] = datetime.now()

    return df_clean
def save_data(df: pd.DataFrame) -> None:
    Path(output).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output, index=False)
    logging.info(f'Data saved to {output}')


if __name__ == '__main__':
    script_path = Path(__file__).parent.parent
    input_path = script_path / 'data' / 'raw' / 'employees.csv'
    output = script_path / 'data' / 'employees_processed' / 'cleaned_employees.csv'
    df = pd.read_csv(input_path)
    df_clean = transform_employees(df)
    save_data(df_clean)
