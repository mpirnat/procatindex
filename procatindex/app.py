from flask import g, request, session, abort, redirect, render_template
from procatindex import get_app
from procatindex import storage

app = get_app()


@app.before_request
def before_request():
    g.db = storage.connect_db(app)


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    cats = storage.get_all_cats()
    return render_template('index.html', **locals())

@app.route('/rss')
def rss():
    cats = storage.get_recent_cats(20)
    return render_template('rss.html', **locals())


if __name__ == '__main__':
    app.run()
