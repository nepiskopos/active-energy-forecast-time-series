from locust import HttpUser, task, between
import json
import time


single = {
    'current': 1,
    'voltage': 2,
    'reactive_power': 3,
    'apparent_power': 4,
    'power_factor': 5,
    'main': "Haze",
    # 'description': "haze",
    # 'temp': 6,
    'feels_like': 7,
    'temp_min': 8,
    'temp_max': 9,
    'pressure': 10,
    'humidity': 11,
    'speed': 12,
    'deg': 13,
}

multi = {
    'steps': 2,
    'current': [
        1, 2
    ],
    'voltage': [
        3, 4
    ],
    'reactive_power': [
        5, 6
    ],
    'apparent_power': [
        7, 8
    ],
    'power_factor': [
        9, 10
    ],
    'main': [
        "Haze", "Haze"
    ],
    # 'description': [
    #     "haze", "haze"
    # ],
    # 'temp': [
    #     11, 12
    # ],
    'feels_like': [
        13, 14
    ],
    'temp_min': [
        15, 16
    ],
    'temp_max': [
        17, 18
    ],
    'pressure': [
        19, 20
    ],
    'humidity': [
        21, 22
    ],
    'speed': [
        23, 24
    ],
    'deg': [
        25, 26
    ],
}

class QuickstartUser(HttpUser):
    wait_time = between(1, 5)

    @task
    def arima_active_power_forecast_single(self):
        self.client.post("/api/arima_active_power_forecast_single", json=single, headers={"accept": "application/json", "Content-Type": "application/json"})

    @task
    def arima_active_power_forecast_multi(self):
        self.client.post("/api/arima_active_power_forecast_multi", json=multi, headers={"accept": "application/json", "Content-Type": "application/json"})

    @task
    def prophet_active_power_forecast_single(self):
        self.client.post("/api/prophet_active_power_forecast_single", json=single, headers={"accept": "application/json", "Content-Type": "application/json"})

    @task
    def prophet_active_power_forecast_multi(self):
        self.client.post("/api/prophet_active_power_forecast_multi", json=multi, headers={"accept": "application/json", "Content-Type": "application/json"})
