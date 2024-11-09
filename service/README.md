## Active energy forecast service

This directory contains an the API-based active energy time series predicition service.

To manually launch the service in a web server, you can use [uvicorn](https://www.tutorialspoint.com/fastapi/fastapi_uvicorn.htm).

### Launch service
```console
cd active-energy-prediction-time-series/service
uvicorn main:app --host 0.0.0.0 --port 8888 --reload
```

Now, the service listens for HTTP requests at the following URL addresses under port 8888:
- http://localhost:8888/
- http://127.0.0.1:8888/
- http://0.0.0.0:8888/
