import pandas as pd
import logging
from pathlib import Path
from extract import extract_data



logging.basicConfig(level=logging.INFO)

def transform(df: pd.DataFrame) -> pd.DataFrame:
    logging.info('Трансформация данных')

    df_clean = df.copy()
    # ✅ ВАЖНО: Убираем пробелы в названиях колонок!
    df_clean.columns = df_clean.columns.str.strip()
    logging.info(f'Колонки после очистки: {list(df_clean.columns)}')

    # ✅ Также чистим значения в статусах (на всякий случай)
    df_clean['status'] = df_clean['status'].str.strip()

    inital_count = len(df_clean)
    df_clean = df_clean.drop_duplicates(subset=['order_id'])
    logging.info(f'Дубликаты удлаены {inital_count - len(df_clean)}')

    df_clean['customer_name'] = df_clean['customer_name'].fillna('Unknown customer')
    logging.info('Заполнены пропуски колоник customer_name')

    quantity_min = len(df_clean)
    df_clean = df_clean[df_clean['quantity'] > 0]
    logging.info(f'Удалены quantity которые отрицательны {quantity_min - len(df_clean)}')

    price_min = len(df_clean)
    df_clean = df_clean[df_clean['price'] > 0]
    logging.info(f'Удалены price которые отрицательны {price_min - len(df_clean)}')

    df_clean['order_date'] = pd.to_datetime(df_clean['order_date'])
    logging.info('Превраитил order_date в тип Date')

    value_sort = ['completed', 'pending']
    status_correct = len(df_clean)
    df_clean = df_clean[df_clean['status'].isin(value_sort)]
    logging.info(f'Удалены неккоректные операции {status_correct - len(df_clean)}')

    df_clean['total_amount'] = df_clean['quantity'] * df_clean['price']
    df_clean = df_clean.sort_values('order_date')

    logging.info(f'Итог после трансформации {len(df_clean)} строк')

    if len(df_clean) > 0:
        logging.info(f'Общая сумма заказов {df_clean['total_amount'].sum():.2f}')
        logging.info(f'Средний чек {df_clean['total_amount'].mean():.2f}')
        logging.info(f'Максимальный чек {df_clean['total_amount'].max():.2f}')

    return df_clean


def save_df(df: pd.DataFrame, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)
    logging.info(f'Очищенные данные {path}')


if __name__ == '__main__':
    script_dir = Path(__file__).parent.parent
    input_path = script_dir / 'data' / 'raw' / 'sales.csv'
    output_path = script_dir / 'data' / 'processed' / 'cleaned_sales.csv'
    df = extract_data(str(input_path))
    df_clean = transform(df)
    save_df(df_clean, str(output_path))

    print(df_clean.head())





















