from bs4 import BeautifulSoup
import requests


def get_page(url):
    return requests.get(url).text


def get_soup(text):
    return BeautifulSoup(text, "html.parser")


def get_bird_url(bird):
    bird = ' '.join(word for word in bird.split())
    bird = bird.replace(' ', '_')
    bird = bird.replace("'", '')
    return 'https://www.allaboutbirds.org/guide/{:s}/'.format(bird)
