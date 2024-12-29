from datetime import datetime
from typing import List, Optional

import numpy as np
from pydantic import BaseModel

from ..client import BaseClient
from ..data_field.utils import get_metric_provider
from ..data_field import RunMetric


class RunActivity(BaseModel):

    activity_id: str
    start_time: datetime
    activity_name: Optional[str] = None
    timezone: Optional[str] = None
    calories: Optional[float] = None
    is_treadmill: bool = False
    run_metrics: Optional[List[RunMetric]] = None

    @staticmethod
    def get_tz(start_local: str, start_gmt: str) -> str:
        hour_diff = int(((
            datetime.fromisoformat(start_local) - datetime.fromisoformat(start_gmt)
        ).total_seconds() / 60) / 60)
        sign = "+" if hour_diff > 0 else "-"
        return f"GMT{sign}{hour_diff}"
    
    @property
    def url(self) -> str:
        return f"https://connect.garmin.com/modern/activity/{self.activity_id}"

    @classmethod
    def from_garmin_activity(cls, activity: dict) -> "RunActivity":
        tz = cls.get_tz(activity["startTimeLocal"], activity["startTimeGMT"])
        return cls(
            activity_id=str(activity["activityId"]),
            start_time=activity["startTimeLocal"],
            activity_name=activity["activityName"],
            timezone=tz,
            calories=activity["calories"],
        )
    
    def load_details(self, client: BaseClient) -> None:
        details = client.get_activity_details(self.activity_id)
        run_metrics = []
        metric_array = np.array([t["metrics"] for t in details["activityDetailMetrics"]])

        for i, metric in enumerate(details["metricDescriptors"]):
            provider = get_metric_provider(metric)
            run_metric = provider.get_metric_from_dict(metric)
            if run_metric:
                run_metric.set_value(metric_array[:, i])

            run_metrics.append(run_metric)

        self.run_metrics = run_metrics
