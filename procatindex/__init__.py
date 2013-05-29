from flask import Flask


def get_app(name=None):
    app = Flask(name or __name__)
    app.config.from_object('procatindex.settings')
    app.config.from_envvar('PROCATINDEX_SETTINGS', silent=True)
    return app
