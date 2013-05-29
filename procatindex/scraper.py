import re
import requests
import time

from flask import Flask
from procatindex.app import get_app
from procatindex import storage


def main():
    app = get_app()
    db = storage.connect_db(app)
    get_cats(db)
    db.close()


def get_cats(db):
    print "Getting data from procatinator..."
    response = requests.get('http://procatinator.com/js/application.js')
    response.raise_for_status()

    for line in response.content.split('\n'):
        if line.startswith('theCats.push'):
            cat_data = parse_cat(line)
            youtube_data = get_youtube_data(cat_data['youtube'])
            print "Storing cat id %s in db" % cat_data['cat_id']
            storage.store_cat(cat_data['cat_id'], youtube_data['title'], db=db)


def parse_cat(line):
    print "Parsing cat..."
    match = re.search(
            "'(?P<start_time>.+)','(?P<image>.+)', "
            "'(?P<youtube>\S+)'\)\); \/\/(?P<cat_id>\d+) "
            "(?P<title>.+)", line)
    return match.groupdict()


def get_youtube_data(video_id):
    print "Getting data from youtube api..."

    # avoid getting 403ed by youtube
    time.sleep(1)

    url = 'http://gdata.youtube.com/feeds/api/videos/' + video_id
    response = requests.get(url, params={'v': 2, 'alt': 'jsonc'})
    response.raise_for_status()
    data = response.json()['data']
    return data


if __name__ == '__main__':
    main()
