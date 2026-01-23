import sys
import json
from pathlib import Path

TAILLE_MINI_MIB = 1
NB_MAXI_FICHIERS = 100

def analyse_arborescence(repertoire_base):
    fichiers = []
    for file in Path(repertoire_base).rglob("*"):
        if file.is_file():
            fichiers.append([str(file.resolve()), file.stat().st_size])
    return fichiers

def tri_decroissant(liste):
    return sorted(liste, key=lambda x: x[1], reverse=True)

def filtrage(liste, taille_mini_mib, nb_max):
    taille_min_octets = taille_mini_mib * 1048576
    liste_filtree = [f for f in liste if f[1] >= taille_min_octets]
    return liste_filtree[:nb_max]

def sauvegarde_json(liste, nom_fichier):
    # Échapper les backslashes pour compatibilité JSON sur Windows
    for f in liste:
        f[0] = f[0].replace("\\", "\\\\")
    with open(nom_fichier, "w", encoding="utf-8") as f:
        json.dump(liste, f, indent=2)

if __name__ == "__main__":
    # Acceptation d'arguments : <repertoire_base> <fichier_sortie>
    if len(sys.argv) >= 2:
        repertoire = sys.argv[1]
    else:
        repertoire = str(Path.home())

    if len(sys.argv) >= 3:
        nom_fichier = sys.argv[2]
    else:
        nom_fichier = "resultats.json"

    fichiers = analyse_arborescence(repertoire)
    fichiers = tri_decroissant(fichiers)
    fichiers = filtrage(fichiers, TAILLE_MINI_MIB, NB_MAXI_FICHIERS)
    sauvegarde_json(fichiers, nom_fichier)
