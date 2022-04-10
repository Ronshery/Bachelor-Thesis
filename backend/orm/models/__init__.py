from sqlalchemy import MetaData, ForeignKey
from sqlalchemy import Table, Column, Integer, String, TIMESTAMP
from sqlalchemy.orm import relationship, declarative_base, registry

mapper_registry = registry()

# TODO remove
metadata_obj = mapper_registry.metadata

Base = mapper_registry.generate_base()


class Benchmark(Base):
    __tablename__ = "benchmarks"

    id = Column(String, primary_key=True, nullable=False)
    node_id = Column(String, nullable=False)
    pod_id = Column(String, nullable=False)
    started = Column(TIMESTAMP, nullable=False)
    duration = Column(Integer)
    image = Column(String)
    options = Column(String)
    logs = Column(String)


class BenchmarkMetric(Base):
    __tablename__ = "benchmark_metrics"

    benchmark_id = Column(ForeignKey("benchmarks.id"), primary_key=True, nullable=False)
    name = Column(String(30), primary_key=True, nullable=False)
    value = Column(String)


benchmarks_table = Benchmark.__table__
metrics_table = BenchmarkMetric.__table__
