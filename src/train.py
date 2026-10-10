import pandas as pd
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
# 2. Define features and target
# -----------------------------

X = df.drop(columns=["value_hg_ha"])
y = df["value_hg_ha"]

print("\nFeatures:")
print(X.columns.tolist())

print("\nTarget: value_hg_ha")


# -----------------------------
# 3. Define column types
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
# 5. Create ML pipeline
# -----------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    n_jobs=-1
)

pipeline = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("model", model)
    ]
)


# -----------------------------
# 6. Train-test split
# -----------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------
# 7. Train model
# -----------------------------

print("\nTraining model...")

pipeline.fit(X_train, y_train)


# -----------------------------
# 8. Predictions
# -----------------------------

y_pred = pipeline.predict(X_test)


# -----------------------------
# 9. Evaluation
# -----------------------------

mae = mean_absolute_error(y_test, y_pred)

rmse = mean_squared_error(
    y_test,
    y_pred
) ** 0.5

r2 = r2_score(y_test, y_pred)


print("\n===== MODEL PERFORMANCE =====")

print(f"MAE  : {mae:.2f}")
print(f"RMSE : {rmse:.2f}")
print(f"R²   : {r2:.4f}")


# -----------------------------
# 10. Save model
# -----------------------------

MODEL_PATH = "models/crop_yield_model.pkl"

joblib.dump(pipeline, MODEL_PATH)

print(f"\nModel saved to: {MODEL_PATH}")