from . import RunDataProvider

from ..schema.run_metric import RunMetric


class StrydZones(RunDataProvider):
    NAME = "StrydZones - Running Power Zones"
    APP_ID = "18fb2cf0-1a4b-430d-ad66-988c847421f4"
    AUTHOR = "StrydTeam"
    METRICS = [
        RunMetric(
            name="Vertical Oscillation Balance",
            unit="Centimeters",
            description="",
            developer_field_number=32,
            app_name=NAME
        ),
        RunMetric(
            name="Form Power",
            unit="Watts",
            description="Form Power is an additional component of running power relating to vertical oscillation and cadence. It is also weight-dependent.",
            developer_field_number=8,
            app_name=NAME
        ),
        RunMetric(
            name="Air Power",
            unit="Watts",
            description="The cost of overcoming air resistance into the total power value in real-time.",
            developer_field_number=11,
            app_name=NAME
        ),
        RunMetric(
            name="Temperature",
            unit="°C",
            description="Run temperature",
            developer_field_number=16,
            app_name=NAME
        ),
        RunMetric(
            name="Impact Loading Rate Balance",
            unit="%",
            description="",
            developer_field_number=30,
            app_name=NAME
        ),
        RunMetric(
            name="Power",
            unit="Watts",
            description="Running power",
            developer_field_number=0,
            app_name=NAME
        ),
        RunMetric(
            name="Leg Spring Stiffness",
            unit="kN/m",
            description="Leg Spring Stiffness (LSS) is a model of elastic energy in the leg, assuming it acts like a spring. It is the maximum vertical force a person generates in a step divided by the displacement during ground contact time.",
            developer_field_number=9,
            app_name=NAME
        ),
        RunMetric(
            name="Humidity",
            unit="%",
            description="Humidity",
            developer_field_number=15,
            app_name=NAME
        ),
        RunMetric(
            name="Impact Loading Rate",
            unit="bw/sec",
            description="The initial rate of increase in vertical (or perpendicular) force as a runner contacts the ground with their foot. It is reported in the units of body weight per second (bw/sec)",
            developer_field_number=24,
            app_name=NAME
        ),
        RunMetric(
            name="Leg Spring Stifness Balance",
            unit="%",
            description="",
            developer_field_number=31,
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
