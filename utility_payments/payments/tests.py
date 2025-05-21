import pandas as pd
import sqlite3
from datetime import datetime

# Настройки
EXCEL_FILE = 'показания.xlsx'
SQLITE_DB = 'db.sqlite3'
ENCODING = 'utf-8'  # или 'cp1251', если файл в Win-1251

# Подключение к SQLite
conn = sqlite3.connect(SQLITE_DB)
cursor = conn.cursor()

# Создание таблицы (если не существует)
cursor.execute('''
CREATE TABLE IF NOT EXISTS payments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    electricity_curr INTEGER NOT NULL,
    gas_curr INTEGER NOT NULL,
    water_curr INTEGER NOT NULL,
    internet_cost DECIMAL NOT NULL,
    trash_cost DECIMAL NOT NULL           
)
''')

# Чтение Excel
try:
    df = pd.read_excel(
        EXCEL_FILE,
        engine='openpyxl',
        usecols=['date', 'electricity_curr', 'gas_curr', 'water_curr','internet_cost','trash_cost','payer_id'],
        parse_dates=['date']
    )
    
    # Очистка и преобразование данных
    df = df.dropna()  # Удаление пустых строк
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')  # Форматирование даты

    # Запись в SQLite
    df.to_sql(
        'payments_payment',
        conn,
        if_exists='append',  # Добавляем к существующим данным
        index=False,
        dtype={
            'date': 'DATE',
            'electricity_curr': 'INTEGER',
            'gas_curr': 'INTEGER',
            'water_curr': 'INTEGER',
            'internet_cost': 'DECIMAL',
            'trash_cost': 'DECIMAL',
            'payer_id': 'ForeignKey'

        }
    )
    print(f"Данные успешно загружены. Добавлено {len(df)} записей.")

except Exception as e:
    print(f"Ошибка: {e}")
finally:
    conn.close()
