import sqlite3

# Создаем подключение и таблицу
conn = sqlite3.connect('film.db')
cursor = conn.cursor()

# Создаем таблицу (если не существует)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Film_recept (
        Film TEXT,
        Developer TEXT,
        Dilution TEXT,
        ISO INTEGER,
        mm35 TEXT,
        mm120 TEXT,
        Sheet TEXT,
        Temp TEXT,
        Notes TEXT,
        Forward_recept TEXT
    )
''')

# Создаем уникальный индекс (ключевой момент!)
cursor.execute('''
    CREATE UNIQUE INDEX IF NOT EXISTS idx_full_unique 
    ON Film_recept (
        Film, Developer, Dilution, ISO,
        mm35, mm120, Sheet, Temp,
        Notes, Forward_recept
    )
''')

# Функция для безопасной вставки
def smart_insert(data):
    try:
        cursor.execute('''
            INSERT OR IGNORE INTO Film_recept 
            VALUES (?,?,?,?,?,?,?,?,?,?)
        ''', (
            data['Film'], data['Developer'], data['Dilution'],
            data['ISO'], data['mm35'], data['mm120'],
            data['Sheet'], data['Temp'], data['Notes'],
            data['Forward_recept']
        ))
        conn.commit()
        return cursor.rowcount > 0  # True если запись добавлена
    except sqlite3.IntegrityError as e:
        print(f"Ошибка уникальности: {e}")
        return False

# Тестовые данные
test_data = {
    'Film': 'Kodak Tri-X 400',
    'Developer': 'D-76',
    'Dilution': '1+1',
    'ISO': 400,
    'mm35': '8:30',
    'mm120': '9:45',
    'Sheet': '6:15',
    'Temp': '20°C',
    'Notes': 'Standard development',
    'Forward_recept': 'https://example.com/trix'
}

# Первая вставка
result1 = smart_insert(test_data)
print(f"Первая вставка: {'Успех' if result1 else 'Дубликат'}")

# Пытаемся вставить те же данные повторно
result2 = smart_insert(test_data)
print(f"Вторая вставка: {'Успех' if result2 else 'Дубликат'}")

conn.close()