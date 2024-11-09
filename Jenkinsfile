pipeline {
    environment {
        imagename = "nepiskopos/power"
        dockerImage = ''
        containerName = 'power'
    }

    agent any

    stages {
        stage('Cloning Git') {
            steps {
                git([url: 'https://github.com/nepiskopos/active-energy-prediction-time-series.git', branch: 'main'])
            }
        }

        stage('Building image') {
            steps {
                script {
                    dockerImage = docker.build "${imagename}:latest"
                }
            }
        }

        stage('Running image') {
            steps {
                script {
                    sh "docker run -d -p 8888:8000 --name ${containerName} ${imagename}:latest"
                    sh "sleep 2"
                    sh '''curl  -X 'POST' 'http://0.0.0.0:8888/api/arima_active_power_forecast_single'
                                -H 'accept: application/json'
                                -H 'Content-Type: application/json'
                                -d '{
                                        "current": 1,
                                        "voltage": 2,
                                        "reactive_power": 3,
                                        "apparent_power": 4,
                                        "power_factor": 5,
                                        "main": "Clear",
                                        "feels_like": 6,
                                        "temp_min": 7,
                                        "temp_max": 8,
                                        "pressure": 9,
                                        "humidity": 10,
                                        "speed": 11,
                                        "deg": 12,
                                    }'
                        '''
                    sh '''curl  -X 'POST' 'http://0.0.0.0:8888/api/prophet_active_power_forecast_single'
                                -H 'accept: application/json'
                                -H 'Content-Type: application/json'
                                -d '{
                                        "current": 1,
                                        "voltage": 2,
                                        "reactive_power": 3,
                                        "apparent_power": 4,
                                        "power_factor": 5,
                                        "main": "Clear",
                                        "feels_like": 6,
                                        "temp_min": 7,
                                        "temp_max": 8,
                                        "pressure": 9,
                                        "humidity": 10,
                                        "speed": 11,
                                        "deg": 12,
                                    }'
                        '''
                    // Perform any additional steps needed while the container is running
                }
            }
        }

        stage('Stop and Remove Container') {
            steps {
                script {
                    sh "docker stop ${containerName} || true"
                    sh "docker rm ${containerName} || true"
                }
            }
        }
    }
}
