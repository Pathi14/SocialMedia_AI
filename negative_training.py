from pathlib import Path
import pickle
import sqlalchemy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from preprocessing import preprocess

# 🔹 Connexion à la base de données MySQL via SQLAlchemy
db_url = "mysql+pymysql://user:userpassword@localhost/tweets_db"
engine = sqlalchemy.create_engine(db_url)

query = "SELECT text, negative FROM tweets"
df = pd.read_sql(query, engine)

# 🔹 Vérification des classes dans y
if df["negative"].nunique() < 2:
    raise ValueError(
        "Erreur : La base de données doit contenir au moins deux classes (positif et négatif)."
    )

X = preprocess(df["text"])
y = df["negative"]  # On prend la colonne `negative` comme label

# Séparation des données
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

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
new_comments_vectorized = preprocess(new_comments)

# Prédictions
predictions = model.predict(new_comments_vectorized)
for comment, label in zip(new_comments, predictions):
    print(f"Commentaire : '{comment}' -> {'Negative' if label == 1 else 'Else'}")

# 🔹 Sauvegarde
pickle.dump(model, open(Path(__file__).parent / "models/negative.pkl", "wb"))
