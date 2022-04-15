from datetime import datetime
from typing import List, Optional, Tuple
from pydantic import BaseModel, Field


class DataRecordingModel(BaseModel):
    time: datetime = Field(...)
    value: float = Field(...)


class NodeMetricsModel(BaseModel):
    node_name: str = Field(...)
    memory_used: List[DataRecordingModel] = Field(default=[])
    cpu_busy: List[DataRecordingModel] = Field(default=[])
    disk_io_util: List[DataRecordingModel] = Field(default=[])


class PrometheusDataInstanceModel(BaseModel):
    metric: dict
    values: List[Tuple[float, str]]  # point in time, value


class PrometheusDataModel(BaseModel):
    resultType: str
    result: List[PrometheusDataInstanceModel]


class PrometheusApiResponseModel(BaseModel):
    status: str
    errorType: Optional[str] = None
    error: Optional[str] = None
    data: Optional[PrometheusDataModel] = None
