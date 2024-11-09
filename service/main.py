from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from prophet.serialize import model_from_json
from pydantic import BaseModel
from statsmodels.tsa.arima.model import ARIMAResults
from typing import List

import os
import pandas as pd
import pickle


# Defining input parameters types
class model_input_single(BaseModel):
    current : float
    voltage : float
    reactive_power : float
    apparent_power : float
    power_factor : float
    main : str
    # description : str
    # temp : float
    feels_like : float
    temp_min : float
    temp_max : float
    pressure : int
    humidity : int
    speed : float
    deg : int

# Defining input parameters types
class model_input_multi(BaseModel):
    steps : int
    current : List[float]
    voltage : List[float]
    reactive_power : List[float]
    apparent_power : List[float]
    power_factor : List[float]
    main : List[str]
    # description : List[str]
    # temp : List[float]
    feels_like : List[float]
    temp_min : List[float]
    temp_max : List[float]
    pressure : List[int]
    humidity : List[int]
    speed : List[float]
    deg : List[int]


category_mapping = None
# Load mapping between sky status categorical and numerical values
with open(os.path.join(os.path.dirname(__file__), 'models/category_mapping.pkl'), 'rb') as f:
    category_mapping = pickle.load(f)


# Load stored ARIMA model
model_arima = ARIMAResults.load(os.path.join(os.path.dirname(__file__), 'models/model_arima.pkl'))


# Load stored Prophet model
model_prophet = None
with open(os.path.join(os.path.dirname(__file__), 'models/model_prophet.json'), 'r') as fin:
    model_prophet = model_from_json(fin.read())


# Define a new FastAPI object
app = FastAPI()


# Define the behaviour of a POST request to the /api/active_power_forecast_single server path
@app.post('/api/arima_active_power_forecast_single', tags=['single-step active power forecast using ARIMA'])
async def active_power_forecast_single(input_data: model_input_single, response: JSONResponse):
    '''
    Predict the next (single) timeseries point, i.e. the next Active Power
    measurement, based on exogenous data, using an ARIMA model.

    **Input**:  A list of 13 key-value pairs (like Python's dictionary) using
            the data ("body") part of the HTTP POST request. Each key is a
            exogeneous parameter and each value is the respective measurement
            for said parameter. The acceptable exogeneous input parameters
            are the following:
    * current (float number)
    * voltage (float number)
    * reactive_power (float number)
    * apparent_power (float number)
    * power_factor (float number)
    * main (string - possible values: clear, clouds, drizzle, fog, haze, mist, rain, thunderstorm)
    * feels_like (float number)
    * temp_min (float number)
    * temp_max (float number)
    * pressure (integer number)
    * humidity (integer number)
    * speed (float number)
    * deg (integer number)

    **Returns**: A JSON object which contains the predicted value under the
                "forecast" key.

    **API test using cURL**:\n
        curl -X 'POST' 'http://SERVER_IP_ADDRESS:PORT/api/arima_active_power_forecast_single'
                -H 'accept: application/json'
                -H 'Content-Type: application/json'
                -d '{
                        "current": CURRENT_VALUE,
                        "voltage": VOLTAGE_VALUE,
                        "reactive_power": REACTIVE_POWER_VALUE,
                        "apparent_power": APPARENT_POWER_VALUE,
                        "power_factor": POWER_FACTOR_VALUE,
                        "main": "MAIN_VALUE",
                        "feels_like": FEELS_LIKE_VALUE,
                        "temp_min": TEMP_MIN_VALUE,
                        "temp_max": TEMP_MAX_VALUE,
                        "pressure": PRESSURE_VALUE,
                        "humidity": HUMIDITY_VALUE,
                        "speed": SPEED_VALUE,
                        "deg": DEG_VALUE,
                    }'
    '''
    data = input_data.model_dump()

    df = pd.DataFrame(data=data, index=[0])

    df['main'] = df['main'].apply(lambda x: category_mapping[x.lower()])
    # df['description'] = df['description'].apply(lambda x: category_mapping[x])

    forecast = model_arima.forecast(steps=1, exog=df)
    ret_val = round(forecast.iloc[0], 1)

    return JSONResponse(content={"forecast": ret_val}, status_code=status.HTTP_200_OK)

# Response(content={"forecast": ret_val}, status_code=200, media_type='application/json')


