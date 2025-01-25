import os
from time import sleep
from typing import List, Tuple

import requests


def get_elevation_data(coordinates: List[Tuple[float, float]]) -> List[float]:
    """
    Get elevation data for a list of coordinates using Google Maps Elevation API.
    
    Args:
        coordinates: List of (latitude, longitude) tuples
        
    Returns:
        List of elevation values in meters
        
    Raises:
        ValueError: If API key is not set or API request fails
    """
    api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    if not api_key:
        raise ValueError("GOOGLE_MAPS_API_KEY environment variable is not set")
    
    base_url = "https://maps.googleapis.com/maps/api/elevation/json"
    elevations = []
    
    # Google Maps API has a limit of 500 locations per request
    batch_size = 500
    
    for i in range(0, len(coordinates), batch_size):
        batch = coordinates[i:i + batch_size]
        
        # Format coordinates for API request
        locations = "|".join(f"{lat},{lng}" for lat, lng in batch)
        
        params = {
            'locations': locations,
            'key': api_key
        }
        
        response = requests.get(base_url, params=params)
        
        if response.status_code != 200:
            raise ValueError(f"API request failed with status code {response.status_code}")
        
        data = response.json()
        
        if data['status'] != 'OK':
            raise ValueError(f"API request failed with status: {data['status']}")
        
        batch_elevations = [result['elevation'] for result in data['results']]
        elevations.extend(batch_elevations)
        
        # Add a small delay to respect API rate limits
        if i + batch_size < len(coordinates):
            sleep(0.1)
    
    return elevations
