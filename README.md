# Active energy forecast (time series) using ARIMA and Prophet

This repository contains an API-based active energy time series predicition solution, using ARIMA and Prophet.

The solution predicts the next N values / steps for active power, based on the [provided dataset](https://data.mendeley.com/datasets/tvhygj8rgg/).

The provided dataset using exogenous data / exogenous regressor for forecasting.

Both [ARIMA](https://en.wikipedia.org/wiki/Autoregressive_integrated_moving_average) and [Prophet](https://facebook.github.io/prophet/) are provided as base models options, the user can choose whichever they prefer.

---

To easily use this application, use the provided docker container, which contains all the required setup instructions and procedure to build and deploy this application to production.

For a scalable option, a dockerized load-balancer solution is provided, which spawns an Nginx server which redirects any incoming traffic to any of the 4 spawned docker containers backends.

---

To deploy the provided service, first you need to train the ARIMA and Prophet models.

The pre-trained models are not provided due to their huge size relative to GitHub's recommendations.

To manually train these models, you need to use the provided Jupyter notebooks.

Before running any of these notebooks, you need to download the provided dataset and place the included CSV file under the [train directory](train/). 

The correct order to run these notebooks are:
1. [EDA](train/eda.ipynb)
2. [Prophet](train/prophet.ipynb)
3. [ARIMA](train/arima.ipynb)

Then, you need to place the three generated models under the [service/models](service/models) directory.

The models have the following file names:
* category_mapping.pkl
* model_prophet.json
* model_arima.pkl

Then, you can either manually run the service using Python, or use Docker to create a service image and launch a container with a production-ready instance.

The dockerized solution is preferred.

---

To launch the service in a single docker container, first you need to [install Docker](https://docs.docker.com/desktop/install/linux/) and [buildx](https://docs.docker.com/reference/cli/docker/buildx/).

After you setup Docker and launch the Docker service, use the following commands to build the Docker Image and run the Container.

### To build the Docker image naming it "nepiskopos/power" using the provided Dockerfile
```console
cd active-energy-prediction-time-series
docker buildx build -t nepiskopos/power .
```

### To deploy the application to production using a Docker container named "power" which accepts network traffic in container port 8000 through host port 8888
```console
docker run -p 8888:8000 --name power nepiskopos/power
```

### To send a POST HTTP request to the application API on a running server using cURL and forecast using the ARIMA model:
```console
curl  -X 'POST' 'http://127.0.0.1:8888/api/arima_active_power_forecast_multi'
      -H 'accept: application/json'
      -H 'Content-Type: application/json'
      -d '{
            "steps": NUMBER_OF_PREDICTION_STEPS,
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
```



### To send a POST HTTP request to the application API on a running server using cURL and forecast using Meta's Prophet model:
```console
curl  -X 'POST' 'http://127.0.0.1:8888/api/prophet_active_power_forecast_multi'
      -H 'accept: application/json'
      -H 'Content-Type: application/json'
      -d '{
            "steps": NUMBER_OF_PREDICTION_STEPS,
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
```

The service response to the HTTP request is a JSON object which contains the predicted values under the "forecast" key.

---

To launch a Load-balancing service, first you need to [install Docker](https://docs.docker.com/desktop/install/linux/) and [Docker Compose](https://docs.docker.com/compose/install/linux/).

After you setup Docker and launch the Docker service, use the following command to easily build the Docker Image and run all the Containers.

### To build the Docker image naming it "nepiskopos/power-lb" using the provided Dockerfile
```console
cd active-energy-prediction-time-series/load_balancer
docker-compose up
```

Then, you can send POST HTTP requests to the application API and get the response as a JSON file, just like before, but this time more requests can be served in parallel.
