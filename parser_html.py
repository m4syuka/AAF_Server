from bs4 import BeautifulSoup
import db_wrapper
import requests


def get_page(url: str) -> BeautifulSoup:
    """Получить страницу
    :param url: ссылка на страницу
    :return : возвращает BeautifulSoup объект
    """
    response = requests.get(url)
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def _get_film_from_selector(page: BeautifulSoup) -> list:
    """
    Получить список фотопленок из выпадающего списка
    :param page: страница с селектором
    :return: [[url_value, film_name]]
    """
    selector_values = page.find("select", {"name": "Film", "id": "Film", "class": "pulldown"})
    selector_list = selector_values.findAll("option")[3:-2]
    films_list = []
    for single_option in selector_list:
        films_list.append([single_option.attrs['value'], single_option.text])

    return films_list


def _get_notes_for_film(url: str) -> str:
    """
    Получение заметки из рецепта
    :param url: Ссылка на заметку
    :return: Строка с заметками. Несколько заметок разделены \n
    """
    page = get_page(f'https://www.digitaltruth.com/{url}')
    note_table = page.find("table", {"class": "notenote"})
    td_table = note_table.findAll("td")[1::2]
    td_table = [td_table[i].text + "\n" for i in range(len(td_table))]

    return ''.join(td_table)


def _get_film_recept(url_to_recept: str) -> list:
    """
    Получить из таблицы список рецептов
    :param url_to_recept: ссылка на конкретную пленку
    :return: Список с рецептами
    """
    page = get_page(
        f'https://www.digitaltruth.com/devchart.php?Film={url_to_recept}&Developer=&mdc=Search&TempUnits=C&TimeUnits=T')
    recept_table = page.find("table", {"class": "mdctable sortable"})
    recept_table_body = recept_table.contents[1].findAll("td")

    recept_list = [recept_table_body[i:i + 9] for i in range(0, len(recept_table_body), 9)]
    return_recept = list()
    for current_recept in recept_list:
        temp_recept = [current_recept[i].text for i in range(len(current_recept) - 1)]
        if len(current_recept[8].contents) == 2:
            notes = _get_notes_for_film(current_recept[8].contents[0].get('href'))
            temp_recept.append(notes)
        elif len(current_recept[8].contents) == 1:
            notes = ""
            temp_recept.append(notes)
        else:
            notes = ""
            temp_recept.append(notes)

        return_recept.append(temp_recept)

    return return_recept


def get_films(page: BeautifulSoup):
    films_list = _get_film_from_selector(page)
    #db_wrapper.upload_films_from_selector(films_list)
    for idx in films_list:
        try:
            recept_lst = _get_film_recept(idx[0])
            recept_from_bd = db_wrapper.get_film_recept(films_list[1])
        except Exception as e:
            print(e)
        pass
    pass
