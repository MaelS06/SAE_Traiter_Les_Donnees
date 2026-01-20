import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from pathlib import Path

def selection_repertoire():
    app = QApplication(sys.argv)

    repertoire = QFileDialog.getExistingDirectory(
        None,
        "Sélectionnez le répertoire de base"
    )

    if repertoire:
        print(str(Path(repertoire)))
    else:
        print("")

    app.exit()

if __name__ == "__main__":
    selection_repertoire()
