from typing import Dict, Literal, Optional

import pandas as pd
from .schema.run_activity import RunActivity


def split_df(df: pd.DataFrame, min_break = 10):
    """Source: https://stackoverflow.com/questions/63959471/split-a-dataframe-by-rows-containing-zero-in-python-pandas"""
    df2 = df.mask((df['Speed'] == 0) & ((df['Speed'].shift(1) == 0) | (df['Speed'].shift(-1) == 0)))
    df2['group'] = (df2['Speed'].shift(1).isnull() & df2['Speed'].notnull()).cumsum()
    splits = [x[1] for x in list(df2[df2['Speed'].notnull()].groupby('group'))]
    return splits


def get_power_indices(activity: RunActivity, include_timestamp: bool = True) -> Dict[Literal["stryd", "garmin", "runpowermodel", "time"], int]:
    """Get index of metric from the run"""
    output = {
        "stryd": None,
        "garmin": None,
        "runpowermodel": None,
    }
    if include_timestamp:
        output["timestamp"] = None
    for i, _metric in enumerate(activity.run_metrics):
        if _metric is None:
            continue
        if all(_v is not None for _v in output.values()):
            break
        if _metric.name.lower() in ["power", "running power"]:
            if "stryd" in _metric.app_name.lower():
                output["stryd"] = i
            elif "runpowermodel" in _metric.app_name.lower():
                output["runpowermodel"] = i
            else:
                assert "garmin" in _metric.app_name.lower()
                output["garmin"] = i

        if _metric.name.lower() == "timestamp":
            output["timestamp"] = i
    return output


def get_metric_index(activity: RunActivity, keyword: str) -> Optional[int]:
    for i, _metric in enumerate(activity.run_metrics):
        if _metric is None:
            continue
        if _metric.name.lower() == keyword.lower():
            return i
        