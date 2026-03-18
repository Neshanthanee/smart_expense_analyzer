def answer_question(df, question):
    question = question.lower()

    if "total" in question:
        return f"Total spending is ₹{df['amount'].sum():,.0f}"

    elif "highest" in question:
        return f"Highest transaction is ₹{df['amount'].max():,.0f}"

    elif "average" in question:
        return f"Average transaction is ₹{df['amount'].mean():,.0f}"

    elif "month" in question:
        m = df.groupby("month")["amount"].sum().idxmax()
        return f"Highest spending month is {m}"

    else:
        return "Try asking about total, average or highest spending."