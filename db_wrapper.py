import sqlite3

def upload_films_from_selector(films_list:list):
    """
    Загрузка списка фотопленок из селектора в БД
    :param films_list: Список фотопленок
    """
    _connection = sqlite3.connect("./film_db.db")
    _cursor = _connection.cursor()

    for film in films_list:
        _cursor.execute("INSERT INTO Film_selector_name (name, url) VALUES (?, ?)", (film[1], film[0]))

    _connection.commit()
    _connection.close()


def get_film_recept(film_name: str) -> list:
    """
    Получить рецепт фотопленки из БД
    :param film_name: Название фотопленки
    :return: список рецептов фотопленки из БД
    """
    pass