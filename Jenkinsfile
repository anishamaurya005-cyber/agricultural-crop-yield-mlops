pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo "Project workspace: ${WORKSPACE}"
                sh 'ls -la'
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