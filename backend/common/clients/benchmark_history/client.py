from typing import Dict, List

from sqlalchemy.orm import Session, subqueryload

from orm import engine
from orm.models import Benchmark, BenchmarkMetric


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

