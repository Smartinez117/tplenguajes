import re
import urllib.parse as urlparse

def extract_url_features(url):
    features = {}
    if not url:
        return features

    if not url.startswith("http"):
        url = "http://" + url

    parsed = urlparse.urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()

    features["url_length"] = len(url)
    features["num_dots"] = domain.count(".")
    features["num_hyphens"] = domain.count("-")
    features["num_slashes"] = path.count("/")
    features["has_https"] = int(parsed.scheme == "https")
    features["has_ip"] = int(bool(re.search(r"\d+\.\d+\.\d+\.\d+", domain)))

    suspicious = ["login", "verify", "secure", "account", "bank"]
    for w in suspicious:
        features[f"url_has_{w}"] = int(w in url.lower())

    return features


def extract_text_features(text):
    features = {}
    if not isinstance(text, str):
        text = ""

    text = text.lower()
    features["text_length"] = len(text)
    features["num_words"] = len(text.split())
    features["num_links"] = len(re.findall(r"http[s]?://", text))
    features["num_exclaims"] = text.count("!")

    urgency = ["urgent", "immediately", "verify", "suspend"]
    for w in urgency:
        features[f"text_has_{w}"] = int(w in text)

    return features
