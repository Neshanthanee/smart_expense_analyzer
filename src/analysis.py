def get_metrics(df):
    return df["amount"].sum(), df["amount"].mean(), df["amount"].max()

def monthly_spending(df):
    return df.groupby("month")["amount"].sum()

def top_merchants(df):
    return df["description"].value_counts().head(5)

def txn_type(df):
    return df.groupby("transaction_type")["amount"].sum()