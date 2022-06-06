from sqlalchemy import create_engine
from sqlalchemy.orm import registry

import orm.models as orm_models

engine = create_engine("sqlite+pysqlite:///test.sqlite")


def create_tables():
    orm_models.mapper_registry.metadata.create_all(engine)
