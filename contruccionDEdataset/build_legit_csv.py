import pandas as pd

legit_domains = [
    "https://www.google.com",
    "https://www.wikipedia.org",
    "https://www.bing.com",
    "https://duckduckgo.com",
    "https://www.yahoo.com",
    "https://chatgpt.com",
    "https://github.com",
    "https://www.amazon.com",
    "https://www.netflix.com",
    "https://www.microsoft.com",
    "https://www.apple.com",
    "https://www.paypal.com",
    "https://www.linkedin.com",
    "https://www.youtube.com",
    "https://www.reddit.com",
    "https://www.stackoverflow.com",
    "https://www.coursera.org",
    "https://www.spotify.com",
    "https://www.bbc.com",
    "https://www.nytimes.com",
]

data = []
for url in legit_domains:
    data.append({
        "url": url,
        "email_text": "",
        "label": 0
    })

df = pd.DataFrame(data)
df.to_csv("../data/legit.csv", index=False)

print(f"legit.csv generado con {len(df)} URLs")
