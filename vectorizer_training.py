from pathlib import Path
import pickle
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
import sqlalchemy

# Vectorisation (bag of words)
french_stopwords = [
    "le",
    "la",
    "les",
    "un",
    "une",
    "des",
    "du",
    "de",
    "dans",
    "et",
    "en",
    "au",
    "aux",
    "avec",
    "ce",
    "ces",
    "pour",
    "par",
    "sur",
    "pas",
    "plus",
    "où",
    "mais",
    "ou",
    "donc",
    "ni",
    "car",
    "ne",
    "que",
    "qui",
    "quoi",
    "quand",
    "à",
    "son",
    "sa",
    "ses",
    "ils",
    "elles",
    "nous",
    "vous",
    "est",
    "sont",
    "cette",
    "cet",
    "aussi",
    "être",
    "avoir",
    "faire",
    "comme",
    "tout",
    "bien",
    "mal",
    "on",
    "lui",
]

vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)

db_url = "mysql+pymysql://user:userpassword@localhost/tweets_db"
engine = sqlalchemy.create_engine(db_url)

query = "SELECT text FROM tweets"
df = pd.read_sql(query, engine)

vectorizer.fit(df["text"])

# 🔹 Sauvegarde
pickle.dump(
    vectorizer, open(Path(__file__).parent.parent / "models/vectorizer.pkl", "wb")
)
