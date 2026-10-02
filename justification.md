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


# R3 - Missing Data Analysis

The dataset contains five columns with missing values:

- passenger_count
- RatecodeID
- store_and_fwd_flag
- congestion_surcharge
- Airport_fee

Each of these columns has approximately 30.1% missing values.

To investigate the missingness mechanism, the mean values of several observed variables were compared between rows with missing values and rows without missing values.

Rows with missing values had:

- Mean trip_distance = 12.97 miles
- Mean fare_amount = 27.23
- Mean total_amount = 33.68

Rows without missing values had:

- Mean trip_distance = 3.35 miles
- Mean fare_amount = 19.24
- Mean total_amount = 28.58

The differences are substantial. Therefore, the probability of a value being missing appears to depend on other observed variables in the dataset. This suggests a Missing At Random (MAR) mechanism rather than MCAR.

Because the missingness mechanism is MAR, imputation methods that use information from the observed data are appropriate.

---

## passenger_count

Approximately 30.1% of values are missing.

The missing rows have significantly larger trip distances and fare amounts than non-missing rows, indicating that missingness depends on observed trip characteristics. Therefore, the mechanism is classified as MAR.

Median imputation was selected because passenger_count is numerical and contains a limited range of values.

A passenger_count_missing indicator variable was created and retained because the missingness pattern itself may contain useful information.

Before imputation:

- Mean = 1.16
- Median = 1.00
- Standard Deviation = 0.54

---

## RatecodeID

Approximately 30.1% of values are missing.

The missingness pattern follows the same behaviour observed for passenger_count, suggesting a MAR mechanism.

Since RatecodeID represents fare categories, missing values were replaced using the most frequent category.

A RatecodeID_missing indicator variable was created and retained.

Before imputation:

- Mean = 3.97
- Median = 1.00
- Standard Deviation = 16.62

---

## store_and_fwd_flag

Approximately 30.1% of values are missing.

The missing rows exhibit different trip characteristics compared to non-missing rows, supporting a MAR assumption.

Since this is a binary categorical variable (Y/N), mode imputation was used.

A store_and_fwd_flag_missing indicator variable was created and retained.

---

## congestion_surcharge

Approximately 30.1% of values are missing.

Missingness appears related to observed trip properties such as trip distance and fare amount. Therefore, the mechanism is considered MAR.

Median imputation was selected because the variable is numerical and highly skewed.

A congestion_surcharge_missing indicator variable was created and retained.

Before imputation:

- Mean = 2.27
- Median = 2.50
- Standard Deviation = 0.77

---

## Airport_fee

Approximately 30.1% of values are missing.

The missingness pattern is associated with observed trip characteristics, indicating a MAR mechanism.

Median imputation was used because the variable is numerical and contains a large number of zero values.

An Airport_fee_missing indicator variable was created and retained.

Before imputation:

- Mean = 0.10
- Median = 0.00
- Standard Deviation = 0.44

# R4 – Scaling Decisions

### trip_distance
The trip_distance column has extremely high positive skewness (267.40). The median value is only 1.8 miles, while the maximum value is 328,522.2 miles, indicating the presence of extreme outliers. Therefore, I applied a Log1p transformation followed by RobustScaler. The log transformation reduces the impact of very large values, and RobustScaler is less sensitive to outliers than StandardScaler.

### fare_amount
The fare_amount column has a skewness of 3.20 and contains extreme values ranging from -2084.1 to 2084.1. These values indicate refunds, corrections, or data anomalies. Therefore, RobustScaler was selected because it scales data using the median and interquartile range, making it suitable for distributions with outliers.

### total_amount
The total_amount column is positively skewed (2.92) and contains large positive and negative outliers. Since StandardScaler is sensitive to outliers, RobustScaler was chosen to preserve the overall distribution while reducing the influence of extreme values.

### tip_amount
The tip_amount column has a skewness of 5.81. Most observations are close to zero, but a few very large tips create a long right tail. Therefore, Log1p transformation followed by RobustScaler was applied to reduce skewness and improve scaling.

### tolls_amount
The tolls_amount column has a skewness of 5.35. Most trips have zero tolls, while a small number of trips have very high toll values. RobustScaler was chosen because it performs better when data contains extreme values.

### passenger_count
Although passenger_count has a skewness of 4.17, it is a discrete count variable with only a few possible values (0–9). Since it represents the number of passengers rather than a continuous measurement, no scaling was applied.

