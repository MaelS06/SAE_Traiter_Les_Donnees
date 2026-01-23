import sys
import json
import random
import os
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtGui import QColor

from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

NB_LEGENDES_PAR_PAGE = 25

def lire_json(nom_fichier):
    with open(nom_fichier, "r", encoding="utf-8") as f:
        return json.load(f)

def couleurs_aleatoires(n):
    return [QColor(random.randint(0,255),
                   random.randint(0,255),
                   random.randint(0,255)) for _ in range(n)]

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        nom_fichier = sys.argv[1]
    else:
        nom_fichier = "resultats.json"

    if not os.path.exists(nom_fichier):
        # Si on est lancé depuis une console (ex. PowerShell), on écrit sur stdout.
        print(f"Fichier '{nom_fichier}' introuvable. Exécutez d'abord l'analyse pour générer ce fichier.")
        sys.exit(2)

    liste_fichiers = lire_json(nom_fichier)
    liste_couleurs = couleurs_aleatoires(len(liste_fichiers))

    app = QApplication(sys.argv)
    fenetre = Onglets()

    cam = Camembert(liste_fichiers, liste_couleurs)
    fenetre.add_onglet("Camembert", cam.dessine_camembert())

    liste_legendes = []
    for i in range(0, len(liste_fichiers), NB_LEGENDES_PAR_PAGE):
        leg = Legendes(liste_fichiers, liste_couleurs, i)
        liste_legendes.append(leg)
        fenetre.add_onglet(f"Légende {i//NB_LEGENDES_PAR_PAGE + 1}", leg.dessine_legendes())

    ihm = Boutons(liste_fichiers)
    fenetre.add_onglet("IHM", ihm.dessine_boutons())

    fenetre.show()
    sys.exit(app.exec_())
