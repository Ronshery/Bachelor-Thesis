from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP

metadata_obj = MetaData()

benchmarks_table = Table(
     "benchmarks",
     metadata_obj,
     Column('id', String, primary_key=True, nullable=False),
     Column('node_id', String, nullable=False),
     Column('pod_id', String, nullable=False),
     Column('started', TIMESTAMP, nullable=False),
     Column('duration', Integer),
     Column('image', String),
     Column('options', String),
     Column('logs', String)
)

metrics_table = Table(
     "benchmark_metrics",
     metadata_obj,
     Column('benchmark_id', ForeignKey("benchmarks.id"), primary_key=True, nullable=False),
     Column('name', String(30), primary_key=True, nullable=False),
     Column('value', String)
)
