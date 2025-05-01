from bs4 import BeautifulSoup
import requests
import parser_html
import logging
import db_wrapper
from flask import Flask, request
import threading
import configparser
import time

logging.basicConfig(level=logging.INFO, filename="./log.log", filemode="w",
                    format="%(asctime)s [%(levelname)s] %(message)s",
                    datefmt="%d-%m-%Y %H:%M:%S")
logger = logging.getLogger(__name__)
app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')


# CONST
URL = "https://www.digitaltruth.com/devchart.php"
WRITE_TO_DB_FLAG = True


def update_db():
    try:
        page_html = parser_html.get_page(URL)
        film_list = parser_html.get_film_from_selector(page_html)
        for film in film_list:
            try:
                film_recepts = parser_html.get_film_recepts(film[0])
                if WRITE_TO_DB_FLAG:
                    logger.info(f'write to db "{film[1]}" len of recepts {len(film_recepts)}')
                    db_wrapper.upload_films_recepts(film_recepts)
            except Exception as e:
                logger.error(f"error in {film}")
                logger.error(e)

    except requests.HTTPError as e:
        logging.error(e)

@app.route('/check')
def default_route():
    return  "ok"

@app.route('/film_list', methods=['GET'])
def film_list():
    error_flag = False
    error_message = ""
    result = ""
    try:
        result = db_wrapper.get_list_of_films()
    except Exception as e:
        error_flag = True
        error_message = e

    return {
        "error_flag": error_flag,
        "error_message": str(error_message),
        "result": result
    }


@app.route("/recepts_by_name", methods=['POST'])
def film_by_name():
    error_flag = False
    error_message = ""
    result = ""
    try:
        film_name = request.get_json()['film_name']
        result = db_wrapper.recepts_by_name(film_name)
    except Exception as e:
        error_flag = True
        error_message = e

    return {
        "error_flag": error_flag,
        "error_message": str(error_message),
        "result": result
    }

if __name__ == '__main__':
    update_db_trhead = threading.Thread(target=update_db)
    update_db_trhead.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # update_db()
