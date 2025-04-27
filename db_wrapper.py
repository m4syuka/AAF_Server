import sqlite3
import logging

logger = logging.getLogger(__name__)


def upload_films_recepts(recepts_list: list, film_selector_name: str):
    """
    Загрузка списка с рецептами фотопленок
    :param recepts_list: Список рецептов
    :param film_selector_name: Название фотопленки из селектора
    :param check_new: Запись только новых рецептов
    :return:
    """

    _connection = sqlite3.connect("./film_db.db")
    _cursor = _connection.cursor()


    logger.info(f"Upload to db len {len(recepts_list)}: {recepts_list}")
    for recept in recepts_list:
        _cursor.execute(
            "INSERT INTO Film_recept (Film, Developer, Dilution, ISO, mm35, mm120, Sheet, Temp, Notes, Forward_recept)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (
            recept[0], recept[1], recept[2], recept[3], recept[4], recept[5], recept[6], recept[7], recept[8], False))

    _connection.commit()
    _connection.close()


def get_forward() -> list:
    """
    Получить список избранных рецептов
    :return: Список избранных рецептов
    """
    _connection = sqlite3.connect("./film_db.db")
    _cursor = _connection.cursor()

    # запись новых рецептов
    _cursor.execute('SELECT * FROM Film_recept WHERE Forward = 1')
    forward_recepts = [tuple(film[:9]) for film in _cursor.fetchall()]

    _connection.commit()
    _connection.close()

    return  forward_recepts



def get_myself() -> list:
    """
    Получить список самосозданных рецептов
    :return: Список самосозданных рецептов
    """
    _connection = sqlite3.connect("./film_db.db")
    _cursor = _connection.cursor()

    # запись новых рецептов
    _cursor.execute('SELECT * FROM Film_recept WHERE Myself_recept = 1')
    forward_recepts = [tuple(film[:9]) for film in _cursor.fetchall()]

    _connection.commit()
    _connection.close()

    return  forward_recepts