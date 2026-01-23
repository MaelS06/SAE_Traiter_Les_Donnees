# --------------------------------------------------------
# Script : Creation_Boutons.py
# Destiné à la SAE 1.05 : traitement des données
# Dev : O. ECKLE - Ver : 1.2 - Janvier 2026
# --------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QListWidget, QListWidgetItem, QMessageBox
from PyQt5.QtCore import Qt
import os

class Boutons:
    """
    Création d'un objet graphique contenant des boutons et une liste de fichiers.
    Boutons:
      - Générer le script PowerShell de suppression (suppression.ps1)
      - Supprimer la sélection (demande confirmation)
    La classe attend que `liste_fichiers` soit passée lors de la création.
    """

    def __init__(self, liste_fichiers):
        self.liste_fichiers = liste_fichiers

    def dessine_boutons(self):
        """Retourne un QWidget contenant les contrôles pour gérer la suppression de fichiers."""
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setAlignment(Qt.AlignTop)
        layout.setSpacing(10)

        # Liste des fichiers
        self.liste_widget = QListWidget()
        for path, taille in self.liste_fichiers:
            item = QListWidgetItem(f"{path} ({taille // 1048576} MiB)")
            item.setData(Qt.UserRole, path)
            self.liste_widget.addItem(item)
        self.liste_widget.setSelectionMode(QListWidget.ExtendedSelection)
        layout.addWidget(self.liste_widget)

        # Bouton pour supprimer la sélection
        btn_supprimer = QPushButton("Supprimer la sélection")
        btn_supprimer.clicked.connect(self.supprimer_selection)
        layout.addWidget(btn_supprimer)

        # Bouton pour générer le script PowerShell
        btn_script = QPushButton("Générer script PowerShell de suppression")
        btn_script.clicked.connect(self.generer_script)
        layout.addWidget(btn_script)

        return container

    def supprimer_selection(self):
        items = self.liste_widget.selectedItems()
        if not items:
            QMessageBox.information(None, "Information", "Aucun fichier sélectionné.")
            return

        reply = QMessageBox.question(None, "Confirmation", f"Supprimer {len(items)} fichier(s) sélectionné(s) ?",
                                     QMessageBox.Yes | QMessageBox.No)
        if reply != QMessageBox.Yes:
            return

        erreurs = []
        for item in items:
            path = item.data(Qt.UserRole)
            try:
                os.remove(path)
                self.liste_widget.takeItem(self.liste_widget.row(item))
            except Exception as e:
                erreurs.append((path, str(e)))

        if erreurs:
            texte = "Certains fichiers n'ont pas pu être supprimés:\n"
            for p, err in erreurs:
                texte += f"{p} -> {err}\n"
            QMessageBox.warning(None, "Erreurs", texte)
        else:
            QMessageBox.information(None, "Succès", "Fichiers supprimés avec succès.")

    def generer_script(self):
        lignes = []
        lignes.append('Write-Output "Script PowerShell pour supprimer des fichiers sans confirmation"')
        lignes.append('$reponse = Read-Host "Confirmer ? (OUI)"')
        lignes.append('if ($reponse -eq "OUI") {')

        for index in range(self.liste_widget.count()):
            item = self.liste_widget.item(index)
            path = item.data(Qt.UserRole)
            lignes.append(f'  Remove-Item -Path "{path}" -Force')

        lignes.append('}')

        try:
            with open("suppression.ps1", "w", encoding="utf-8") as f:
                f.write("\n".join(lignes))
            QMessageBox.information(None, "Succès", "Le script suppression.ps1 a été généré.")
        except Exception as e:
            QMessageBox.warning(None, "Erreur", f"Impossible d'écrire le script: {e}")
