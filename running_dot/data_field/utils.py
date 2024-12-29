import logging
from typing import Any, Dict, Optional

from . import RunDataProvider

from .garmin import GarminDefaultField
from .run_power_model import RunPowerModel
from .stryd_zones import StrydZones


def get_metric_provider(metric: Dict[str, Any]) -> Optional["RunDataProvider"]:
    """Read metric from metricDescriptors field in details dict and return data provider"""
    if "key" in metric and "IQDeveloper" in metric["key"]:
        if metric["appID"] == RunPowerModel.APP_ID:
            return RunPowerModel()
        elif metric["appID"] == StrydZones.APP_ID:
            return StrydZones()
        else:
            logging.warning(f"Unknown app id: {metric['appID']}, skipping...")
            return None
    else:
        return GarminDefaultField()
    

def get_iq_app_name(app_id: str) -> str:
    if app_id == RunPowerModel.APP_ID:
        return RunPowerModel().name
    elif app_id == StrydZones.APP_ID:
        return StrydZones().name
    else:
        raise NameError(f"Unknown app id: {app_id}")
    