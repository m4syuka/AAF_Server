import logging

from bs4 import BeautifulSoup
import requests
import logging

logger = logging.getLogger(__name__)


def get_page(url: str) -> BeautifulSoup:
    """Получить страницу
    :param url: ссылка на страницу
    :return : возвращает BeautifulSoup объект
    """
    response = requests.get(url)
    response.raise_for_status()

    return BeautifulSoup(response.text, "html.parser")


def get_film_from_selector(page: BeautifulSoup) -> list:
    """
    Получить список фотопленок из выпадающего списка
    :param page: страница с селектором
    :return: [(url_value, film_name), ...]
    """
    selector_values = page.find("select", {"name": "Film", "id": "Film", "class": "pulldown"})
    selector_list = selector_values.findAll("option")[3:-2]
    film_list = []
    for single_option in selector_list:
        film_list.append((single_option.attrs['value'], single_option.text))

    logger.info(f"film list from selector [(url_value, film_name), ...]: {film_list}")
    return film_list


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


def get_film_recepts(url_to_recept: str, temp_units = "C", time_units = "T") -> list:
    """
    Получить из таблицы список рецептов
    :param url_to_recept: ссылка на конкретную пленку
    :param temp_units: Единицы измерения температуры (C/F)
    :param time_units: Формат времени (T/D)
    :return: Список с рецептами
    """
    url_page = f'https://www.digitaltruth.com/devchart.php?Film={url_to_recept}&Developer=&mdc=Search&TempUnits={temp_units}&TimeUnits={time_units}'
    page = get_page(url_page)
    recept_table = page.find("table", {"class": "mdctable sortable"})
    recept_table_body = recept_table.contents[1].findAll("td")

    recept_list = [recept_table_body[i:i + 9] for i in range(0, len(recept_table_body), 9)]
    return_recept = list()
    for current_recept in recept_list:
        try:
            temp_recept = [current_recept[i].text for i in range(len(current_recept) - 1)]
            if len(current_recept[8].contents) == 2:
                notes_col = _get_notes_for_film(current_recept[8].contents[0].get('href'))
                temp_recept.append(notes_col)
            elif len(current_recept[8].contents) == 1:
                notes_col = ""
                temp_recept.append(notes_col)
            else:
                notes_col = ""
                temp_recept.append(notes_col)

            return_recept.append(tuple(temp_recept))
        except Exception as e:
            logger.error(f"Error parsing recept page url - {url_page}\n{e}")

    logger.info(f"recepts from '{url_to_recept}' :{return_recept}")
    return return_recept

