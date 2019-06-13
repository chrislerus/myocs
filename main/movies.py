from bs4 import BeautifulSoup
import requests
from datetime import datetime
from datetime import timedelta

LIMIT=30
BASE_URL="https://www.ocs.fr"
RAW_OCS_MOVIES="{}/ajax/programs/search?categories%5B%5D=movie&keyword=&order=null&refresh=false&offset={}&limit={}"


def clean_movies():
	n = LIMIT
	step = 0
	l_movies = []
	while n == LIMIT:
		response = get_raw_data(RAW_OCS_MOVIES.format(BASE_URL, step, LIMIT))
		soup = get_soup(response.text)
		html_movies = soup.find_all("div", {"class": "result"})
		n = len(html_movies)
		for result in html_movies:
			movie_info = {}
			title = result.find("h3").find("span")
			movie_info['title'] = title
			href = result.find("a").get('href')
			get_detail_data(BASE_URL + href, movie_info)
			l_movies.append(movie_info)
		step += LIMIT
	return str(l_movies)


def get_detail_data(url, movie_info):
	detail_data = get_raw_data(url)
	soup = get_soup(detail_data.text).find('div', {'class': 'film-over-pres'})
	movie_info['img_url'] = soup.find('img').get('src')
	movie_info['date_exp'] = get_expiration_date(soup.find('li').text)
	movie_info['origin'] = "ocs"


def get_days_number(text):
	for s  in text.split():
		if s.isdigit():
			return int(s)
	return text.split()


def get_expiration_date(text):
	n_days_exp = get_days_number(text)
	if n_days_exp == 99:
		# 2100 : Never expired
		return 4102444800
	else:
		exp_date = datetime.now() + timedelta(days=n_days_exp)
		return exp_date.timestamp()


def get_soup(html_doc):
	soup = BeautifulSoup(html_doc, 'html.parser')
	return soup


def get_raw_data(url):
	response = requests.get(url)
	return response
