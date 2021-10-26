from datetime import datetime
from playhouse.db_url import connect
from environs import Env
import pydantic
import peewee


env = Env()
env.read_env()
database = env.str("DATABASE_URL")
db = connect(database)


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Paste(BaseModel):
    slug = peewee.CharField()
    title = peewee.CharField()
    text = peewee.TextField()
    created_at = peewee.DateTimeField(default=datetime.now)
    signature = peewee.TextField(null=True)


class PasteRequestModel(pydantic.BaseModel):
    slug: str
    title: str
    text: str
    signature: str = None


class PasteResponseModel(pydantic.BaseModel):
    slug: str
    title: str
    text: str
    created_at: datetime
    signature: str = None


def create_tables():
    db.connect()
    db.create_tables([Paste])


if __name__ == "__main__":
    create_tables()
