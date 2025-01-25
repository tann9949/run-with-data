from datetime import datetime
from typing import List, Optional

import numpy as np
import pandas as pd
from pydantic import BaseModel

from ..client import BaseClient
from ..data_field.utils import get_metric_provider
from ..data_field import RunMetric


def garmin_resample(df: pd.DataFrame, target_freq: str = '1s', break_threshold: int = 10):
    """
    Custom resample function for time series with varying sample rates.
    Handles multiple columns with datetime index.
    
    Parameters:
    -----------
    df : pandas.DataFrame
        Input dataframe with datetime index and value columns
    target_freq : str
        Target frequency for resampling (default: '1S' for 1 second)
    break_threshold : int
        Threshold in seconds to consider as a break (default: 10)
        
    Returns:
    --------
    pandas.DataFrame
        Resampled dataframe with breaks filled with zeros and other gaps
        filled using forward fill
    """
    # Ensure index is datetime
    df = df.copy()
    if not isinstance(df.index, pd.DatetimeIndex):
        df.index = pd.to_datetime(df.index)
    
    # Create a complete time range
    full_range = pd.date_range(
        start=df.index.min(),
        end=df.index.max(),
        freq=target_freq
    )
    
    # Reindex the dataframe to include all timestamps
    resampled = df.reindex(full_range)
    
    # Get original timestamps
    original_timestamps = df.index
    
    # Calculate the time difference between each timestamp and the nearest previous original timestamp
    time_diffs = []
    for idx in resampled.index:
        # Find timestamps before current index
        prev_timestamps = original_timestamps[original_timestamps <= idx]
        if len(prev_timestamps) > 0:
            # Calculate time difference with nearest previous timestamp
            time_diff = (idx - prev_timestamps[-1]).total_seconds()
            time_diffs.append(time_diff)
        else:
            time_diffs.append(0)  # For the first timestamp
            
    # Create mask for breaks
    break_mask = np.array(time_diffs) > break_threshold
    
    # Fill breaks with zeros first
    resampled.loc[break_mask] = 0
    
    # Then forward fill the remaining NaN values
    resampled = resampled.ffill()
    
    return resampled.fillna(0.)


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
            is_treadmill=activity["activityType"]["typeKey"] == "treadmill_running"
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

    def to_df(self, client: BaseClient, resample: Optional[str] = None) -> pd.DataFrame:
        self.load_details(client)

        columns = []
        data = []
        for metric in self.run_metrics:
            if metric is None:
                continue

            # custom power column for garmin/stryd power
            # since both use the same name
            if metric.name == "Power":
                columns.append(f"Power - {metric.app_name}")
            else:
                columns.append(metric.name)
            data.append(metric.value)
        data = np.stack(data).T
        df = pd.DataFrame(data, columns=columns)

        df["Timestamp"] = df["Timestamp"].map(lambda x: datetime.fromtimestamp(x/1000))
        df = df.set_index("Timestamp")

        if resample:
            df = garmin_resample(df, resample)
        return df

        
        
