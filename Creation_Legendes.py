#--------------------------------------------------------
# Script : Creation_Legendes.py
# Destiné à la SAE 1.05 : traitement des données
# Dev : O. ECKLE - Ver : 1.1 - Janvier 2026
#--------------------------------------------------------

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QCheckBox
from PyQt5.QtCore import Qt

class Legendes:
    """
    Création d'un objet graphique contenant une série de lignes de légendes.
    """

    def __init__(self, liste_fichiers, liste_couleurs, num_legende_start, nb_legende_par_page=25):
        self.liste_fichiers = liste_fichiers
        self.liste_couleurs = liste_couleurs
        self.num_legende_start = num_legende_start
        self.nb_legende_par_page = nb_legende_par_page
        self.num_legende_stop = min(
            len(liste_fichiers),
            num_legende_start + self.nb_legende_par_page
        )
        self.cases_a_cocher = []

    def dessine_legendes(self):
        """
        Retourne un QWidget contenant une liste de légendes.
        """

        widget = QWidget()
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setAlignment(Qt.AlignTop)

        for num_slice in range(self.num_legende_start, self.num_legende_stop):
            case = QCheckBox()
            self.cases_a_cocher.append(case)

            rectangle = QWidget()
            rectangle.setFixedSize(16, 16)
            couleur = self.liste_couleurs[num_slice].name()
            rectangle.setStyleSheet(
                f"background-color: {couleur}; border: 1px solid black;"
            )

            chemin = self.liste_fichiers[num_slice][0]
            taille = self.liste_fichiers[num_slice][1] // 1048576
            texte = QLabel(
                f"<span style='font-family:Arial Narrow'>{chemin} → </span>"
                f"<span style='color:red'>{taille} MiB</span>"
            )

            ligne = QHBoxLayout()
            ligne.setAlignment(Qt.AlignLeft)
            ligne.setContentsMargins(5, 0, 5, 5)
            ligne.addWidget(case)
            ligne.addWidget(rectangle)
            ligne.addWidget(texte)

            ligne_widget = QWidget()
            ligne_widget.setLayout(ligne)

            layout.addWidget(ligne_widget)

        return widget

    def recupere_etats_case_a_cocher(self):
        """
        Retourne la liste des états des cases à cocher.
        """
        return [case.isChecked() for case in self.cases_a_cocher]
