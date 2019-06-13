from bs4 import BeautifulSoup
import unittest
import requests

from main import movies


class TestCanalApi(unittest.TestCase):
    def test_basic_call(self):
        response = requests.get(movies.RAW_OCS_MOVIES.format(movies.BASE_URL, 0, 20))
        self.assertEqual(200, response.status_code)
        soup = movies.get_soup(response.text)

        html_movies = soup.find_all("div", {"class": "result"})

        self.assertEqual(len(html_movies), 20)
        for result in html_movies:
            title = result.find("h3").find("span")
            href = result.find("a").get('href')
            self.assertNotEqual("", title)
            self.assertNotEqual("", href)

