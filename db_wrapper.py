import sqlite3
import logging

logger = logging.getLogger(__name__)


def upload_films_from_selector(film_list: list, check_new=True):
    """
    Загрузка списка фотопленок из селектора в БД
    :param films_list: Список фотопленок
    :param check_new: Запись только новых фотопленок
    """
    _connection = sqlite3.connect("./film_db.db")
    _cursor = _connection.cursor()

    # сначала обновляем БД
    _cursor.execute('SELECT * FROM Film_selector_name')
    db_films = [tuple(film) for film in _cursor.fetchall()]
    logger.info(f"film from db: {db_films}")
    updatable_films = list(set(db_films) - set(film_list))
    logger.info(f"Update record in db: {updatable_films}")
    for corrupt_record in updatable_films:
        for film in film_list:
            if film[1] == corrupt_record[1]:
                _cursor.execute("UPDATE Film_selector_name SET url = ? WHERE name = ?", (film[0], film[1]))
            elif film[0] == corrupt_record[0]:
                _cursor.execute("UPDATE Film_selector_name SET name = ? WHERE url = ?", (film[1], film[0]))
    _connection.commit()

    # Потом записываем новые фотопленки
    _cursor.execute('SELECT * FROM Film_selector_name')
    db_films = [tuple(film) for film in _cursor.fetchall()]
    logger.info(f"film from db: {db_films}")
    newest_films = list(set(film_list) - set(db_films)) if check_new else film_list
    logger.info(f"Upload to db: {newest_films}")
    for film in newest_films:
        _cursor.execute("INSERT INTO Film_selector_name (name, url) VALUES (?, ?)", (film[1], film[0]))

    _connection.commit()
    _connection.close()


def upload_films_recept(films_list: list):
    pass


def get_film_recept(film_name: str) -> list:
    """
    Получить рецепт фотопленки из БД
    :param film_name: Название фотопленки
    :return: список рецептов фотопленки из БД
    """
    pass