# Define the behaviour of a POST request to the /api/active_power_forecast_multi server path
@app.post('/api/arima_active_power_forecast_multi', tags=['multi-step active power forecast using ARIMA'])
async def active_power_forecast_multi(input_data: model_input_multi, response: JSONResponse):
    '''
    Predict the a number of next timeseries points, i.e. the next Active
    Power measurements, based on exogenous data, using an ARIMA model.

    **Input**: A list of 13 key-value pairs (like Python's dictionary) using
           the data ("body") part of the HTTP POST request. Each key is a
           exogeneous parameter and each value is a list with the respective
           measurement for said parameter. The acceptable exogeneous
           parameters are the following:
    * current (list of float numbers)
    * voltage (list of float numbers)
    * reactive_power (list of float numbers)
    * apparent_power (list of float numbers)
    * power_factor (list of float numbers)
    * main (list of strings - possible values: clear, clouds, drizzle, fog, haze, mist, rain, thunderstorm)
    * feels_like (list of float numbers)
    * temp_min (list of float numbers)
    * temp_max (list of float numbers)
    * pressure (list of integer numbers)
    * humidity (list of integer numbers)
    * speed (list of float numbers)
    * deg (list of integer numbers)

    **Returns**: A JSON object which contains the predicted value under the
             "forecast" key.

    **API test using curl**:\n
        curl -X 'POST' 'http://SERVER_IP_ADDRESS:PORT/api/arima_active_power_forecast_multi'
             -H 'accept: application/json'
             -H 'Content-Type: application/json'
             -d '{
                     "current": [CURRENT_VALUE_1, CURRENT_VALUE_2, ...],
                     "voltage": [VOLTAGE_VALUE_1, VOLTAGE_VALUE_2, ...],
                     "reactive_power": [REACTIVE_POWER_VALUE_1, REACTIVE_POWER_VALUE_2, ...],
                     "apparent_power": [APPARENT_POWER_VALUE_1, APPARENT_POWER_VALUE_2, ...],
                     "power_factor": [POWER_FACTOR_VALUE_1, POWER_FACTOR_VALUE_2, ...],
                     "main": ["MAIN_VALUE_1", "MAIN_VALUE_2", ...],
                     "feels_like": [FEELS_LIKE_VALUE_1, FEELS_LIKE_VALUE_2, ...],
                     "temp_min": [TEMP_MIN_VALUE_1, TEMP_MIN_VALUE_2, ...],
                     "temp_max": [TEMP_MAX_VALUE_1, TEMP_MAX_VALUE_2, ...],
                     "pressure": [PRESSURE_VALUE_1, PRESSURE_VALUE_2, ...],
                     "humidity": [HUMIDITY_VALUE_1, HUMIDITY_VALUE_2, ...],
                     "speed": [SPEED_VALUE_1, SPEED_VALUE_2, ...],
                     "deg": [DEG_VALUE_1, DEG_VALUE_2, ...],
                 }'
    '''
    data = input_data.model_dump()

    steps = data['steps']
    del data['steps']

    df = pd.DataFrame(data=data, index=list(range(steps))) # Predict for the next n minutes
    df['main'] = df['main'].apply(lambda x: category_mapping[x.lower()])
    # df['description'] = df['description'].apply(lambda x: category_mapping[x])

    forecast = model_arima.forecast(steps=steps, exog=df)
    ret_val = [round(x, 1) for x in forecast.to_list()]

    return JSONResponse(content={"forecast": ret_val}, status_code=status.HTTP_200_OK)


# Define the behaviour of a POST request to the /api/active_power_forecast_single server path
@app.post('/api/prophet_active_power_forecast_single', tags=['single-step active power forecast using Meta\'s Prohet'])
async def active_power_forecast_single(input_data: model_input_single, response: JSONResponse):
    '''
    Predict the next (single) timeseries point, i.e. the next Active Power
    measurement, based on exogenous data, using Meta's Prophet model.

    **Input**:  A list of 13 key-value pairs (like Python's dictionary) using
            the data ("body") part of the HTTP POST request. Each key is a
            exogeneous parameter and each value is the respective measurement
            for said parameter. The acceptable exogeneous input parameters
            are the following:
    * current (float number)
    * voltage (float number)
    * reactive_power (float number)
    * apparent_power (float number)
    * power_factor (float number)
    * main (string - possible values: clear, clouds, drizzle, fog, haze, mist, rain, thunderstorm)
    * feels_like (float number)
    * temp_min (float number)
    * temp_max (float number)
    * pressure (integer number)
    * humidity (integer number)
    * speed (float number)
    * deg (integer number)

    **Returns**: A JSON object which contains the predicted value under the
                "forecast" key.

    **API test using cURL**:\n
        curl -X 'POST' 'http://SERVER_IP_ADDRESS:PORT/api/arima_active_power_forecast_single'
                -H 'accept: application/json'
                -H 'Content-Type: application/json'
                -d '{
                        "current": CURRENT_VALUE,
                        "voltage": VOLTAGE_VALUE,
                        "reactive_power": REACTIVE_POWER_VALUE,
                        "apparent_power": APPARENT_POWER_VALUE,
                        "power_factor": POWER_FACTOR_VALUE,
                        "main": "MAIN_VALUE",
                        "feels_like": FEELS_LIKE_VALUE,
                        "temp_min": TEMP_MIN_VALUE,
                        "temp_max": TEMP_MAX_VALUE,
                        "pressure": PRESSURE_VALUE,
                        "humidity": HUMIDITY_VALUE,
                        "speed": SPEED_VALUE,
                        "deg": DEG_VALUE,
                    }'
    '''
    data = input_data.model_dump()

    df = model_prophet.make_future_dataframe(periods=1, freq='1min', include_history=False) # Predict for the next minute

    for k, v in data.items():
        df[k] = [v]

    df['main'] = df['main'].apply(lambda x: category_mapping[x.lower()])
    # df['description'] = df['description'].apply(lambda x: category_mapping[x])

    forecast = model_prophet.predict(df)
    ret_val = round(forecast['yhat'].iloc[0], 1)

    return JSONResponse(content={"forecast": ret_val}, status_code=status.HTTP_200_OK)


