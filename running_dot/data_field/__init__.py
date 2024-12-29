import logging
from typing import Any, Dict, List, Optional

from ..schema.run_metric import RunMetric


class RunDataProvider:
    
    def __init__(
        self,
        name: str,
        app_id: str,
        author: str,
        metrics: Optional[List[RunMetric]] = None,
    ) -> None:
        self.name = name
        self.app_id = app_id
        self.author = author
        self.metrics = metrics or []
        self.fid2metric = {
            metric.key or metric.developer_field_number: metric
            for metric in self.metrics
        }

    def add_metric(self, metric: RunMetric) -> None:
        self.metrics.append(metric)

    @property
    def app_url(self) -> str:
        return f"https://apps.garmin.com/apps/{self.app_id}"
    
    def __getitem__(self, dev_field_no: int) -> Optional[RunMetric]:
        if dev_field_no in self.fid2metric:
            return self.fid2metric[dev_field_no]
        else:
            # logging.warning(f"Unknown developer field number: {dev_field_no}")
            return None
        
    def get_metric_from_dict(self, metric_dict: Dict[str, Any]) -> Optional[RunMetric]:
        if "connectIQ" in metric_dict["key"]:
            # connect iq field
            return self[metric_dict["developerFieldNumber"]]
        else:
            # garmin field
            return self[metric_dict["key"]]
