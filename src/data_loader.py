import pandas as pd
import os


def load_data(file_path):
    """
    Load network traffic dataset
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    print("Data loaded successfully")
    print(f"Shape: {df.shape}")

    return df


if __name__ == "__main__":
    path = "data/raw/network_data.csv"
    df = load_data(path)
    print(df.head())