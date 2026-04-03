import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score


def train_classifier(df):
    print("\nTraining attack classification model")

    df = df.copy()
    df.columns = df.columns.str.strip()

    if "Label" not in df.columns:
        raise ValueError("Label column not found in dataset")

    X = df.drop(columns=["Label"])
    y = df["Label"]

    X = X.select_dtypes(include=["number"]).copy()
    X.replace([np.inf, -np.inf], np.nan, inplace=True)
    X = X.clip(lower=-1e9, upper=1e9)
    X.dropna(inplace=True)

    y = y.loc[X.index]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    print("Classifier trained successfully")
    print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    print("\nClassification Report:\n")
    print(classification_report(y_test, y_pred))

    return model


if __name__ == "__main__":
    from data_loader import load_data
    from preprocess import clean_data
    from feature_engineering import create_features

    path = "data/raw/network_data.csv"

    df = load_data(path)
    df = clean_data(df)
    df = create_features(df)

    train_classifier(df)