### VendorID
VendorID is a categorical identifier representing taxi vendors. Even though its skewness is 4.54, scaling is not appropriate. Instead, One-Hot Encoding will be used.

### payment_type
payment_type represents payment categories such as credit card and cash. Since it is categorical data, One-Hot Encoding will be used instead of scaling.

### PULocationID and DOLocationID
These columns are location identifiers rather than continuous numerical measurements. Therefore, they will be encoded as categorical variables instead of being scaled.

### congestion_surcharge, Airport_fee, cbd_congestion_fee, mta_tax and improvement_surcharge
These columns contain fixed charges with only a small number of unique values. Additional scaling is not necessary because their values are already bounded and interpretable.

### Conclusion
Not all numerical columns were standardized. Highly skewed columns such as trip_distance, tip_amount, fare_amount and total_amount required RobustScaler or Log1p transformation. Categorical identifiers such as VendorID, payment_type and location IDs were encoded instead of scaled. These decisions were based on the observed skewness, outliers and the meaning of each feature.

# R5 - Encoding Strategy

The dataset contains six categorical features:

- VendorID
- payment_type
- RatecodeID
- store_and_fwd_flag
- PULocationID
- DOLocationID

An encoding audit was performed by counting the number of unique categories in each feature.

VendorID, payment_type, RatecodeID and store_and_fwd_flag were identified as low-cardinality categorical variables because they contain fewer than 10 unique categories. These features were encoded using:

```python
OneHotEncoder(handle_unknown="ignore")<img width="819" height="415" alt="Screenshot 2026-10-02 at 12 20 13 AM" src="https://github.com/user-attachments/assets/daeff8a7-693a-4ab5-a232-d528fc98ba77" />

```

# R6 - One Pipeline Object

A single Pipeline object was created using Pipeline and ColumnTransformer.

Numerical features were processed through a numerical pipeline containing:
- SimpleImputer(strategy="median")
- RobustScaler

Categorical features were processed through a categorical pipeline containing:
- SimpleImputer(strategy="most_frequent")
- OneHotEncoder(handle_unknown="ignore")

Both pipelines were combined using ColumnTransformer and connected to a Linear Regression model.

# R7
Justification:
- All preprocessing steps are performed inside the pipeline.
- Unseen categories are handled using handle_unknown='ignore'.
- Missing values are handled automatically through SimpleImputer.
- The same transformations are applied during training, testing, and cross-validation.
- No preprocessing is fitted outside the pipeline, reducing the risk of data leakage.

Leakage Score (R²): 0.9819
Pipeline Score (R²): 0.9839
Difference: -0.0020

The difference between the two scores was very small. In this dataset, leakage did not noticeably inflate performance. However, the pipeline approach remains the correct practice because preprocessing is learned separately within each fold.

For unseen-category testing, the pipeline successfully produced a prediction (30.97) for categories that were never observed during training. This demonstrates that handle_unknown='ignore' improves robustness and prevents prediction failures in production environments.

# R8 

Leak Experiment:

I compared a correct pipeline against a deliberately broken version where preprocessing was performed outside the pipeline before cross-validation.

Correct Pipeline R² Score = 0.9839

Leakage Version R² Score = 0.9819

Difference = -0.0020

The difference is very small (0.2%), showing that leakage was not severe for this dataset. This is a useful finding because small leakage effects are often difficult to notice in practice. Using the pipeline remains the correct approach because preprocessing is learned separately inside each cross-validation fold.

# R8 Section 5 — What I would do differently

If I had more time and computational resources, I would explore additional feature engineering techniques such as trip duration features, location clustering, and interaction variables.

I would also compare multiple regression models including Random Forest Regressor, XGBoost, and Gradient Boosting Regressor.

Finally, I would investigate advanced missing-value imputation methods and perform hyperparameter tuning using GridSearchCV.

# R8 Section 6 — What breaks this pipeline

This pipeline does not handle completely new numeric distributions that are very different from the training data.

Extremely large trip distances, fare amounts, or corrupted records may reduce prediction quality.

The pipeline also assumes that the input columns exist with the same names and data types as the training dataset.

If important columns are removed, renamed, or contain unexpected formats, the pipeline may fail.

Although unseen categories are handled through OneHotEncoder(handle_unknown="ignore"), performance may still decrease when many new categories appear in production.

# R9

Median imputation achieved the highest average R² score and was therefore selected for the final pipeline. Mean and most-frequent imputation produced similar performance, suggesting that the model is relatively robust to the imputation choice.
