from bs4 import BeautifulSoup
import requests
import parser_html
import logging
import db_wrapper
from flask import Flask, request
import threading
import configparser
import time
import sys
import flask_cors

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%m-%Y %H:%M:%S",
    handlers=[
        logging.FileHandler("./log.log", mode="w"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)
app = Flask(__name__)
flask_cors.CORS(app)

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

@app.route("/film_size", methods=['GET'])
def films_size():
    error_flag = False
    result = ""
    try:
        result = db_wrapper.get_list_size()
    except Exception as e:
        error_flag = True

    return {
        "err": error_flag,
        "res": result
    }


@app.route("/film_list_all", methods=['GET'])
def film_list_all():
    error_flag = False
    result = ""
    try:
        result = db_wrapper.get_film_list_step(0, db_wrapper.get_list_size())
    except Exception as e:
        error_flag = True

    return {
        "err": error_flag,
        "res": result
    }


@app.route("/dev_by_film", methods=['POST'])
def dev_by_film():
    error_flag = False
    result = ""
    try:
        req_json = request.get_json()
        result = db_wrapper.get_developer_by_film_name(req_json["film"])
    except Exception as e:
        error_flag = True

    return {
        "err": error_flag,
        "res": result
    }


@app.route("/iso_by_dev_film", methods=['POST'])
def iso_by_dev_film():
    error_flag = False
    result = ""
    try:
        req_json = request.get_json()
        result = db_wrapper.get_iso_by_dev_and_film(req_json["film"], req_json["dev"])
    except Exception as e:
        error_flag = True

    return {
        "err": error_flag,
        "res": result
    }


@app.route("/time_by_iso_dev_film_frmt", methods=['POST'])
def time_by_iso_dev_film():
    error_flag = False
    result = ""
    try:
        req_json = request.get_json()
        result = db_wrapper.get_time_by_iso_dev_film(req_json["film"], req_json["dev"], req_json["ISO"], req_json["frmt"])
    except Exception as e:
        error_flag = True

    return {
        "err": error_flag,
        "res": result
    }




if __name__ == '__main__':
    # update_db_trhead = threading.Thread(target=update_db)
    # update_db_trhead.start()
    app.run(host='0.0.0.0', port=5000, debug=True)
    # update_db()
