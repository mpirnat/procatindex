def datetimeformat(value, format='%H:%M / %d-%m-%Y'):
    return value.strftime(format)


def datetimerss(value):
    return datetimeformat(value, format='%a, %d %b %Y %H:%M:%S +0000')


def register_filters(app):
    app.jinja_env.filters['datetimeformat'] = datetimeformat
    app.jinja_env.filters['datetimerss'] = datetimerss
