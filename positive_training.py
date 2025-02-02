import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix

data_positive = {
    "text": [
        "J'adore ce film, c'est un chef-d'œuvre !", # Positif
        "Un plat délicieux, merci pour la recette !", # Positif
        "Un plat qu'on peut manger, voilà tout.", # Neutre
        "C'était immangeable, horrible expérience.", # Négatif
        "Tu es une personne inspirante, merci !", # Positif
        "Tu es une personne comme une autre.", # Neutre
        "Tu es tellement agaçant, insupportable.", # Négatif
        "Super travail, continuez comme ça !", # Positif
        "C'est un travail correct, rien d'exceptionnel.", # Neutre
        "Travail bâclé, très décevant.", # Négatif
        "Quel film incroyable, une belle découverte !", # Positif
        "Un film qui fait son job.", # Neutre
        "Film raté, je regrette de l'avoir regardé.", # Négatif
        "J'aime bien cette musique, elle me met de bonne humeur !", # Positif
        "Cette musique existe, c'est tout.", # Neutre
        "Cette musique est insupportable, horrible.", # Négatif
        "Superbe initiative, bravo !", # Positif
        "Une initiative comme une autre.", # Neutre
        "Mauvaise idée, complètement inutile.", # Négatif
        "J'apprécie vraiment cette discussion constructive !", # Positif
        "C'est une discussion, comme toutes les autres.", # Neutre
        "Cette discussion est stérile et sans intérêt.", # Négatif
        "J'adore ce film, c'est un chef-d'œuvre !", # Positif
        "Pas correct, tu as tout gaché.", # Négatif
    ],
    "label": [
        1, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0
    ]
}

df = pd.DataFrame(data_positive)

#Fonction de nettoyage
def clean_text(text):
    text = text.lower() # Mettre en minuscule
    text = re.sub(r'[^\w\s]', '', text) # Supprimer les caractères spéciaux
    return text

df['text_clean'] = df['text'].apply(clean_text)
french_stopwords = [
    "le", "la", "les", "un", "une", "des", "du", "de", "dans", "et", "en", "au",
    "aux", "avec", "ce", "ces", "pour", "par", "sur", "pas", "plus", "où", "mais",
    "ou", "donc", "ni", "car", "ne", "que", "qui", "quoi", "quand", "à", "son",
    "sa", "ses", "ils", "elles", "nous", "vous", "est", "sont", "cette", "cet",
    "aussi", "être", "avoir", "faire", "comme", "tout", "bien", "mal", "on", "lui"
]

# Vectorisation (bag of words)
vectorizer = CountVectorizer(stop_words=french_stopwords, max_features=100)
X = vectorizer.fit_transform(df['text_clean'])
y = df['label']
print("Vectorisation terminée.")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)
print("Modèle entraîné avec succès.")

# Prédictions
y_pred = model.predict(X_test)
# Rapport de classification
print("Rapport de classification :")
print(classification_report(y_test, y_pred))
# Matrice de confusion
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# Prédictions
y_pred = model.predict(X_test)
# Rapport de classification
print("Rapport de classification :")
print(classification_report(y_test, y_pred))
# Matrice de confusion
print("Matrice de confusion :")
print(confusion_matrix(y_test, y_pred))

# Nouvelles données
new_comments = [
    "Je ne supporte pas cette personne.", # negative
    "Cette vidéo est incroyable, merci pour votre travail.", # positive
    "Arrête de dire n'importe quoi, imbécile.", # negative
    "Une excellente présentation, bravo à toute l'équipe.", # positive
    "Ta gueule!!!", # negative
    "Imbécile" # negative
]

# Nettoyage et vectorisation
new_comments_clean = [clean_text(comment) for comment in new_comments]
new_comments_vectorized = vectorizer.transform(new_comments_clean)

# Prédictions
predictions = model.predict(new_comments_vectorized)
for comment, label in zip(new_comments, predictions):
    print(f"Commentaire : '{comment}' -> {'Positive' if label == 1 else 'Else'}")

