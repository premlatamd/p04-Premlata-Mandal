from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, RobustScaler
from sklearn.linear_model import LinearRegression


def build_pipeline():

    numeric_cols = [
        "trip_distance",
        "fare_amount",
        "tip_amount",
        "tolls_amount",
        "extra",
        "Airport_fee",
        "congestion_surcharge",
        "cbd_congestion_fee"
    ]

    categorical_cols = [
        "VendorID",
        "payment_type",
        "RatecodeID",
        "store_and_fwd_flag",
        "PULocationID",
        "DOLocationID"
    ]

    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", RobustScaler())
    ])

    cat_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="most_frequent")),
        ("encoder", OneHotEncoder(handle_unknown="ignore"))
    ])

    preprocessor = ColumnTransformer([
        ("num", num_pipeline, numeric_cols),
        ("cat", cat_pipeline, categorical_cols)
    ])

    model_pipeline = Pipeline([
        ("preprocessor", preprocessor),
        ("model", LinearRegression())
    ])

    return model_pipeline


if __name__ == "__main__":
    model = build_pipeline()
    print(model)