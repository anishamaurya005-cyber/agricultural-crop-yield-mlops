
node {
    try {
        stage('Checkout') {
            checkout scm
            echo "Workspace: ${env.WORKSPACE}"
        }

        stage('Prepare Model') {
            sh '''
                set -eu

                SOURCE="/workspace/models/crop_yield_model_mlflow.pkl"
                DEST="$WORKSPACE/models/crop_yield_model_mlflow.pkl"

                test -f "$SOURCE" || {
                    echo "Model file not found: $SOURCE"
                    exit 1
                }

                mkdir -p "$WORKSPACE/models"
                cp "$SOURCE" "$DEST"
                ls -lh "$DEST"
            '''
        }

        stage('API Tests') {
            sh '''
                set -eu

                docker rm -f crop-yield-test-runner 2>/dev/null || true

                docker run -d \
                    --name crop-yield-test-runner \
                    python:3.12-slim \
                    sh -c "sleep 600"

                docker cp "$WORKSPACE/." crop-yield-test-runner:/app/

                docker exec -w /app crop-yield-test-runner \
                    pip install --no-cache-dir -r requirements.txt pytest httpx

                docker exec -w /app crop-yield-test-runner \
                    python -m pytest tests/test_api.py -v
            '''
        }

        stage('Docker Build') {
            sh 'docker build -t crop-yield-api:latest .'
        }

        echo 'SUCCESS: Pipeline completed!'
    } finally {
        sh 'docker rm -f crop-yield-test-runner 2>/dev/null || true'
    }
}
