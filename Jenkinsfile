
pipeline {
    agent any

    stages {
        stage('Prepare Model') {
            steps {
                sh '''
                    set -eu

                    SOURCE="/workspace/models/crop_yield_model_mlflow.pkl"
                    DEST="$WORKSPACE/models/crop_yield_model_mlflow.pkl"

                    if [ ! -f "$SOURCE" ]; then
                        echo "ERROR: Model file not found at $SOURCE"
                        exit 1
                    fi

                    mkdir -p "$WORKSPACE/models"
                    cp "$SOURCE" "$DEST"

                    ls -lh "$DEST"
                    echo "Model prepared successfully."
                '''
            }
        }

        stage('API Tests') {
            steps {
                sh '''
                    set -eu

                    docker rm -f crop-yield-test-runner 2>/dev/null || true

                    docker run -d \
                        --name crop-yield-test-runner \
                        -v "$WORKSPACE:/app" \
                        -w /app \
                        python:3.12-slim \
                        sh -c "sleep 600"

                    docker exec crop-yield-test-runner \
                        pip install --no-cache-dir -r requirements.txt pytest httpx

                    docker exec crop-yield-test-runner \
                        python -m pytest tests/test_api.py -v

                    docker rm -f crop-yield-test-runner
                '''
            }
        }

        stage('Docker Build') {
            steps {
                sh '''
                    docker build -t crop-yield-api:latest .
                '''
            }
        }
    }

    post {
        success {
            echo 'SUCCESS: Crop Yield MLOps pipeline completed.'
        }
        failure {
            echo 'FAILED: Check the Console Output for details.'
        }
    }
}
