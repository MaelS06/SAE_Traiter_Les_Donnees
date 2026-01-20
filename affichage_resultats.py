import sys
import json
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor

from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

NB_LEGENDES_PAR_PAGE = 25

def lire_json():
    with open("resultats.json", "r", encoding="utf-8") as f:
        return json.load(f)

def couleurs_aleatoires(n):
    return [QColor(random.randint(0,255),
                   random.randint(0,255),
                   random.randint(0,255)) for _ in range(n)]

def creation_script_suppression():
    lignes = []
    lignes.append('Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"')
    lignes.append('$reponse = Read-Host "Confirmer ? (OUI)"')
    lignes.append('if ($reponse -eq "OUI") {')

    for page in liste_legendes:
        etats = page.recupere_etats_case_a_cocher()
        for i, etat in enumerate(etats):
            if etat:
                index = page.num_legende_start + i
                path = liste_fichiers[index][0]
                lignes.append(f'  Remove-Item -Path "{path}" -Force')

    lignes.append('}')

    with open("suppression.ps1", "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

if __name__ == "__main__":
    liste_fichiers = lire_json()
    liste_couleurs = couleurs_aleatoires(len(liste_fichiers))

    app = QApplication(sys.argv)
    fenetre = Onglets()

    cam = Camembert(liste_fichiers, liste_couleurs)
    fenetre.add_onglet("Camembert", cam.dessine_camembert())

    liste_legendes = []
    for i in range(0, len(liste_fichiers), NB_LEGENDES_PAR_PAGE):
        leg = Legendes(liste_fichiers, liste_couleurs, i)
        liste_legendes.append(leg)
        fenetre.add_onglet(f"Légende {i//25 + 1}", leg.dessine_legendes())

    ihm = Boutons("Répertoire de base", creation_script_suppression)
    fenetre.add_onglet("IHM", ihm.dessine_boutons())

    fenetre.show()
    sys.exit(app.exec_())
