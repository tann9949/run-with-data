from . import RunDataProvider

from ..schema.run_metric import RunMetric


class RunPowerModel(RunDataProvider):

    NAME = "RunPowerModel - Wrist-Based Running Power Meter"
    APP_ID = "6ac39398-29fa-4183-a9ac-8396ce941446"
    AUTHOR = "MarkusHoller"
    METRICS = [
        RunMetric(
            name="Running Power",
            unit="Watt",
            description="Running power",
            developer_field_number=0,
            app_name=NAME
        ),
        RunMetric(
            name="Trail Score",
            unit="%",
            description="Trail score",
            developer_field_number=1,
            app_name=NAME
        ),
        RunMetric(
            name="Running Score",
            unit="%",
            description="Running score",
            developer_field_number=2,
            app_name=NAME
        ),
    ]

    def __init__(self) -> None:
        super().__init__(
            name=self.NAME,
            app_id=self.APP_ID,
            author=self.AUTHOR,
            metrics=self.METRICS,
        )
