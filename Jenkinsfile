
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "Project workspace: ${WORKSPACE}"
                sh 'ls -la'
            }
        }

        stage('Prepare Model') {
            steps {
                sh '''
                    set -e

                    MODEL_DIR="/var/jenkins_home/workspace/Crop-Yield-MLOps-Pipeline/models"

                    if [ ! -f "$MODEL_DIR/crop_yield_model_mlflow.pkl" ]; then
                        echo "ERROR: Model file is missing."
                        exit 1
                    fi

                    ls -lh "$MODEL_DIR/crop_yield_model_mlflow.pkl"
                    echo "Model file is available."
                '''
            }
        }

        stage('API Tests') {
            steps {
                sh '''
                    set -e
                    docker rm -f crop-yield-test-runner 2>/dev/null || true

                    docker create \
                      --name crop-yield-test-runner \
                      -w /app \
                      python:3.12-slim \
                      sh -c "pip install --no-cache-dir -r requirements.txt pytest httpx && python -m pytest tests/test_api.py -v"

                    docker cp "$WORKSPACE/." crop-yield-test-runner:/app/
                    docker cp "C:/Users/Admin/Desktop/agricultural-crop-yield-mlops/models/crop_yield_model_mlflow.pkl" crop-yield-test-runner:/app/models/crop_yield_model_mlflow.pkl

                    docker start -a crop-yield-test-runner
                    docker rm -f crop-yield-test-runner
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
            echo 'SUCCESS: API tests passed and Docker image built.'
        }
        failure {
            echo 'FAILED: Check the console output for the error.'
        }
    }
}
