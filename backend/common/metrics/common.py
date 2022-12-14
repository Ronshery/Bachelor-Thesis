from __future__ import annotations

import re
from typing import TypeVar, Optional, Type, Dict, Iterable, List, Union

TMetricClass = TypeVar("TMetricClass")


class BMMetricField:
    pattern: Optional[str]
    value: Optional[Union[str, List[str]]] = None
    collect_list: bool = False

    def __init__(self, pattern: Optional[str], collect_list: bool = False):
        self.pattern = pattern
        self.collect_list = collect_list

    def copy(self) -> BMMetricField:
        f = BMMetricField(
            pattern=self.pattern,
            collect_list=self.collect_list
        )
        f.value=self.value.copy() if type(self.value) == list else self.value
        return f

    def __str__(self):
        return self.value or repr(self)

    def __repr__(self):
        if self.value is not None:
            return repr(self.value)
        else:
            return f"(no value, pattern: {self.pattern})"


def read_benchmark_metrics(cls: Type[TMetricClass], lines: Iterable[str]) -> TMetricClass:
    metric_fields: Dict[str, BMMetricField] = {
        k: v for k, v in vars(cls).items() if isinstance(v, BMMetricField)
    }

    result = cls()

    for line in lines:
        for msmt, msmt_field in metric_fields.items():
            # print(f"Matching '{line.strip()}' against '{msmt_field.pattern}'")
            m = re.match(msmt_field.pattern, line.strip(), re.IGNORECASE)
            if m:
                val = m.group(1).strip()
                field: BMMetricField = getattr(result, msmt).copy()

                if field.collect_list:
                    if field.value is None:
                        field.value = [val]
                    else:
                        field.value.append(val)
                else:
                    field.value = val

                setattr(result, msmt, field)

    return result

