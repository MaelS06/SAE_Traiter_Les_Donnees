import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from pathlib import Path

def selection_repertoire():
    app = QApplication(sys.argv)
    repertoire = QFileDialog.getExistingDirectory(
        None,
        "Sélectionnez le répertoire de base",
        str(Path.home())
    )
    return repertoire

if __name__ == "__main__":
    rep = selection_repertoire()
    if rep:
        print(rep)
