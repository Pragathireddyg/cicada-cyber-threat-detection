import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest


def train_anomaly_model(df):
    print("\nTraining anomaly detection model")

    # keep only numeric columns
    df_numeric = df.select_dtypes(include=["number"]).copy()

    # replace inf values again just to be safe
    df_numeric.replace([np.inf, -np.inf], np.nan, inplace=True)

    # remove very large values that break sklearn
    df_numeric = df_numeric.clip(lower=-1e9, upper=1e9)

    # drop remaining NaN rows
    df_numeric.dropna(inplace=True)

    # train model
    model = IsolationForest(
        n_estimators=100,
        contamination=0.05,
        random_state=42
    )

    df_numeric["anomaly"] = model.fit_predict(df_numeric)

    print("Model trained successfully")
    return df_numeric


if __name__ == "__main__":
    from data_loader import load_data
    from preprocess import clean_data
    from feature_engineering import create_features

    path = "data/raw/network_data.csv"

    df = load_data(path)
    df = clean_data(df)
    df = create_features(df)

    df_result = train_anomaly_model(df)

    print(df_result["anomaly"].value_counts())