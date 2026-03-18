import pandas as pd

def clean_data(df):
    df.columns = df.columns.str.lower()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

    df = df.dropna()
    df = df.drop_duplicates()
    df = df[df["amount"] > 0]

    return df


def feature_engineering(df):
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["weekday"] = df["date"].dt.day_name()

    return df