
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Preparing Crop Yield Prediction project'
                sh 'pwd'
                sh 'ls -la'
            }
        }

        stage('API Tests') {
            steps {
                sh '''
                    docker run --rm \
                      -v "$WORKSPACE:/app" \
                      -w /app \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt pytest httpx && python -m pytest tests/test_api.py -v"
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t crop-yield-api:latest .'
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: API tests passed and Docker image was built.'
        }
        failure {
            echo 'FAILED: Check the stage logs for details.'
        }
    }
}