-- Load spatial extension (DuckDB)
INSTALL spatial;
LOAD spatial;

-- View: Unified snapshot data from all local Parquet snapshots
-- Assumes all .parquet files are stored in the folder: data/snapshots_velo/ 
CREATE OR REPLACE VIEW v_stations_velo_snapshots AS
SELECT 
  number AS station_id,
  name AS station_name,
  address,
  bonus,
  bike_stands AS total_stands,
  available_bike_stands AS free_stands,
  available_bikes AS available_bikes,
  status,
  contract_name,
  banking,
  last_update,
  "position.lat" AS latitude,
  "position.lng" AS longitude,
  ST_Point("position.lng", "position.lat") AS geom,
  snapshot_time
FROM read_parquet('data/snapshots_velo/*.parquet'); -- Update the path if your snapshots are stored elsewhere

-- Example: Snapshot evolution for a specific station
SELECT 
  station_name,
  snapshot_time,
  available_bikes
FROM v_stations_velo_snapshots
WHERE station_name ILIKE '%MATABIAU GARE%'
ORDER BY snapshot_time;

-- Bonus opportunity classification (strict: 0 bikes or 0 free stands only)
CREATE OR REPLACE VIEW v_stations_bonus_analysis AS
SELECT 
  station_name,
  snapshot_time,
  available_bikes,
  free_stands,
  CASE 
    WHEN free_stands = 0 THEN 'DEPART_BONUS'
    WHEN available_bikes = 0 THEN 'ARRIVAL_BONUS'
    ELSE NULL
  END AS bonus_type,
  10 AS assumed_points,
  ST_Point(longitude, latitude) AS geom
FROM v_stations_velo_snapshots
WHERE free_stands = 0 OR available_bikes = 0;

-- View latest bonus opportunities
SELECT *
FROM v_stations_bonus_analysis
WHERE snapshot_time = (
  SELECT MAX(snapshot_time) FROM v_stations_bonus_analysis
);
