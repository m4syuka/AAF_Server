from bs4 import BeautifulSoup
import requests
import parser_html
import logging
import db_wrapper

logging.basicConfig(level=logging.DEBUG, filename="./log.log", filemode="w",
                    format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

URL = "https://www.digitaltruth.com/devchart.php"
WRITE_TO_DB_FLAG = True


def update_db():
    try:
        page_html = parser_html.get_page(URL)
        film_list = parser_html.get_film_from_selector(page_html)
        if  WRITE_TO_DB_FLAG:
            db_wrapper.upload_films_from_selector(film_list)
    except requests.HTTPError as e:
        logging.error(e)

def main():
    update_db()

if __name__ == '__main__':
    main()
