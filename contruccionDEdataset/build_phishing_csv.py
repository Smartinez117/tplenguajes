import requests
import pandas as pd

URL = "https://openphish.com/feed.txt"

print("Descargando URLs phishing...")
resp = requests.get(URL, timeout=20)
resp.raise_for_status()

urls = resp.text.splitlines()

data = []
for u in urls:
    if u.strip():
        data.append({
            "url": u.strip(),
            "email_text": "",
            "label": 1
        })

df = pd.DataFrame(data)
df.to_csv("../data/phishing.csv", index=False)

print(f"phishing.csv generado con {len(df)} URLs")
