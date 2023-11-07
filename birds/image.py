from .html import *
from .utils import *
import streamlit as st
import re
import random


def get_image_urls(bird_name):
    url = get_bird_url(bird_name) + 'id/'
    page = get_page(url)
    soup = get_soup(page)
    image = soup.findAll('section', 'carousel wide id-carousel')[0]
    image = image.findAll('img')
    image = [img['data-interchange'].split('[')[-1].split(',')[0] for img in image]

    caption = soup.findAll('div', class_='annotation-txt')

    header = []
    for text in caption:
        content = re.search('<h5>(.*)</h5>', str(text))
        if isinstance(content, type(None)):
            header.append('')
        else:
            header.append(content.group(1))

    paragraph = []
    for text in caption:
        content = re.search('<p>(.*)</p>', str(text))
        if isinstance(content, type(None)):
            paragraph.append('')
        else:
            paragraph.append(content.group(1))

    caption = []
    for h, p in zip(header, paragraph):
        if h != '':
            caption.append('{:s}. {:s}'.format(h, p))
        else:
            caption.append('{:s}'.format(p))

    return image, caption


@st.cache_data
def find_image_urls(birds):
    image = {}
    # caption = {}
    for bird in birds:
        urls = load_urls(bird, 'image')
        # text = load_urls(bird, 'caption')
        if not isinstance(urls, list):
            urls = get_image_urls(birds[bird])
            save_urls(bird, urls, 'image')
            # save_urls(bird, text, 'caption')
        image[bird] = urls
        # caption[bird] = text
    return image


@st.cache_data
def find_caption_urls(birds):
    caption = {}
    for bird in birds:
        text = load_urls(bird, 'caption')
        if not isinstance(text, list):
            text = get_image_urls(birds[bird])
            save_urls(bird, text, 'caption')
        caption[bird] = text
    return caption


@st.cache_data
def get_image(birds, answer):
    image_file = find_image_urls(birds['name'])
    url = random.choice(image_file[answer])
    return url


@st.cache_data
def get_caption(birds, answer):
    caption_info = find_caption_urls(birds['name'])
    url = random.choice(caption_info[answer])
    return url
