import streamlit as st
import os

def clean_bird_name(bird):
    bird = bird.replace(' ', '_')
    bird = bird.replace('\'', '')
    return bird


def get_base_dir(key):
    bird_dir = os.path.dirname(__file__)
    bird_dir = os.path.join(bird_dir, 'resources', key)
    if not os.path.exists(bird_dir):
        os.mkdir(bird_dir)
    return bird_dir


def get_filename(bird, key):
    bird = clean_bird_name(bird)
    return os.path.join(get_base_dir(key), bird)


# @st.cache_data
def load_urls(bird, key):
    filename = get_filename(bird=bird, key=key)
    with open(filename + '.txt', 'r') as f:
        urls = f.readlines()
    return [url.strip() for url in urls]


def save_urls(bird, urls, key):
    try:
        filename = get_filename(bird=bird, key=key)
        with open(filename + '.txt', 'w') as f:
            for url in urls:
                f.write(url + '\n')
    except:
        print('Failed to save {:s} url'.format(key))
