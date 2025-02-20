import pandas as pd
import re
import pickle
from pathlib import Path

vectorizer = pickle.load(open(Path(__file__).parent / "models/vectorizer.pkl", "rb"))


# 🔹 Fonction de nettoyage du texte
def clean_text(text):
    text = text.lower()  # Minuscule
    text = re.sub(r"[^\w\s]", "", text)  # Suppression des caractères spéciaux
    return text


def preprocess(texts: list[str]):
    cleaned = [clean_text(text) for text in texts]
    return vectorizer.transform(cleaned)
