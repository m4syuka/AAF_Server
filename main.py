from bs4 import BeautifulSoup
import requests
import parser_html

URL = "https://www.digitaltruth.com/devchart.php"


def main():
    page_html = parser_html.get_page(URL)
    film_list = parser_html.get_films(page_html)


if __name__ == '__main__':
    main()