# Define the behaviour of a POST request to the /api/active_power_forecast_multi server path
@app.post('/api/prophet_active_power_forecast_multi', tags=['multi-step active power forecast using Meta\'s Prohet'])
async def active_power_forecast_multi(input_data: model_input_multi, response: JSONResponse):
    '''
    Predict the a number of next timeseries points, i.e. the next Active
    Power measurements, based on exogenous data, using Meta's Prophet model.

    **Input**: A list of 13 key-value pairs (like Python's dictionary) using
           the data ("body") part of the HTTP POST request. Each key is a
           exogeneous parameter and each value is a list with the respective
           measurement for said parameter. The acceptable exogeneous
           parameters are the following:
    * current (list of float numbers)
    * voltage (list of float numbers)
    * reactive_power (list of float numbers)
    * apparent_power (list of float numbers)
    * power_factor (list of float numbers)
    * main (list of strings - possible values: clear, clouds, drizzle, fog, haze, mist, rain, thunderstorm)
    * feels_like (list of float numbers)
    * temp_min (list of float numbers)
    * temp_max (list of float numbers)
    * pressure (list of integer numbers)
    * humidity (list of integer numbers)
    * speed (list of float numbers)
    * deg (list of integer numbers)

    **Returns**: A JSON object which contains the predicted value under the
             "forecast" key.

    **API test using cURL**:\n
        curl -X 'POST' 'http://SERVER_IP_ADDRESS:PORT/api/prophet_active_power_forecast_multi'
             -H 'accept: application/json'
             -H 'Content-Type: application/json'
             -d '{
                     "current": [CURRENT_VALUE_1, CURRENT_VALUE_2, ...],
                     "voltage": [VOLTAGE_VALUE_1, VOLTAGE_VALUE_2, ...],
                     "reactive_power": [REACTIVE_POWER_VALUE_1, REACTIVE_POWER_VALUE_2, ...],
                     "apparent_power": [APPARENT_POWER_VALUE_1, APPARENT_POWER_VALUE_2, ...],
                     "power_factor": [POWER_FACTOR_VALUE_1, POWER_FACTOR_VALUE_2, ...],
                     "main": ["MAIN_VALUE_1", "MAIN_VALUE_2", ...],
                     "feels_like": [FEELS_LIKE_VALUE_1, FEELS_LIKE_VALUE_2, ...],
                     "temp_min": [TEMP_MIN_VALUE_1, TEMP_MIN_VALUE_2, ...],
                     "temp_max": [TEMP_MAX_VALUE_1, TEMP_MAX_VALUE_2, ...],
                     "pressure": [PRESSURE_VALUE_1, PRESSURE_VALUE_2, ...],
                     "humidity": [HUMIDITY_VALUE_1, HUMIDITY_VALUE_2, ...],
                     "speed": [SPEED_VALUE_1, SPEED_VALUE_2, ...],
                     "deg": [DEG_VALUE_1, DEG_VALUE_2, ...],
                 }'
    '''
    data = input_data.model_dump()

    steps = data['steps']
    del data['steps']

    df = model_prophet.make_future_dataframe(periods=steps, freq='1min', include_history=False) # Predict for the next n minutes

    for k, v in data.items():
        df[k] = v

    df['main'] = df['main'].apply(lambda x: category_mapping[x.lower()])
    # df['description'] = df['description'].apply(lambda x: category_mapping[x])

    forecast = model_prophet.predict(df)
    ret_val = [round(x, 1) for x in forecast['yhat'].to_list()]

    return JSONResponse(content={"forecast": ret_val}, status_code=status.HTTP_200_OK)


if __name__ == '__main__':
    uvicorn.run(app, host = '0.0.0.0', port=8000)
