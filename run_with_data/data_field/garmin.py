import logging
from typing import Optional

from . import RunDataProvider
from . import RunMetric


class GarminDefaultField(RunDataProvider):
    NAME = "Default Garmin Field"
    APP_ID = "00000000-0000-0000-0000-000000000000"
    AUTHOR = "Garmin"
    METRICS = [
        RunMetric(
            name="Longitude",
            unit="Watt",
            description="Running power",
            key="directLongitude"
        ),
        RunMetric(
            name="Latitude",
            unit="Watt",
            description="Running power",
            key="directLatitude"
        ),
        RunMetric(
            name="Cadence",
            unit="spm",
            description="Number of steps per minutes",
            key="directDoubleCadence"
        ),
        RunMetric(
            name="Stride Length",
            unit="cm",
            description="Stride length",
            key="directStrideLength"
        ),
        RunMetric(
            name="Speed",
            unit="mps",
            description="Running speed in mps",
            key="directSpeed"
        ),
        RunMetric(
            name="Grade Adjusted Speed",
            unit="mps",
            description="Grade adjusted running speed (adjusted from elevation) in mps",
            key="directGradeAdjustedSpeed"
        ),
        RunMetric(
            name="Power",
            unit="Watt",
            description="Running power measured by Garmin",
            key="directPower"
        ),
        RunMetric(
            name="Heart Rate",
            unit="bpm",
            description="Measured heart rate from Garmin",
            key="directHeartRate"
        ),
        RunMetric(
            name="Timestamp",
            unit="milli epoch time",
            description="UNIX timestamp in milli epoch. Divide by 1000 to convert to second.",
            key="directTimestamp"
        ),
        RunMetric(
            name="Moving Duration",
            unit="second",
            description="Run Moving duration",
            key="sumMovingDuration"
        ),
        RunMetric(
            name="Total Distance",
            unit="meter",
            description="Total run distance",
            key="sumDistance"
        ),
        RunMetric(
            name="Vertical Speed",
            unit="mps",
            description="Vertical speed",
            key="directVerticalSpeed"
        ),
        RunMetric(
            name="Vertical Oscillation",
            unit="cm",
            description="Vertical Oscillation",
            key="directVerticalOscillation"
        ),
        RunMetric(
            name="Vertical Ratio",
            unit="%",
            description="Vertical speed",
            key="directVerticalRatio"
        ),
        RunMetric(
            name="Ground Contact Time",
            unit="ms",
            description="Ground contact time",
            key="directGroundContactTime"
        ),
        RunMetric(
            name="Ground Contact Balance",
            unit="%",
            description="Ground contact time left percentage. (You can get right by subtract from 100)",
            key="directGroundContactBalanceLeft"
        ),
        RunMetric(
            name="Respiration Rate",
            unit="bpm",
            description="Number of breaths per minute",
            key="directRespirationRate"
        ),
        RunMetric(
            name="Elevation",
            unit="m",
            description="Elevation gain",
            key="directElevation"
        )
    ]

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            app_id=self.APP_ID,
            author=self.AUTHOR,
            metrics=self.METRICS,
        )

    def __getitem__(self, key: str) -> Optional[RunMetric]:
        if key in self.fid2metric:
            return self.fid2metric[key]
        else:
            # logging.warning(f"Unknown key: {key}")
            return None
