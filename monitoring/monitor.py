
import csv
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
LOG_FILE = BASE_DIR / "monitoring" / "prediction_log.csv"


def log_prediction(input_data, prediction):
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

    file_exists = LOG_FILE.exists()

    with open(LOG_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        if not file_exists:
            writer.writerow([
                "timestamp",
                "area",
                "year",
                "item",
                "rainfall",
                "pesticides",
                "avg_temp",
                "predicted_yield_hg_ha"
            ])

        writer.writerow([
            datetime.now().isoformat(timespec="seconds"),
            input_data["area"],
            input_data["year"],
            input_data["item"],
            input_data["average_rain_fall_mm_per_year"],
            input_data["pesticides_tonnes"],
            input_data["avg_temp"],
            round(float(prediction), 2)
        ])