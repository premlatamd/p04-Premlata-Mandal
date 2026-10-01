# R1 — Dataset Selection

Dataset:
NYC Yellow Taxi Trip Records (February 2026)

Why this dataset:

- large real-world dataset
- contains missing values
- contains low-cardinality categorical features
- contains high-cardinality categorical features
- contains genuine outliers and noisy records

Requirement checks:

- rows = 3,399,866 (> 1,000)
- columns = 20 (> 8)

Numeric column with ≥3% missing values:

- passenger_count (30.09% missing)

Low-cardinality categorical column (<10 categories):

- payment_type (5 categories)

High-cardinality categorical column (>30 categories):

- PULocationID (259 categories)

License:

- NYC TLC Open Data
- publicly available for research and educational use

Conclusion:

The dataset satisfies all four required messiness properties and is suitable for the remaining preprocessing and pipeline tasks.

# R2 - Data Audit

## VendorID
VendorID contains only 4 distinct values and has no missing values. Since it represents different taxi vendors rather than a continuous numerical measurement, it will be treated as a categorical feature. One-Hot Encoding will be used during preprocessing.

## passenger_count
This column has 30.1% missing values and only 9 distinct values. It represents the number of passengers travelling in a taxi. Since the column contains missing values, median imputation will be applied and a passenger_count_missing indicator column will be created to preserve information about missingness.

## trip_distance
trip_distance is a continuous numerical feature with 4,719 distinct values. The maximum value is 328,522.2 miles, which is unrealistic for a taxi trip and indicates the presence of extreme outliers. Therefore, outlier treatment using IQR or percentile clipping will be applied.

## RatecodeID
RatecodeID contains only 7 distinct values but has 30.1% missing values. Since it represents fare categories, it will be treated as a categorical feature. Missing values will be filled using the most frequent category and then encoded.

## store_and_fwd_flag
This column contains only two categories: Y and N. It also has 30.1% missing values. Since it is a binary categorical feature, missing values will be imputed using the mode and the column will be binary encoded.

## PULocationID
PULocationID contains 259 distinct values and no missing values. It is a high-cardinality categorical feature representing pickup locations. Frequency Encoding will be used to reduce dimensionality.

## DOLocationID
DOLocationID contains 261 distinct values and no missing values. Similar to PULocationID, it is a high-cardinality location feature and will be Frequency Encoded.

## payment_type
payment_type contains only 5 distinct values and no missing values. The values represent categories such as Credit Card, Cash, No Charge and Dispute. Therefore, it will be treated as a categorical feature and encoded using One-Hot Encoding.

## fare_amount
fare_amount is a continuous numerical variable with 12,616 distinct values. Negative fare values are present, which may indicate data quality issues. Outlier treatment and validation checks will be applied before modeling.

## extra
extra represents additional charges applied to a trip. It contains 41 distinct values and some negative values. Outlier analysis will be performed before model training.

## mta_tax
mta_tax has only 10 distinct values and no missing values. Since it is a tax-related numerical feature with a small value range, it will be retained without major transformation.

## tip_amount
tip_amount is a continuous numerical variable with 4,210 distinct values. Extreme positive and negative values are present. Outlier capping will be performed to reduce their influence.

## tolls_amount
tolls_amount contains 1,169 distinct values. Extreme values are observed, including negative amounts. Outlier treatment will be applied before modeling.

## improvement_surcharge
This column contains only 4 distinct values and no missing values. Since it already has a limited range, it will be retained as a numerical feature.

## total_amount
total_amount contains 19,930 distinct values and represents the final trip cost. Extreme values are present and may influence model performance. Outlier treatment will therefore be applied.

## congestion_surcharge
This feature has 30.1% missing values and only 4 distinct values. Missing values may indicate trips where congestion surcharge was not applicable. Median imputation and a missing-value indicator column will be used.

## Airport_fee
Airport_fee contains 30.1% missing values and 8 distinct values. Missing values likely correspond to trips not associated with airports. Median imputation and a missing-value indicator will be created.

## cbd_congestion_fee
This feature contains only 3 distinct values and no missing values. It will be retained as a numerical feature without major transformation.

## tpep_pickup_datetime
This column is a timestamp with very high cardinality. Instead of using the raw timestamp, useful features such as pickup hour, day, weekday and month will be extracted.

## tpep_dropoff_datetime
This column is also a timestamp with high cardinality. Trip duration will be calculated using pickup and dropoff times, and additional temporal features will be extracted.
