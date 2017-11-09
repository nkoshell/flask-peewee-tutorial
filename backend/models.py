from peewee import PostgresqlDatabase, Model, PrimaryKeyField, CharField, TextField, ForeignKeyField


db = PostgresqlDatabase('flask-peewee-tutorial', user='postgres', password='qwerty', host='localhost', port=5432)


class BaseModel(Model):
    class Meta:
        database = db


class Category(BaseModel):
    id = PrimaryKeyField()
    title = CharField(max_length=50)

    def __str__(self):
        return '%s(id=%r, title=%r)' % (self.__class__.__name__, self.id, self.title)


class Book(BaseModel):
    id = PrimaryKeyField()
    title = CharField()
    description = TextField()
    url = CharField()

    category = ForeignKeyField(Category, related_name='books', on_delete='cascade')

    def __str__(self):
        return '%s(id=%r, title=%r, ..., category=%s)' % (self.__class__.__name__, self.id, self.title, self.category)


if __name__ == '__main__':
    db.connect()
    db.create_tables([Category, Book], safe=True)  # skip if tables exists
    db.commit()
    db.close()
