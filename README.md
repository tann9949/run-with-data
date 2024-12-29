# 🏃‍♂️ Running Dot

A Python package for analyzing running data from Garmin Connect, with a focus on comparing different running power metrics (Stryd, Garmin, RunPowerModel).

## 🛠️ Features

- Fetch running activities from Garmin Connect
- Compare power metrics from different sources:
  - Stryd Running Power
  - Garmin Running Power
  - RunPowerModel (third-party CIQ app)
- Cache activity details locally to minimize API calls
- Support for various running metrics including:
  - Power
  - Speed/Pace
  - Cadence
  - Ground Contact Time
  - Vertical Oscillation
  - And more...

## 📦 Installation

1. Clone this repository
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file with your Garmin credentials:
```
GARMIN_EMAIL=your.email@example.com
GARMIN_PASSWORD=your_password
```

## 🔄 Usage

Here's a basic example of fetching running activities and analyzing power data:

```python
from running_dot.client.garmin import GarminClient
from running_dot.utils import get_power_indices

# Initialize client
client = GarminClient()

# Get last 10 running activities
activities = client.get_run_activities(total=10)

# Load details for first activity
activity = activities[0]
activity.load_details(client)

# Get power data indices
power_indices = get_power_indices(activity)

# Access different power metrics
stryd_power = activity.run_metrics[power_indices["stryd"]].value
garmin_power = activity.run_metrics[power_indices["garmin"]].value
rpm_power = activity.run_metrics[power_indices["runpowermodel"]].value
```

## 🌐 Project Structure

- `running_dot/`
  - `client/` - API client implementations
  - `data_field/` - Data field definitions for different metrics
  - `schema/` - Data models and schemas
  - `utils.py` - Utility functions

## 📊 Dependencies

Key dependencies include:

```1:6:requirements.txt
garminconnect
matplotlib
numpy
pandas
folium
tqdm
```

## 🛡️ Cache

Activity details are cached locally to minimize API calls. Cache location:

```15:18:running_dot/client/garmin.py
    def __init__(self, cache_dir: str = "~/.cache/garmin_activities") -> None:
        super().__init__()
        self.cache_dir = os.path.expanduser(cache_dir)
        self.details_cache_dir = os.path.join(self.cache_dir, "details")
```

## 📚 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📃 License

MIT License

## 💖 Acknowledgments

- [Garmin Connect API](https://connect.garmin.com/)
- [Stryd](https://www.stryd.com/)
- [RunPowerModel CIQ App](https://apps.garmin.com/en-US/apps/6ac39398-29fa-4183-a9ac-8396ce941446)

## 👤 Author
Chompakorn Chaksangchaichot
