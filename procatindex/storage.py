import datetime
from flask import g
from sqlite3 import dbapi2 as sqlite3


class NotFound(Exception):
    pass

class NotUnique(Exception):
    pass


def connect_db(app):
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])


def init_db(app):
    """Creates the database tables."""
    with closing(connect_db(app)) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()


def query_db(query, args=(), one=False, db=None):
    """Makes querying the databse a little nicer."""
    db = db or g.db

    try:
        cursor = db.execute(query, args)
    except sqlite3.IntegrityError, e:
        if "not unique" in str(e):
            raise NotUnique()
        raise

    result = [dict((cursor.description[i][0], value)
                for i, value in enumerate(row))
                for row in cursor.fetchall()]

    return (result[0] if result else None) if one else result


def get_cat(cat_id, db=None):
    sql = "select id, title from cats where id = ?"
    result = query_db(sql, [cat_id], one=True, db=db)
    if not result:
        raise NotFound()
    return result


def insert_cat(cat_id, title, db=None):
    sql = "insert into cats(id, title, created) "\
            "values(?, ?, ?)"
    created = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.000")
    query_db(sql, [cat_id, title, created], db=db)
    db.commit()


def update_cat(cat_id, title, db=None):
    sql = "update cats set title = ? where id = ?"
    query_db(sql, [title, cat_id], db=db)
    db.commit()


def get_all_cats(db=None):
    sql = "select * from cats order by created asc"
    result = query_db(sql, [], db=db)
    return result


def get_recent_cats(n, db=None):
    sql = "select * from urls order by created desc limit %s" % n
    result = query_db(sql, [], db=db)
    return result


def store_cat(cat_id, title, db=None):
    try:
        existing = get_cat(cat_id, db=db)
    except NotFound:
        insert_cat(cat_id, title, db=db)
    else:
        if existing['title'] != title:
            update_cat(cat_id, title, db=db)
