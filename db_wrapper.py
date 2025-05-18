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


def get_list_size() -> int:
    """
    Получить количество уникальных фотопленок
    :return: количество
    """

    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT DISTINCT Film FROM Film_recept')

    films = _cursor.fetchall()

    _connection.close()

    return len(list(film[0] for film in films))


def get_film_list_step(start: int, end:int) -> list():
    """
    Получить список фотолпенок согласно диапозону
    :param start: стартовая позиция
    :param end: конечная позиция
    :return: список фотопленок
    """

    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT DISTINCT Film FROM Film_recept')

    films = list()
    if start == -1 and end == -1:
        films = _cursor.fetchall()
    elif start == -1 or end == -1:
        raise Exception(f'error start or end index. {start}, {end}')
    else:
        films = _cursor.fetchall()[start:end]

    _connection.close()

    return list(film[0] for film in films)


def recepts_by_name(film_name: str, recept_idx: int):
    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT * FROM Film_recept WHERE Film = ?', (film_name,))

    recepts = _cursor.fetchall()

    _connection.close()

    return recepts if recept_idx == -1 else recepts[recept_idx]


def get_developer_by_film_name(film_name: str):
    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT DISTINCT Developer FROM Film_recept WHERE Film = ?', (film_name,))
    developers = _cursor.fetchall()

    _connection.close()

    return list(dev[0] for dev in developers)


def get_iso_by_dev_and_film(film_name: str, dev_name: str):
    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    _cursor.execute('SELECT DISTINCT ISO FROM Film_recept WHERE Film = ? AND Developer = ?', (film_name,dev_name,))
    ISO = _cursor.fetchall()

    _connection.close()

    return list(iso[0] for iso in ISO)


def get_time_by_iso_dev_film(film_name: str, dev_name:str, ISO:str, frmt:str):
    _connection = sqlite3.connect("./film.db")
    _cursor = _connection.cursor()

    if frmt == "mm35":
        _cursor.execute('SELECT  mm35, Dilution FROM Film_recept WHERE Film = ? AND Developer = ? AND ISO = ? ',
                        (film_name, dev_name, ISO, ))
    elif frmt == "mm120":
        _cursor.execute('SELECT mm120, Dilution FROM Film_recept WHERE Film = ? AND Developer = ? AND ISO = ? ',
                        (film_name, dev_name, ISO, ))
    recepts = _cursor.fetchall()
    _connection.close()

    rec_dict = {}
    for recept in recepts:
        if recept[0].find('-') != -1:
            start = int(recept[0].split('-')[0])
            end = int(recept[0].split('-')[1])
            for i in range(start, end + 1):

                rec_dict[i] = recept[1]
        else:
            rec_dict[recept[0]] = recept[1]


    return rec_dict
