# Load-balancing service

This directory provides a set of tools to create a Load-balancing version of the provided forecast service, using a containerized [Nginx server](https://nginx.org/) as the service frontend and 4 forecast containers as the service backend. This setup balances inbound traffic reducing response time, improving service availability.

---

To launch a Load-balancing service, first you need to [install Docker](https://docs.docker.com/desktop/install/linux/) and [Docker Compose](https://docs.docker.com/compose/install/linux/).

After you setup Docker and launch the Docker service, use the following command to easily build the Docker Image and run all the Containers.

### To build the Docker image naming it "nepiskopos/power-lb" using the provided Dockerfile
```console
cd active-energy-prediction-time-series/load_balancer
docker-compose up
```

### To send a POST HTTP request to the application API on a running server using cURL and forecast using the ARIMA model:
```console
curl  -X 'POST' 'http://127.0.0.1:8888/api/arima_active_power_forecast_single'
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
```



### To send a POST HTTP request to the application API on a running server using cURL and forecast using Meta's Prophet model:
```console
curl  -X 'POST' 'http://127.0.0.1:8888/api/prophet_active_power_forecast_single'
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
```

The service response to the HTTP request is a JSON object which contains the predicted values under the "forecast" key.
