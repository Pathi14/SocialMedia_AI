import pickle
import sqlalchemy
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from pathlib import Path
from preprocessing import preprocess

# Connexion à la base de données MySQL via SQLAlchemy
db_url = "mysql+pymysql://user:userpassword@localhost/tweets_db"
engine = sqlalchemy.create_engine(db_url)

query = "SELECT text, positive FROM tweets"
df = pd.read_sql(query, engine)

# 🔹 Vérification des classes dans y
if df["positive"].nunique() < 2:
    raise ValueError(
        "Erreur : La base de données doit contenir au moins deux classes (positif et négatif)."
    )

X = preprocess(df["text"])
y = df["positive"]  # On prend la colonne "positive" comme label

# 🔹 Séparation des données en train/test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# 🔹 Vérification des classes après séparation
if len(set(y_train)) < 2:
    raise ValueError(
        "Erreur : y_train doit contenir au moins 2 classes distinctes (positif/négatif)."
    )

# 🔹 Entraînement du modèle de régression logistique
model = LogisticRegression()
model.fit(X_train, y_train)

# 🔹 Prédictions et évaluation du modèle
y_pred = model.predict(X_test)
print("Rapport de classification :")
print(classification_report(y_test, y_pred))

print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# 🔹 Tester avec de nouveaux commentaires
new_comments = [
    "Je ne supporte pas cette personne.",  # Négatif
    "Cette vidéo est incroyable, merci pour votre travail.",  # Positif
    "Arrête de dire n'importe quoi, imbécile.",  # Négatif
    "Une excellente présentation, bravo à toute l'équipe.",  # Positif
    "Ta gueule!!!",  # Négatif
    "Imbécile",  # Négatif
]

# 🔹 Nettoyage et vectorisation
new_comments_vectorized = preprocess(new_comments)

# 🔹 Prédictions sur les nouveaux commentaires
predictions = model.predict(new_comments_vectorized)
for comment, label in zip(new_comments, predictions):
    print(f"Commentaire : '{comment}' -> {'Positive' if label == 1 else 'Else'}")

# 🔹 Sauvegarde
pickle.dump(model, open(Path(__file__).parent / "models/positive.pkl", "wb"))
