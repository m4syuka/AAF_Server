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


def upload_films_recepts(recepts_list: list, film_selector_name: str, check_new=True):
    """
    Загрузка списка с рецептами фотопленок
    :param recepts_list: Список рецептов
    :param film_selector_name: Название фотопленки из селектора
    :param check_new: Запись только новых рецептов
    :return:
    """

    _connection = sqlite3.connect("./film_db.db")
    _cursor = _connection.cursor()


    _cursor.execute('SELECT * FROM Film_recept WHERE Film_selector = ?', (film_selector_name,))
    db_recepts = [tuple(film) for film in _cursor.fetchall()]
    logger.info(f"film from db: {db_recepts}")
    newest_recepts = list(set(recepts_list) - set(db_recepts)) if check_new else recepts_list
    logger.info(f"Upload to db: {newest_recepts}")
    for recept in newest_recepts:
        _cursor.execute("INSERT INTO Film_recept (Film, Developer, Dilution, ISO, mm35, mm120, Sheet, Temp, Notes, Film_selector, Myself_recept, Forward)"
                        " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (recept[0], recept[1], recept[2], recept[3], recept[4], recept[5], recept[6], recept[7], recept[8], film_selector_name, 0, 0))

    _connection.commit()
    _connection.close()

