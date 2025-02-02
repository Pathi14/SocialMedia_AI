import pandas as pd
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix


data_negative = {
    "text": [
        "Un événement standard, pas de surprise.", # Neutre
        "Un événement parfait, super bien organisé !", # Positif
        "Un repas immangeable, une horreur.", # Négatif
        "Un plat qui se mange, rien de spécial.", # Neutre
        "Un des meilleurs repas de ma vie, succulent !", # Positif
        "Service lent et désagréable, je ne reviendrai pas.", # Négatif
        "Un service correct, sans plus.", # Neutre
        "Un personnel aux petits soins, expérience formidable !", # Positif
        "Je me suis fait arnaquer avec ce site, à éviter absolument.", # Négatif
        "Un site fonctionnel mais pas très attractif.", # Neutre
        "Un site super intuitif et efficace, je recommande !", # Positif
        "Les délais de livraison sont un cauchemar, très déçu.", # Négatif
        "La livraison a pris du temps, mais est arrivée.", # Neutre
        "Livraison ultra rapide, super service !", # Positif
        "Expérience client catastrophique, je déconseille vivement.", # Négatif
        "Une expérience correcte, sans éclat.", # Neutre
        "Une expérience fluide et agréable, bravo !", # Positif
        "Un appareil qui tombe en panne après une semaine, honteux !", # Négatif
        "Un appareil standard, il fait son travail.", # Neutre
        "Un appareil fiable et performant, excellent achat !", # Positif
         "Je n'ai jamais vu un service client aussi inefficace.", # Négatif
    ],
    "label": [
        0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 1
    ]
}

df = pd.DataFrame(data_negative)

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
    "Ce produit est une arnaque totale, à fuir !", # Négatif
    "C'est un produit comme un autre, rien de spécial.", # Neutre
    "J'adore ce produit, il est génial !", # Positif
    "Ce restaurant a un service exécrable, très déçu.", # Négatif
    "Un restaurant correct, sans plus.", # Neutre
    "Une expérience culinaire incroyable, bravo !", # Positif
]

# Nettoyage et vectorisation
new_comments_clean = [clean_text(comment) for comment in new_comments]
new_comments_vectorized = vectorizer.transform(new_comments_clean)

# Prédictions
predictions = model.predict(new_comments_vectorized)
for comment, label in zip(new_comments, predictions):
    print(f"Commentaire : '{comment}' -> {'Negative' if label == 1 else 'Else'}")

