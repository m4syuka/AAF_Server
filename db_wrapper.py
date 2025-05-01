import sqlite3
import logging

logger = logging.getLogger(__name__)



def upload_films_recepts(recepts_list: list):
    """
    Сохранение списка с рецептами фотопленок
    :param recepts_list: Список рецептов
    :return:
    """

    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    for recept in recepts_list:
        try:
            _cursor.execute('''
                INSERT OR IGNORE INTO Film_recept 
                VALUES (?,?,?,?,?,?,?,?,?,?)
            ''', (
                recept[0], recept[1], recept[2],
                recept[3], recept[4], recept[5],
                recept[6], recept[7], recept[8],
                "0"
            ))
            _connection.commit()
        except sqlite3.IntegrityError as e:
            continue

    _connection.close()


def get_list_of_films():
    """
    Получить список уникальных фотопленок
    :return: list
    """

    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT DISTINCT Film FROM Film_recept')

    films = _cursor.fetchall()

    _connection.close()

    return {"len":len(films),
            "list":list(film[0] for film in films)}


def recepts_by_name(film_name: str, recept_idx: int):
    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT * FROM Film_recept WHERE Film = ?', (film_name,))

    recepts = _cursor.fetchall()

    _connection.close()

    return recepts if recept_idx == -1 else recepts[recept_idx]
