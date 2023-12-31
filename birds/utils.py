import os


def clean_bird_name(bird):
    bird = bird.replace(' ', '_')
    bird = bird.replace('\'', '')
    bird = bird.lower()
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
    with open(filename + '.txt', 'r', encoding="utf-8") as f:
        urls = f.readlines()
    return [url.strip() for url in urls]


def save_urls(bird, urls, key):
    filename = get_filename(bird=bird, key=key)
    with open(filename + '.txt', 'w', encoding="utf-8") as f:
        for url in urls:
            f.write(url + '\n')


def load_state_list(state, key):
    filename = get_filename(state, key)
    with open(filename + '.txt', 'r', encoding="utf-8") as f:
        bird_names = [x for x in (line.strip() for line in f) if x]
    return bird_names
