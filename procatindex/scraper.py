import re
import requests
import time

from BeautifulSoup import BeautifulSoup
from flask import Flask
from procatindex import get_app
from procatindex import storage


def main():
    app = get_app()
    db = storage.connect_db(app)
    get_cats(db)
    db.close()


def get_cats(db):

    inserted = 0
    updated = 0
    total = 0

    content = get_latest_application_js()

    for line in content.split('\n'):
        if line.startswith('theCats.push'):
            total += 1

            cat_data = parse_cat(line)

            try:
                existing = storage.get_cat(cat_data['cat_id'], db=db)

            except storage.NotFound:
                youtube_data = get_youtube_data(cat_data['youtube'])

                print "Inserting cat %s into db" % cat_data['cat_id']
                storage.insert_cat(
                        cat_data['cat_id'], youtube_data['title'], db=db)
                inserted += 1

    print "Inserted %s cats" % inserted
    print "Updated %s cats" % updated
    print "Processed %s total cats" % total


def get_latest_application_js():
    print "Getting data from procatinator..."

    response = requests.get('http://procatinator.com')
    soup = BeautifulSoup(response.content)
    urls = [x['src'] for x in soup.findAll('script')
            if x.has_key('src')
            and '/application.js' in x['src']]
    if not urls:
        raise Exception("Couldn't find application.js link!")

    url = 'http://procatinator.com' + urls[0]
    response = requests.get(url)
    response.raise_for_status()

    return response.content


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
