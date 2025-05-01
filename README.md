# Velib Toulouse Fidelity Analysis

## Context

As a regular user of the "Vélo Toulouse" bike-sharing service for over a year, I became increasingly curious about the fidelity point system.  
Users can earn 10 fidelity points by returning a bike to a designated "bonus" station, which in turn allows them to reserve a bike for 15 minutes.  
However, I noticed that I rarely received points, and the official documentation or website provided no clear explanation about how or when points were awarded.

This project was born out of a personal need to better understand and optimize the earning of fidelity points.  
Since no reliable resource was available online, I decided to build my own dataset and analyze the patterns myself.

---

## Tools and Technologies

To carry out this analysis, the following tools were used:

- **Python**: to collect real-time data from the JCDecaux API
- **Parquet**: to store snapshot data efficiently
- **DBeaver / DuckDB**: to perform SQL-based analysis
- **JCDecaux API**: to retrieve live bike station status

---

## How to Use This Project

You have two options to explore the project.

### Option A — Run the Python script via Google Colab

1. Open the file `scripts_snapshot_collector.py` in [Google Colab](https://colab.research.google.com/)
2. Replace the placeholder with your JCDecaux API key:
   ```python
   API_KEY = "YOUR_API_KEY_HERE"
   ```
3. Install the required packages at the top of the notebook:
   ```python
   !pip install pytz duckdb pyarrow pandas
   ```
4. Run the script to generate `.parquet` files in a folder named `snapshots_velo/`.  
   The script will take one snapshot every 5 minutes over a 1-hour period (12 total).

### Option B — Use the provided dataset

1. Download and unzip the file `snapshots_velo.zip`
2. Extract the files into a local folder named `snapshots_velo/`
3. Open the SQL script `bonus_opportunities_analysis.sql` in DBeaver
4. Make sure the SQL script points to your local path:
   ```sql
   FROM read_parquet('snapshots_velo/*.parquet')
   ```
5. Execute the script to analyze the bonus station conditions.

---

## Get a JCDecaux API Key

To collect your own data using the script:

1. Go to the JCDecaux developer portal: https://developer.jcdecaux.com/#/account
2. Create an account or log in
3. Generate a new API key
4. Enable the **Toulouse** contract
5. Copy the key and paste it into the Python script as shown above

---

## SQL Analysis Summary

The SQL script `bonus_opportunities_analysis.sql` creates two views:

- `v_stations_velo_snapshots`: loads all `.parquet` files and extracts relevant fields
- `v_stations_bonus_analysis`: classifies stations into bonus types based on simple conditions

| Bonus Type       | Condition                          |
|------------------|-------------------------------------|
| `DEPART_BONUS`   | The station is full (`free_stands = 0`) |
| `ARRIVAL_BONUS`  | The station is empty (`available_bikes = 0`) |

Example query to get the most recent bonus opportunities:
```sql
SELECT *
FROM v_stations_bonus_analysis
WHERE snapshot_time = (
  SELECT MAX(snapshot_time) FROM v_stations_bonus_analysis
);
```
## Conclusion

This project allowed me to confirm, both through data and personal testing, that the conditions for earning fidelity points with Vélo Toulouse are based on two key situations:  
either taking a bike from a full station (`free_stands = 0`), or returning one to an empty station (`available_bikes = 0`).

These factors are not clearly documented by the service, but through SQL analysis and live experiments using my own Vélo Toulouse account, I was able to validate that these criteria are indeed what trigger point rewards.

The version published here focuses on a lightweight and accessible workflow, allowing anyone to test the logic using a short data collection session or the provided sample dataset.  
For those interested in a deeper analysis over time (seasonality, best locations, peak hours), the data collection script can be extended to run continuously.

Ideally, if Vélo Toulouse were to make historical data openly available, users and researchers would no longer need to collect snapshots in real time.  
My project was created precisely because this data was not accessible — I wanted to investigate the logic myself, without having to wait for official documentation or datasets.


---


## Author

**PeterBlue78**
