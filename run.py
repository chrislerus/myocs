from flask import Flask
from main.movies import clean_movies
app = Flask(__name__)


@app.route('/get_movies')
def get_movies():
	return clean_movies()
