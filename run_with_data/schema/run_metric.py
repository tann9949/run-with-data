from typing import Any, Sequence, Optional, Literal

import matplotlib.pyplot as plt
import numpy as np
from pydantic import BaseModel, field_validator


def ms_to_pace(speed_ms: float, unit: Literal["km", "mi"] = "km") -> Optional[str]:
    """
    Convert speed in meters/second to pace in min/km format
    
    Args:
        speed_ms (float): Speed in meters per second
    
    Returns:
        str: Pace in format "MM:SS min/km"
    """
    if speed_ms <= 0:
        return None
    
    # Calculate minutes per kilometer
    # 1 km = 1000m, so time for 1km = 1000/speed
    # Convert seconds to minutes by dividing by 60
    minutes_per_km = (1000 / speed_ms) / 60
    
    # Split into whole minutes and remaining seconds
    whole_minutes = int(minutes_per_km)
    seconds = int((minutes_per_km - whole_minutes) * 60)

    whole_minutes*60
    
    if unit == "km":
        return f"{whole_minutes}:{seconds:02d} min/km"
    elif unit == "mi":
        return f"{whole_minutes}:{seconds:02d} min/mi"
    else:
        raise ValueError(f"Invalid unit: {unit}")


class PaceMinPerKm(BaseModel):
    minute: int
    second: int
    mps: Optional[float] = None  # Made optional with default None

    def __post_init__(self) -> None:
        if self.mps is None:
            self.mps = self.to_mps()

    @classmethod
    def from_mps(cls, mps: float) -> "PaceMinPerKm":
        pace = ms_to_pace(mps, unit="km")
        if pace is None:
            return cls(minute=0, second=0)
        pace = pace.split()[0]
        minute, second = pace.split(":")
        return cls(minute=int(minute), second=int(second), mps=mps)
    
    def to_mps(self) -> float:
        """
        Convert pace (minutes and seconds per kilometer) to meters per second
        
        Returns:
            float: Speed in meters per second
        """
        if self.minute == 0 and self.second == 0:
            return 0.
        # Convert pace to total seconds per kilometer
        total_seconds = (self.minute * 60) + self.second
        
        # Convert to meters per second:
        # 1 km = 1000m
        # speed = distance/time
        mps = 1000 / total_seconds
        
        # Update the mps field
        self.mps = mps
        return mps
    
    def __repr__(self) -> str:
        return f"{self.minute:02d}:{self.second:02d} min/km"


class RunMetric(BaseModel):
    name: str
    unit: str
    description: str
    key: Optional[str] = None
    developer_field_number: Optional[int] = None
    value: Optional[np.ndarray] = None
    app_name: str = "Garmin" # default field value from garmin

    class Config:
        arbitrary_types_allowed = True  # This allows numpy arrays

    @field_validator("value")
    def validate_numpy_array(cls, v):
        if v is None:
            return v
        if not isinstance(v, np.ndarray):
            try:
                return np.array(v)
            except Exception as e:
                raise ValueError(f"Could not convert to numpy array: {e}")
        return v

    def __init__(self, **data):
        super().__init__(**data)
        if self.key is None and self.developer_field_number is None:
            raise ValueError(f"Both key and developer_field_number can't be None")

    @property
    def is_connect_iq_field(self) -> bool:
        return self.developer_field_number is not None
    
    @property
    def is_garmin_field(self) -> bool:
        return not self.is_connect_iq_field
    
    def set_value(self, value: np.ndarray):
        self.value = value

    def plot(self, x: Optional[Sequence[Any]] = None) -> None:
        if self.value is not None:
            if x:
                if len(x) != len(self.value):
                    raise ValueError(f"x value provided length aren't match. Expected {len(self.value)} but got {len(x)}")
                plt.plot(x, self.value)
            else:
                plt.plot(self.value)
            plt.title(
                self.name if self.is_garmin_field else self.name + "\n(" + self.app_name + ")"
            )
            plt.ylabel(self.unit)
            plt.show()
