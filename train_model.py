
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, roc_auc_score
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import joblib

from feature_extractor import extract_url_features, extract_text_features
# 1️ Cargar datos
phishing = pd.read_csv("data/phishing.csv")
legit = pd.read_csv("data/legit.csv")
df = pd.concat([phishing, legit], ignore_index=True)
# 2️ LIMPIEZA (ANTES DE TODO)
df["url"] = df["url"].fillna("").astype(str)
df["email_text"] = df["email_text"].fillna("").astype(str)
# 3️ Extraer features manuales
url_feats = df["url"].apply(extract_url_features).apply(pd.Series)
text_feats = df["email_text"].apply(extract_text_features).apply(pd.Series)

df_feats = pd.concat([df, url_feats, text_feats], axis=1).fillna(0)

# 4️ Texto combinado para TF-IDF
df_feats["text_all"] = df_feats["url"] + " " + df_feats["email_text"]
# 5️  X / y
X = df_feats.drop(columns=["label"])
y = df_feats["label"]

text_col = "text_all"
num_cols = [c for c in X.columns if c not in ["url", "email_text", "text_all"]]
# 6️ Pipeline
pipeline = Pipeline([
    ("features", ColumnTransformer([
        ("tfidf", TfidfVectorizer(ngram_range=(3,5)), text_col),
        ("num", StandardScaler(), num_cols)
    ])),
    ("clf", LogisticRegression(max_iter=1000, class_weight="balanced"))
])

# 7️ Train / Test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

pipeline.fit(X_train, y_train)
# 8️ Evaluación
preds = pipeline.predict(X_test)
probs = pipeline.predict_proba(X_test)[:, 1]

print(classification_report(y_test, preds))
print("AUC:", roc_auc_score(y_test, probs))
# 9️ Guardar modelo
joblib.dump(pipeline, "phishing_model.joblib")
print("Modelo guardado")
