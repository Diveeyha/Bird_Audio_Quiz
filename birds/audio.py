from .html import *
from .utils import *
import streamlit as st


def get_audio_urls(bird_name):
    url = get_bird_url(bird_name) + 'sounds'
    page = get_page(url)
    soup = get_soup(page)
    audio = soup.findAll('div', class_='jp-jplayer player-audio')
    audio = [content['name'] for content in audio]
    return audio


@st.cache_data
def find_bird_urls(birds):
    audio = {}
    for bird in birds:
        urls = load_urls(bird, 'audio')
        if not isinstance(urls, list):
            urls = get_audio_urls(birds[bird])
            save_urls(bird, urls, 'audio')
        audio[bird] = urls
    return audio


def get_audio(question_number, birds, answer):
    audio_file = find_bird_urls(birds['name'])
    url = random.choice(audio_file[answer])
    return url
