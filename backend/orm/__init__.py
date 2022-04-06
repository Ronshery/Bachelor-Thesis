from sqlalchemy import create_engine
import orm.models as orm_models

engine = create_engine("sqlite+pysqlite:///test.sqlite")


def create_tables():
    orm_models.metadata_obj.create_all(engine)
