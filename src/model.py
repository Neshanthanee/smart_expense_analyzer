from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

def assign_category(text):
    text = str(text).lower()

    if "swiggy" in text or "zomato" in text:
        return "Food"
    elif "uber" in text or "ola" in text:
        return "Transport"
    elif "amazon" in text or "flipkart" in text:
        return "Shopping"
    elif "netflix" in text or "spotify" in text:
        return "Entertainment"
    else:
        return "Others"

def train_model(df):
    df["category"] = df["description"].apply(assign_category)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["description"])
    y = df["category"]

    model = LogisticRegression()
    model.fit(X, y)

    return model, vectorizer

def predict_category(model, vectorizer, text):
    return model.predict(vectorizer.transform([text]))[0]