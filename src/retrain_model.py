import sqlalchemy
import pymysql
import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import logging

# Configurer la journalisation
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def retrain_model():
    logging.info("Début du réentraînement du modèle")
    try:
        # 🔹 Connexion à la base de données MySQL
        logging.info("Connexion à la base de données MySQL...")
        engine = sqlalchemy.create_engine('mysql+pymysql://user:userpassword@localhost/tweets_db')
        logging.info("Connexion réussie à la base de données MySQL")

        query = "SELECT text, positive, negative FROM tweets"
        df = pd.read_sql(query, engine)
        logging.info("Données récupérées depuis la base de données MySQL")
        logging.info(f"Nombre de lignes récupérées : {len(df)}")

        # 🔹 Fonction de nettoyage du texte
        def clean_text(text):
            text = text.lower()  # Minuscule
            text = re.sub(r'[^\w\s]', '', text)  # Suppression des caractères spéciaux
            return text

        df['text_clean'] = df['text'].apply(clean_text)
        logging.info("Nettoyage du texte terminé")

        # Vérifier la distribution des classes avant la séparation des données
        logging.info(f"Distribution des classes (positif) avant la séparation : {df['positive'].value_counts().to_dict()}")
        logging.info(f"Distribution des classes (négatif) avant la séparation : {df['negative'].value_counts().to_dict()}")

        # 🔹 Stopwords français (à filtrer dans la vectorisation)
        french_stopwords = [
            "le", "la", "les", "un", "une", "des", "du", "de", "dans", "et", "en", "au",
            "aux", "avec", "ce", "ces", "pour", "par", "sur", "pas", "plus", "où", "mais",
            "ou", "donc", "ni", "car", "ne", "que", "qui", "quoi", "quand", "à", "son",
            "sa", "ses", "ils", "elles", "nous", "vous", "est", "sont", "cette", "cet",
            "aussi", "être", "avoir", "faire", "comme", "tout", "bien", "mal", "on", "lui"
        ]

        vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
        X = vectorizer.fit_transform(df['text_clean'])
        y_positive = df['positive']
        y_negative = df['negative']

        # 🔹 Séparation des données en train/test
        X_train_pos, X_test_pos, y_train_positive, y_test_positive = train_test_split(X, y_positive, test_size=0.25, random_state=42)
        X_train_neg, X_test_neg, y_train_negative, y_test_negative = train_test_split(X, y_negative, test_size=0.25, random_state=42)

        # Vérifier la distribution des classes après la séparation des données
        logging.info(f"Distribution des classes dans y_train_positive : {pd.Series(y_train_positive).value_counts().to_dict()}")
        logging.info(f"Distribution des classes dans y_train_negative : {pd.Series(y_train_negative).value_counts().to_dict()}")

        # Vérifier si les classes sont équilibrées
        if len(y_train_positive.unique()) < 2 or len(y_train_negative.unique()) < 2:
            logging.error("Les données d'entraînement ne contiennent pas suffisamment de classes pour l'entraînement.")
            return

        # 🔹 Entraînement du modèle de régression logistique pour les tweets positifs
        model_positive = LogisticRegression()
        model_positive.fit(X_train_pos, y_train_positive)

        # 🔹 Entraînement du modèle de régression logistique pour les tweets négatifs
        model_negative = LogisticRegression()
        model_negative.fit(X_train_neg, y_train_negative)

        # 🔹 Prédictions et évaluation du modèle pour les tweets positifs
        y_pred_positive = model_positive.predict(X_test_pos)
        logging.info("Rapport de classification (positif) :")
        logging.info("\n" + classification_report(y_test_positive, y_pred_positive))

        logging.info("Matrice de confusion (positif) :")
        logging.info("\n" + str(confusion_matrix(y_test_positive, y_pred_positive)))

        # 🔹 Prédictions et évaluation du modèle pour les tweets négatifs
        y_pred_negative = model_negative.predict(X_test_neg)
        logging.info("Rapport de classification (négatif) :")
        logging.info("\n" + classification_report(y_test_negative, y_pred_negative))

        logging.info("Matrice de confusion (négatif) :")
        logging.info("\n" + str(confusion_matrix(y_test_negative, y_pred_negative)))

    except Exception as e:
        logging.error("Erreur lors du réentraînement du modèle : %s", e)

if __name__ == "__main__":
    retrain_model()