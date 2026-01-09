import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from pathlib import Path

def selection_repertoire():
    """
    Ouvre une boîte de dialogue permettant de sélectionner un répertoire.
    Retourne le chemin sélectionné sous forme de chaîne.
    """
    repertoire = QFileDialog.getExistingDirectory(
        None,
        "Sélectionnez le répertoire de base",
        str(Path.home())
    )
    return repertoire

if __name__ == "__main__":
    selection_repertoire()

