import datetime
import os
from flask import g, request, session, abort, redirect, render_template
from flask import send_from_directory
from procatindex import get_app
from procatindex.filters import register_filters
from procatindex.model import Cat
from procatindex import storage

app = get_app()
register_filters(app)


@app.before_request
def before_request():
    g.db = storage.connect_db(app)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    cats = [Cat.from_db(x) for x in storage.get_all_cats()]
    count = len(cats)
    return render_template('index.html', **locals())


@app.route('/rss')
def rss():
    cats = [Cat.from_db(x) for x in storage.get_recent_cats(20)]
    now = datetime.datetime.utcnow()
    return render_template('rss.html', **locals())


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(
            os.path.join(app.root_path, 'static'),
                    'favicon.ico',
                    mimetype='image/vnd.microsoft.icon')


if __name__ == '__main__':
    app.run()
