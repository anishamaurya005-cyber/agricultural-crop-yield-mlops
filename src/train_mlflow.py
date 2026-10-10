import pandas as pd
import mlflow
import mlflow.sklearn
import joblib

from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


# -----------------------------
# 1. Load dataset
# -----------------------------

DATA_PATH = "data/raw/df_yield_merged.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset shape:", df.shape)


# -----------------------------
# 2. Features and target
# -----------------------------

X = df.drop(columns=["value_hg_ha"])
y = df["value_hg_ha"]


# -----------------------------
# 3. Feature types
# -----------------------------

categorical_features = ["area", "item"]

numerical_features = [
    "year",
    "average_rain_fall_mm_per_year",
    "pesticides_tonnes",
    "avg_temp"
]


# -----------------------------
# 4. Preprocessing
# -----------------------------

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# -----------------------------
# 5. Model
# -----------------------------

n_estimators = 100

model = RandomForestRegressor(
    n_estimators=n_estimators,
    random_state=42,
    n_jobs=-1
)


# -----------------------------
# 6. Pipeline
# -----------------------------

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# -----------------------------
# 7. Train-test split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)


# -----------------------------
# 8. MLflow configuration
# -----------------------------

mlflow.set_experiment("Agricultural_Crop_Yield_Prediction")


with mlflow.start_run():

    print("\nTraining model...")

    pipeline.fit(X_train, y_train)

    # Predictions
    y_pred = pipeline.predict(X_test)

    # Metrics
    mae = mean_absolute_error(y_test, y_pred)

    rmse = mean_squared_error(
        y_test,
        y_pred
    ) ** 0.5

    r2 = r2_score(y_test, y_pred)

    # -------------------------
    # Log parameters
    # -------------------------

    mlflow.log_param("model", "RandomForestRegressor")
    mlflow.log_param("n_estimators", n_estimators)
    mlflow.log_param("random_state", 42)
    mlflow.log_param("test_size", 0.20)

    # -------------------------
    # Log metrics
    # -------------------------

    mlflow.log_metric("MAE", mae)
    mlflow.log_metric("RMSE", rmse)
    mlflow.log_metric("R2", r2)

    # -------------------------
    # Save model
    # -------------------------

    MODEL_PATH = "models/crop_yield_model_mlflow.pkl"

    joblib.dump(pipeline, MODEL_PATH)

    # Log model to MLflow
    mlflow.sklearn.log_model(
        pipeline,
        name="crop_yield_model",
        skops_trusted_types=[
            "sklearn.tree._tree.Tree"
        ]
    )

    print("\n===== MODEL PERFORMANCE =====")

    print(f"MAE  : {mae:.2f}")
    print(f"RMSE : {rmse:.2f}")
    print(f"R²   : {r2:.4f}")

    print("\nMLflow run completed successfully.")

    print(f"Model saved to: {MODEL_PATH}")