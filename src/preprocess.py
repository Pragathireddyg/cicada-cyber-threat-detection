import pandas as pd
import numpy as np


def clean_data(df):
    print("\n Cleaning data")

    # Remove duplicate columns (sometimes exist in dataset)
    df = df.loc[:, ~df.columns.duplicated()]

    # Replace infinite values with NaN
    df.replace([np.inf, -np.inf], np.nan, inplace=True)

    # Drop rows with NaN values
    df.dropna(inplace=True)

    print(" Removed NaN and infinite values")

    # Strip column names (remove spaces)
    df.columns = df.columns.str.strip()

    print(f"Cleaned Shape: {df.shape}")

    return df


if __name__ == "__main__":
    from data_loader import load_data

    path = "data/raw/network_data.csv"
    df = load_data(path)

    df_clean = clean_data(df)

    print(df_clean.head())