import sys
import json
import random
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QColor
import platform

from Creation_Onglets import Onglets
from Creation_Camembert import Camembert
from Creation_Legendes import Legendes
from Creation_Boutons import Boutons

NB_LEGENDES_PAR_PAGE = 25
NOM_JSON = "resultat.json"

# --------------------------------------------------
def lecture_json():
    with open(NOM_JSON, "r", encoding="utf-8") as f:
        return json.load(f)

# --------------------------------------------------
def genere_couleurs(nb):
    couleurs = []
    for _ in range(nb):
        couleurs.append(QColor(
            random.randint(0,255),
            random.randint(0,255),
            random.randint(0,255)
        ))
    return couleurs

# --------------------------------------------------
def creation_script_suppression():
    lignes = [
        'Write-Output "Script PowerShell pour supprimer des fichiers"',
        'Write-Output "Attention : cette suppression est définitive"',
        '$rep = Read-Host "Confirmez la suppression (OUI)"',
        'if ($rep -eq "OUI") {',
        ' $conf = Read-Host "Êtes-vous vraiment sûr(e) ? (OUI)"',
        ' if ($conf -eq "OUI") {'
    ]

    for leg in liste_legendes:
        etats = leg.recupere_etats_case_a_cocher()
        index = leg.num_legende_start

        for i, etat in enumerate(etats):
            if etat:
                chemin = fichiers[index + i][0]
                lignes.append(f'  Remove-Item -Path "{chemin}" -Force')

    lignes.extend([
        ' } else { Write-Output "Opération annulée" }',
        '} else { Write-Output "Opération annulée" }'
    ])

    with open("suppression.ps1", "w", encoding="utf-8") as f:
        f.write("\n".join(lignes))

# --------------------------------------------------
if __name__ == "__main__":
    app = QApplication(sys.argv)

    fichiers = lecture_json()
    couleurs = genere_couleurs(len(fichiers))

    fenetre = Onglets()

    camembert = Camembert(fichiers, couleurs)
    fenetre.add_onglet("Camembert", camembert.dessine_camembert())

    liste_legendes = []
    for i in range(0, len(fichiers), NB_LEGENDES_PAR_PAGE):
        leg = Legendes(fichiers, couleurs, i)
        liste_legendes.append(leg)
        fenetre.add_onglet(f"Légende {i//NB_LEGENDES_PAR_PAGE + 1}", leg.dessine_legendes())

    ihm = Boutons("Répertoire de base", creation_script_suppression)
    fenetre.add_onglet("IHM", ihm.dessine_boutons())

    fenetre.show()
    sys.exit(app.exec_())
