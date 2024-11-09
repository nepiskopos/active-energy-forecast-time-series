from fastapi.testclient import TestClient
from service.main import app
import json


client = TestClient(app)


def test_arima_predict_single():
    url='/api/arima_active_power_forecast_single'
    headers={'accept': 'application/json',  'Content-Type': 'application/json'}
    data={
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

    response = client.post(url=url, content=json.dumps(data, indent=2))
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['forecast']
    assert type(response_json['forecast']) == float


def test_arima_predict_multi():
    url='/api/arima_active_power_forecast_multi'
    headers={'accept': 'application/json',  'Content-Type': 'application/json'}
    data={
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

    response = client.post(url=url, content=json.dumps(data, indent=2))
    response_json = response.json()
    assert response.status_code == 200
    assert response_json['forecast']
    assert type(response_json['forecast']) == list


def test_prophet_predict_single():
    url='/api/prophet_active_power_forecast_single'
    headers={'accept': 'application/json',  'Content-Type': 'application/json'}
    data={
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

    response = client.post(url=url, content=json.dumps(data, indent=2))
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['forecast']
    assert type(response_json['forecast']) == float


def test_prophet_predict_multi():
    url='/api/prophet_active_power_forecast_multi'
    headers={'accept': 'application/json',  'Content-Type': 'application/json'}
    data={
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

    response = client.post(url=url, content=json.dumps(data, indent=2))
    response_json = response.json()

    assert response.status_code == 200
    assert response_json['forecast']
    assert type(response_json['forecast']) == list
    assert all(isinstance(x, float) for x in response_json['forecast'])
