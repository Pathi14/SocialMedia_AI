import sqlite3
import random

# Connexion à la base de données
connection = sqlite3.connect('database.db')
cur = connection.cursor()

# Création manuelle de la table si elle n'existe pas
cur.execute("""
    CREATE TABLE IF NOT EXISTS tweets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        text TEXT NOT NULL,
        positive INTEGER NOT NULL,
        negative INTEGER NOT NULL
    );
""")

# Liste de tweets positifs et négatifs mélangés
tweets = [
    ("J'adore cette vidéo, super travail !", 1, 0),
    ("Expérience horrible, je suis très déçu.", 0, 1),
    ("Merci pour ce merveilleux moment !", 1, 0),
    ("Produit de très mauvaise qualité, à éviter.", 0, 1),
    ("Ce restaurant est incroyable, j'y retournerai.", 1, 0),
    ("Service client désastreux, une honte.", 0, 1),
    ("Super service, rapide et efficace !", 1, 0),
    ("Livraison en retard, très frustrant.", 0, 1),
    ("Un chef-d'œuvre, je recommande vivement.", 1, 0),
    ("Film ennuyant, je me suis endormi.", 0, 1),
    ("La nourriture était exquise, un régal !", 1, 0),
    ("Un désastre, je ne reviendrai plus jamais.", 0, 1),
    ("Cette musique me donne des frissons, magnifique.", 1, 0),
    ("Le produit était cassé à la réception.", 0, 1),
    ("J'aime beaucoup cette application, très utile.", 1, 0),
    ("Publicité mensongère, je suis furieux.", 0, 1),
    ("Je suis ravi de cet achat, parfait !", 1, 0),
    ("Service lamentable, à éviter absolument.", 0, 1),
    ("Le livre était passionnant, je l'ai adoré.", 1, 0),
    ("Une énorme déception, je ne recommande pas.", 0, 1),
    ("Un accueil chaleureux, merci pour tout !", 1, 0),
    ("Le site est mal conçu, une horreur.", 0, 1),
    ("Un excellent rapport qualité/prix.", 1, 0),
    ("Le film était un vrai désastre.", 0, 1),
    ("Une expérience client impeccable, bravo.", 1, 0),
    ("Je regrette cet achat, très décevant.", 0, 1),
    ("Une conférence très enrichissante, top !", 1, 0),
    ("Un service client inexistant, honteux.", 0, 1),
    ("Je suis impressionné par la qualité.", 1, 0),
    ("Je ne recommande pas du tout ce produit.", 0, 1),
    ("Le décor était magnifique, magique.", 1, 0),
    ("Un serveur désagréable, une honte.", 0, 1),
    ("Une application fluide et pratique.", 1, 0),
    ("Produit inutilisable, une perte d'argent.", 0, 1),
    ("Un souvenir inoubliable, merci à vous !", 1, 0),
    ("Le spectacle était catastrophique.", 0, 1),
    ("Une formation claire et bien expliquée.", 1, 0),
    ("Un film médiocre, perte de temps.", 0, 1),
    ("J'ai adoré cet événement, superbe !", 1, 0),
    ("Un repas infect, immangeable.", 0, 1),
    ("Une équipe formidable, bravo !", 1, 0),
    ("J'ai été très mal accueilli, décevant.", 0, 1),
    ("Le jeu est super addictif, j'adore !", 1, 0),
    ("Je suis très en colère, arnaque totale.", 0, 1),
    ("Une performance époustouflante, incroyable !", 1, 0),
    ("Un service trop lent, vraiment pénible.", 0, 1),
    ("Le meilleur hôtel où j'ai séjourné.", 1, 0),
    ("Produit arrivé en retard, frustrant.", 0, 1),
    ("Je me suis régalé, quel bon plat !", 1, 0),
    ("Une vraie perte de temps, zéro intérêt.", 0, 1),
    ("Une innovation géniale, bravo !", 1, 0),
    ("Le SAV est une blague, personne ne répond.", 0, 1),
    ("J'adore ce style, tellement élégant.", 1, 0),
    ("Très mauvaise expérience, à éviter.", 0, 1),
    ("Un moment magique, merci à tous.", 1, 0),
    ("Film sans intérêt, j'ai détesté.", 0, 1),
    ("Expérience client parfaite, merci !", 1, 0),
    ("J'ai perdu mon argent avec ce site.", 0, 1),
    ("Un voyage parfait, organisation au top !", 1, 0),
    ("Un service exécrable, honteux.", 0, 1),
    ("Cette série est géniale, captivante.", 1, 0),
    ("La commande est arrivée incomplète.", 0, 1),
    ("Un projet innovant et inspirant.", 1, 0),
    ("Une plateforme inutilisable, trop de bugs.", 0, 1),
    ("C'est exactement ce que je recherchais !", 1, 0),
    ("Très mauvais goût, je déteste.", 0, 1),
    ("Un excellent concert, incroyable.", 1, 0),
    ("Les vendeurs sont désagréables, inadmissible.", 0, 1),
    ("Un film qui m'a marqué à jamais !", 1, 0),
    ("Une soirée ratée, très déçu.", 0, 1),
    ("J'ai découvert une vraie pépite, génial !", 1, 0),
    ("La connexion est trop lente, insupportable.", 0, 1),
    ("J'ai passé un moment magique, merci !", 1, 0),
    ("Une livraison désastreuse, colis abîmé.", 0, 1),
    ("J'apprécie vraiment cette équipe talentueuse.", 1, 0),
    ("Achat inutile, grosse arnaque.", 0, 1),
    ("C'était une discussion très intéressante.", 1, 0),
    ("Le logiciel plante tout le temps, nul.", 0, 1),
    ("Super article, très bien écrit !", 1, 0),
    ("Produit non conforme, grosse déception.", 0, 1),
    ("Une conférence inspirante, top !", 1, 0),
    ("Le personnel est incompétent, inacceptable.", 0, 1),
    ("Un cadre magnifique, expérience parfaite.", 1, 0),
    ("Film très mauvais, sans intérêt.", 0, 1),
    ("Merci pour votre accueil chaleureux.", 1, 0),
    ("Mauvais goût, je ne recommande pas.", 0, 1),
    ("Une expérience formidable, bravo !", 1, 0),
    ("Commande annulée sans explication.", 0, 1),
]

# Mélanger les tweets pour éviter tout regroupement
random.shuffle(tweets)

# Exécution de plusieurs insertions en une seule requête
cur.executemany("INSERT INTO tweets (text, positive, negative) VALUES (?, ?, ?)", tweets)

connection.commit()
connection.close()

print("✅ 100 tweets insérés avec succès !")
