from typing import Dict, Optional
from pydantic import BaseModel


class BenchmarkResult(BaseModel):
    type: str
    resource: str

    metrics: Dict[str, Optional[str]]
