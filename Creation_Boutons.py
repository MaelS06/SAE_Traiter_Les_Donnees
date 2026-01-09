# --------------------------------------------------------
# Script : Creation_Boutons.py
# Destiné à la SAE 1.05 : traitement des données
# Dev : O. ECKLE - Ver : 1.1 - Janvier 2026
# --------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

class Boutons:
    """
    Création d'un objet graphique contenant un bouton et une zone de texte.
    """

    def __init__(self, repertoire_base, callback):
        self.repertoire_base = repertoire_base
        self.callback = callback

    def dessine_boutons(self):
        """
        Retourne un QWidget contenant un bouton et une zone de texte.
        """

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)

        bouton = QPushButton("Créer le script PowerShell de suppression des fichiers")
        bouton.setFixedSize(500, 40)
        bouton.clicked.connect(self.callback)
        layout.addWidget(bouton, alignment=Qt.AlignHCenter)

        texte_rep = QLineEdit()
        texte_rep.setText(self.repertoire_base)
        texte_rep.setFixedSize(490, 30)
        texte_rep.setReadOnly(True)
        layout.addWidget(texte_rep, alignment=Qt.AlignHCenter)

        return widget
