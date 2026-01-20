# --------------------------------------------------------
# Script : Creation_Boutons.py
# Destiné à la SAE 1.05 : traitement des données
# Dev : O. ECKLE - Ver : 1.1 - Janvier 2026
# --------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt
class Boutons:
    """
    Création d'un objet graphique contenant un bouton et une textBox.
    Création d'un objet graphique contenant un bouton et une zone de texte.

    def __init__(self, repertoire_base, callback):
    def __init__(self, repertoire_base, callback):
        self.repertoire_base = repertoire_base
        self.callback = callback
                Retourne une Widget Layout PyQt contenant un bouton et une textBox.
        """

        Retourne un QWidget contenant un bouton et une zone de texte.
        boutons = QWidget()

        zone_boutons = QVBoxLayout(boutons)
        zone_boutons.setSpacing(10)
        zone_boutons.setAlignment(Qt.AlignTop)

        # Création du Bouton
        bouton = QPushButton("Créer le script PowerShell de suppression des fichiers")
        bouton.setFixedSize(500, 40)
        bouton.clicked.connect(self.callback)
        layout.addWidget(bouton, alignment=Qt.AlignHCenter)
