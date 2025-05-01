#For Google Collab
!pip install pytz
!pip install duckdb pyarrow pandas

import os
import time
import requests
import pandas as pd
from datetime import datetime
from pytz import timezone

# === CONFIGURATION (Google-Colab) ===
# Paste your JCDecaux API key here directly
API_KEY = "YOUR_API_KEY_HERE"
CONTRACT = "toulouse"
SAVE_DIR = "snapshots_velo"  # Folder in your Google Drive or Colab workspace
os.makedirs(SAVE_DIR, exist_ok=True)

# Set Paris timezone for consistent timestamps
paris_tz = timezone("Europe/Paris")


def snapshot_velo():
    """
    Fetch real-time data from JCDecaux API and save as a Parquet file.
    """
    url = f"https://api.jcdecaux.com/vls/v1/stations?contract={CONTRACT}&apiKey={API_KEY}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        df = pd.json_normalize(data)

        now = datetime.now(paris_tz)
        snapshot_time = now.strftime("%Y-%m-%d %H:%M:%S")
        df["snapshot_time"] = snapshot_time

        filename = f"{SAVE_DIR}/snapshot_{now.strftime('%Y%m%d_%H%M')}.parquet"
        df.to_parquet(filename, engine="pyarrow", index=False)

        print(f"[OK] Snapshot saved: {filename}")
    else:
        print(f"[ERROR] API request failed: {response.status_code}")


def run_hourly_capture(interval_minutes=5, duration_minutes=60):
    """
    Take snapshots every X minutes for the specified duration.
    Default = 12 snapshots (every 5 min for 1 hour).
    """
    iterations = duration_minutes // interval_minutes
    for i in range(iterations):
        print(f"--- Snapshot {i + 1}/{iterations} ---")
        snapshot_velo()
        if i < iterations - 1:
            time.sleep(interval_minutes * 60)


# Run the snapshot capture
run_hourly_capture(interval_minutes=5, duration_minutes=60)
