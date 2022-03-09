import asyncio
import json
import logging
import os
import datetime
from typing import List, Tuple, Dict, Optional

import aiohttp
from aiohttp import ClientSession

from common.clients.prometheus.schemes import PrometheusApiResponseModel, NodeMetricsModel, DataRecordingModel
from common.clients.prometheus.settings import PrometheusSettings, PrometheusQuery

prometheus_settings: PrometheusSettings = PrometheusSettings()


class PrometheusClient:

    @staticmethod
    async def __fetch__(url: str, session: ClientSession, item_tuple: Tuple[str, dict]):
        metric_name, query_specs = item_tuple
        try:
            async with session.get(url=url, params=query_specs) as response:
                res: dict = json.loads((await response.read()).decode('utf-8'))
                return metric_name, PrometheusApiResponseModel(**res)
        except BaseException as exc:
            logging.error(f"Unable to fetch metric '{metric_name}' from '{url}' with params '{query_specs}'",
                          exc_info=exc)

    @staticmethod
    async def __gather__(query_list: List[Tuple[str, dict]],
                         results: List[Tuple[str, PrometheusApiResponseModel]]):
        url: str = os.path.join(prometheus_settings.prometheus_endpoint, "api/v1/query_range")
        async with aiohttp.ClientSession() as session:
            results += await asyncio.gather(*[PrometheusClient.__fetch__(url, session, item_tuple)
                                              for item_tuple in query_list])

    @staticmethod
    def __transform_metrics__(result_list: List[Tuple[str, PrometheusApiResponseModel]]):
        node_aggregation_dict: Dict[str, NodeMetricsModel] = {}

        for metric_name, api_response in result_list:
            for data_instance in api_response.data.result:
                node_id: str = data_instance.metric.get("instance", None)
                if node_id:
                    data_list: List[DataRecordingModel] = [DataRecordingModel(time=float(tup[0]), value=float(tup[1]))
                                                           for tup in data_instance.values]
                    new_aggregations = {metric_name: data_list, "node_id": node_id}
                    aggregation_element: Optional[NodeMetricsModel] = node_aggregation_dict.get(node_id, None)
                    aggregation_dict: dict = aggregation_element.dict() if aggregation_element is not None else {}
                    aggregation_dict.update(new_aggregations)
                    node_aggregation_dict[node_id] = NodeMetricsModel(**aggregation_dict)

        return node_aggregation_dict

    @staticmethod
    def __get_metrics__(query_list: List[Tuple[str, str]], start: datetime, end: datetime):
        new_query_list: List[Tuple[str, dict]] = []
        for metric_name, query_string in query_list:
            query_specs: dict = {
                "query": query_string,
                "start": start.timestamp(),
                "end": end.timestamp(),
                "step": int(prometheus_settings.prometheus_query_step_width)
            }
            new_query_list.append((metric_name, query_specs))
        results: List[Tuple[str, PrometheusApiResponseModel]] = []
        asyncio.run(PrometheusClient.__gather__(new_query_list, results))
        return PrometheusClient.__transform_metrics__(results)

    @staticmethod
    def get_node_metrics(start: datetime, end: datetime):
        query_list: List[tuple] = [
            ("memory_used", PrometheusQuery.MEMORY_USED),
            ("cpu_busy", PrometheusQuery.CPU_BUSY),
            ("disk_io_util", PrometheusQuery.DISK_IO_UTIL)
        ]

        return PrometheusClient.__get_metrics__(query_list, start, end)


if __name__ == "__main__":
    test_res = PrometheusClient().get_node_metrics(datetime.datetime.now() - datetime.timedelta(seconds=5),
                                                   datetime.datetime.now())
    for k, v in list(test_res.items())[:5]:
        print(k, v)