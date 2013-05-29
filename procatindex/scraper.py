import re
import requests

def get_cats():
    response = requests.get('http://procatinator.com/js/application.js')
    response.raise_for_status()

    for line in response.content.split('\n'):
        if line.startswith('theCats.push'):
            cat_data = parse_cat(line)
            youtube_data = get_youtube_data(cat_data['youtube'])
            store_cat(cat_data['cat_id'], youtube_data['title'])


def parse_cat(line):
    match = re.search(
            "'(?P<start_time>.+)','(?P<image>.+)', "
            "'(?P<youtube>\S+)'\)\); \/\/(?P<cat_id>\d+) "
            "(?P<title>.+)", line)
    return match.groupdict()


def get_youtube_data(video_id):
    url = 'http://gdata.youtube.com/feeds/api/videos/' + video_id
    response = requests.get(url, params={'v': 2, 'alt': 'jsonc'})
    response.raise_for_status()
    data = response.json()['data']
    return data


def store_cat(cat_id, title):
    try:
        existing = storage.get_cat(cat_id)
    except storage.NotFound:
        insert_cat(cat_id, title)
    else:
        if existing['title'] != title:
            storage.update_cat(cat_id, title)
