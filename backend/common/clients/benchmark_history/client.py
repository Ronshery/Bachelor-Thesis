from typing import Dict, List, Optional
import datetime
from sqlalchemy.orm import Session, subqueryload
from sqlalchemy import and_

from orm import engine
from orm.models import Benchmark, BenchmarkMetric, NodeMetric


class BenchmarkHistoryClient:
    def get_benchmarks_results(self, node_name: str) -> List[Benchmark]:
        with Session(engine) as session:
            rows = session \
                .query(Benchmark) \
                .options(subqueryload(Benchmark.metrics)) \
                .join(BenchmarkMetric, Benchmark.id == BenchmarkMetric.benchmark_id) \
                .filter(Benchmark.node_id == node_name)

            results = []

            for row in rows:
                results.append(row)

            return results

    def get_benchmark_result(self, benchmark_id: str) -> Optional[Benchmark]:
        with Session(engine) as session:
            rows = session \
                .query(Benchmark) \
                .options(subqueryload(Benchmark.metrics)) \
                .join(BenchmarkMetric, Benchmark.id == BenchmarkMetric.benchmark_id) \
                .filter(Benchmark.id == benchmark_id)

            if any(rows):
                return rows[0]
            else:
                return None

    def get_node_metrics(self, node_name: str, time_from: datetime.datetime, time_to: datetime.datetime) -> List[NodeMetric]:
        with Session(engine) as session:
            rows = session \
                .query(NodeMetric) \
                .filter(NodeMetric.node_name == node_name) \
                .filter(and_(NodeMetric.timestamp >= time_from, NodeMetric.timestamp <= time_to))

            results = []

            for row in rows:
                results.append(row)

            return results

