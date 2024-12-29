from typing import Dict, Literal, Optional

from .schema.run_activity import RunActivity


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
        