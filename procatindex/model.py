from dateutil.parser import parse as parse_date


class Cat(object):

    cat_id = None
    title = None
    created = None

    @classmethod
    def from_db(cls, data):
        self = cls()
        self.cat_id = data['id']
        self.title = data['title']
        self.created = parse_date(data['created'])
        return self

    @property
    def link(self):
        return "http://procatinator.com/?cat=%s" % (self.cat_id or 0)
