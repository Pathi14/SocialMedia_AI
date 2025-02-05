import sqlite3
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

# Connexion à la base de données et récupération des tweets
connection = sqlite3.connect('database.db')
query = "SELECT text, negative FROM tweets"
df = pd.read_sql_query(query, connection)
connection.close()

# Nettoyage du texte
def clean_text(text):
    text = text.lower()  # Minuscule
    text = re.sub(r'[^\w\s]', '', text)  # Suppression des caractères spéciaux
    return text

df['text_clean'] = df['text'].apply(clean_text)

# Vectorisation (bag of words)
french_stopwords = [
    "le", "la", "les", "un", "une", "des", "du", "de", "dans", "et", "en", "au",
    "aux", "avec", "ce", "ces", "pour", "par", "sur", "pas", "plus", "où", "mais",
    "ou", "donc", "ni", "car", "ne", "que", "qui", "quoi", "quand", "à", "son",
    "sa", "ses", "ils", "elles", "nous", "vous", "est", "sont", "cette", "cet",
    "aussi", "être", "avoir", "faire", "comme", "tout", "bien", "mal", "on", "lui"
]

vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
X = vectorizer.fit_transform(df['text_clean'])
y = df['negative']  # On prend la colonne `negative` comme label

# Séparation des données
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Entraînement du modèle
model = LogisticRegression()
model.fit(X_train, y_train)

# Prédictions et évaluation
y_pred = model.predict(X_test)
print("Rapport de classification :")
print(classification_report(y_test, y_pred))

print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# Tester avec de nouveaux commentaires
new_comments = [
    "Ce produit est une arnaque totale, à fuir !",  # Négatif
    "Extrêment laid, dégoutant",  # Negatif
    "J'adore ce produit, il est génial !",  # Positif
    "Ce restaurant a un service exécrable, très déçu.",  # Négatif
    "Un restaurant correct, sans plus.",  # Neutre
    "Beau cadeau !!!",  # Positif
]

# Nettoyage et vectorisation
new_comments_clean = [clean_text(comment) for comment in new_comments]
new_comments_vectorized = vectorizer.transform(new_comments_clean)

# Prédictions
predictions = model.predict(new_comments_vectorized)
for comment, label in zip(new_comments, predictions):
    print(f"Commentaire : '{comment}' -> {'Negative' if label == 1 else 'Else'}")
