
stage('Prepare Model') {
    steps {
        sh '''
            set -eu

            SOURCE="/workspace/models/crop_yield_model_mlflow.pkl"
            DEST="$WORKSPACE/models/crop_yield_model_mlflow.pkl"

            if [ ! -f "$SOURCE" ]; then
                echo "ERROR: Model not found at $SOURCE"
                exit 1
            fi
            docker exec jenkins sh -c "ls -lh /workspace/models/crop_yield_model_mlflow.pkl"
            cp "$SOURCE" "$DEST"
            ls -lh "$DEST"
            echo "Model copied into Jenkins workspace."
        '''
    }
}
