from pathlib import Path
import json
import sys

TAILLE_MIN_MIB = 1
NB_MAX_FICHIERS = 100
NOM_FICHIER_JSON = "resultat.json"

# --------------------------------------------------
def inventaire_fichiers(repertoire_base):
    fichiers = []
    base = Path(repertoire_base)

    for element in base.rglob("*"):
        if element.is_file():
            fichiers.append([str(element.resolve()), element.stat().st_size])

    return fichiers

# --------------------------------------------------
def tri_par_taille_decroissante(liste_fichiers):
    return sorted(liste_fichiers, key=lambda x: x[1], reverse=True)

# --------------------------------------------------
def filtre_gros_fichiers(liste_fichiers):
    limite_octets = TAILLE_MIN_MIB * 1048576
    resultat = []

    for fichier in liste_fichiers:
        if fichier[1] >= limite_octets:
            resultat.append(fichier)
        if len(resultat) == NB_MAX_FICHIERS:
            break

    return resultat

# --------------------------------------------------
def ecriture_json(liste_fichiers):
    for fichier in liste_fichiers:
        fichier[0] = fichier[0].replace("\\", "\\\\")

    with open(NOM_FICHIER_JSON, "w", encoding="utf-8") as f:
        json.dump(liste_fichiers, f, indent=2)

# --------------------------------------------------
if __name__ == "__main__":
    repertoire = sys.argv[1]

    fichiers = inventaire_fichiers(repertoire)
    fichiers_tries = tri_par_taille_decroissante(fichiers)
    gros_fichiers = filtre_gros_fichiers(fichiers_tries)
    ecriture_json(gros_fichiers)
