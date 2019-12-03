from mongoengine import StringField, connect, Document


class MongoStore:
    def __init__(self):
        self.db = 'garbanzo_project'

    def store(self, **kwargs):
        keys = kwargs.keys()
        record = type('MongoStoreRecord', (Document,), {k: StringField() for k in keys})(**kwargs)
        with connect(self.db):
            record.save()
