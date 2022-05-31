from typing import Dict, Optional
from pydantic import BaseModel
import datetime

class BenchmarkResult(BaseModel):
    id: str
    type: str
    resource: str
    started: datetime.datetime

    metrics: Dict[str, Optional[str]]
