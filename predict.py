import joblib
import pandas as pd
from feature_extractor import extract_url_features, extract_text_features

model = joblib.load("phishing_model.joblib")

def predict_phishing(url, email_text=""):
    data = {
        "url": url,
        "email_text": email_text
    }

    url_feats = extract_url_features(url)
    text_feats = extract_text_features(email_text)

    row = {**data, **url_feats, **text_feats}
    df = pd.DataFrame([row])
    df["text_all"] = df["url"] + " " + df["email_text"]

    prob = model.predict_proba(df)[0][1]
    return prob

# dato a chequear
p = predict_phishing(
    "https://www.google.com",
    "gracias por usar los servicios de google felices fiestas"
)

print("Probabilidad de phishing:", round(p, 3))
