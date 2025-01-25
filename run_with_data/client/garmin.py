import json
import os
from pathlib import Path
from typing import List, Dict, Any

from garminconnect import Garmin
from tqdm.auto import tqdm

from . import BaseClient
from ..schema.run_activity import RunActivity


class GarminClient(BaseClient):

    def __init__(self, cache_dir: str = "~/.cache/garmin_activities") -> None:
        super().__init__()
        self.cache_dir = os.path.expanduser(cache_dir)
        self.details_cache_dir = os.path.join(self.cache_dir, "details")
        
        # Create cache directories
        Path(self.details_cache_dir).mkdir(parents=True, exist_ok=True)

    def setup(self):
        try:
            self.client = Garmin(
                email=os.getenv("GARMIN_EMAIL"), 
                password=os.getenv("GARMIN_PASSWORD")
            )
            self.client.login()
        except Exception as e:
            if "2FA" in str(e):
                # Handle 2FA by requesting user input
                auth_code = input("Please enter the 2FA code sent to your email: ")
                self.client.login(auth_code)
            else:
                raise e

    def _get_cache_path(self, activity_id: str) -> str:
        return os.path.join(self.details_cache_dir, f"{activity_id}.json")

    def _read_from_cache(self, activity_id: str) -> Dict[str, Any]:
        cache_path = self._get_cache_path(activity_id)
        if os.path.exists(cache_path):
            with open(cache_path, 'r') as f:
                return json.load(f)
        return None

    def _write_to_cache(self, activity_id: str, data: Dict[str, Any]) -> None:
        cache_path = self._get_cache_path(activity_id)
        with open(cache_path, 'w') as f:
            json.dump(data, f)

    def get_activity_details(self, activity_id: str) -> Dict[str, Any]:
        # Try to read from cache first
        cached_data = self._read_from_cache(activity_id)
        if cached_data:
            return cached_data
            
        # If not in cache, fetch from API and cache it
        data = self.client.get_activity_details(activity_id)
        self._write_to_cache(activity_id, data)
        return data

    def get_run_activities(
        self, 
        total: int = 10, 
        page_limit: int = 20
    ) -> List[RunActivity]:
        activities = []
        start = 0
        
        while True:
            # Get activities for current page
            limit = page_limit if total == -1 else min(page_limit, total - len(activities))
            page_activities = self.client.get_activities(start, limit)
            
            # Filter running activities
            running_activities = [
                activity for activity in page_activities
                if activity["activityType"]["typeKey"] in ["running", "treadmill_running"]
            ]
            
            activities.extend(running_activities)
            
            # Break if we got fewer activities than requested (no more available)
            if len(page_activities) < page_limit:
                break
                
            # Break if we've reached the requested total (unless total is -1)
            if total != -1 and len(activities) >= total:
                break
                
            start += page_limit
        
        # Trim to requested total if needed and total is not -1
        activities = activities if total == -1 else activities[:total]
        activities = [
            RunActivity.from_garmin_activity(_a)
            for _a in activities
        ]

        return activities
    