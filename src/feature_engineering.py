import pandas as pd


def create_features(df):
    print("\n Creating features")

    # Example features (very important for security)
    df["packet_rate"] = df["Total Fwd Packets"] / (df["Flow Duration"] + 1)
    df["byte_rate"] = df["Total Length of Fwd Packets"] / (df["Flow Duration"] + 1)

    # Flag suspicious high activity
    df["high_traffic_flag"] = (df["packet_rate"] > df["packet_rate"].quantile(0.95)).astype(int)

    print(" Features created")

    return df


if __name__ == "__main__":
    from data_loader import load_data
    from preprocess import clean_data

    path = "data/raw/network_data.csv"

    df = load_data(path)
    df = clean_data(df)

    df = create_features(df)

    print(df[["packet_rate", "byte_rate", "high_traffic_flag"]].head())