from bs4 import BeautifulSoup
import requests
import parser_html
import logging
import db_wrapper
import flask

logging.basicConfig(level=logging.INFO, filename="./log.log", filemode="w",
                    format="%(asctime)s [%(levelname)s - %(module)10s -  %(funcName)20s()] %(message)s",
                    datefmt="%%d-%m-%Y %H:%M:%S")
logger = logging.getLogger(__name__)
app = flask.Flask(__name__)

# CONST
URL = "https://www.digitaltruth.com/devchart.php"
WRITE_TO_DB_FLAG = True


def update_db():
    try:
        page_html = parser_html.get_page(URL)
        film_list = parser_html.get_film_from_selector(page_html)
        if WRITE_TO_DB_FLAG:
            db_wrapper.upload_films_from_selector(film_list)
        for film in film_list:
            film_recepts = parser_html.get_film_recepts(film[0])
            if WRITE_TO_DB_FLAG:
                db_wrapper.upload_films_recepts(film_recepts, film[1])
    except requests.HTTPError as e:
        logging.error(e)

@app.route('/check')
def default_route():
    return  {"error": False, "message": "None", "content":"ok"}


@app.route('/get_selector_list')
def get_selector_list():
    error = False
    message = ""
    content = ""
    try:
        selector_list = db_wrapper.get_all_selector_list()
        content = sorted(selector_list, key = lambda tup: tup[1])
    except Exception as e:
        error = True
        message = str(e)


    return  {"error": False, "message": message, "content":content}

@app.route('/get_recepts_by_selector', methods=['POST'])
def get_film_by_selector():
    error = False
    message = ""
    content = ""
    try:
        req_selector = flask.request.get_json()
        film_by_selector = db_wrapper.get_recept_by_selector(req_selector["selector"])
        content = sorted(film_by_selector, key = lambda tup: tup[1])
    except Exception as e:
        error = True
        message = str(e)

    return {"error":error, "message":message, "content":content}


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


@app.route('/myself')
def myself():
    error = False
    message = ""
    content = ""
    try:
        content = db_wrapper.get_myself()
    except Exception as e:
        error = True
        message = str(e)

    return {"error":error, "message":message, "content":content}


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
