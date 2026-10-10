
stage('API Tests') {
    steps {
        sh '''
            set -eu

            docker rm -f crop-yield-test-runner 2>/dev/null || true

            docker run -d \
                --name crop-yield-test-runner \
                python:3.12-slim \
                sh -c "sleep 600"

            docker exec crop-yield-test-runner mkdir -p /app

            docker cp "$WORKSPACE/." crop-yield-test-runner:/app/

            docker exec -w /app crop-yield-test-runner \
                pip install --no-cache-dir -r requirements.txt pytest httpx

            docker exec -w /app crop-yield-test-runner \
                python -m pytest tests/test_api.py -v

            docker rm -f crop-yield-test-runner
        '''
    }
}
