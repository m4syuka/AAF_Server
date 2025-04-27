from bs4 import BeautifulSoup
import requests
import parser_html
import logging
import db_wrapper
import flask
import threading
import configparser
import time

logging.basicConfig(level=logging.INFO, filename="./log.log", filemode="w",
                    format="%(asctime)s [%(levelname)s - %(module)10s -  %(funcName)20s()] %(message)s",
                    datefmt="%%d-%m-%Y %H:%M:%S")
logger = logging.getLogger(__name__)
app = flask.Flask(__name__)

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
            film_recepts = parser_html.get_film_recepts(film[0])
            if WRITE_TO_DB_FLAG:
                db_wrapper.upload_films_recepts(film_recepts, film[1])

    except requests.HTTPError as e:
        logging.error(e)

@app.route('/check')
def default_route():
    return  {"error": False, "message": "", "content":"ok"}



@app.route('/forward')
def forward():
    error = False
    message = ""
    content = ""
    try:
        content = db_wrapper.get_forward()
    except Exception as e:
        error = True
        message = str(e)

    return {"error":error, "message":message, "content":content}


@app.route('/film')
def film():
    pass


if __name__ == '__main__':
    # update_db_trhead = threading.Thread(target=update_db)
    # update_db_trhead.start()
    # app.run(host='0.0.0.0', port=5000, debug=True)
    update_db()
