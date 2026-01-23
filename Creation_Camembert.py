#--------------------------------------------------------
# Script : Creation_Camembert.py
# Destiné à la SAE 1.05 : traitement des données
# Dev : O. ECKLE - Ver : 1.2 - Janvier 2026
#--------------------------------------------------------

from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class Camembert:
    """
    Création d'un objet graphique contenant une représentation
    statistique sous forme de camembert.
    """

    def __init__(self, liste_fichiers, liste_couleurs):
        self.liste_fichiers = liste_fichiers
        self.liste_couleurs = liste_couleurs

    def dessine_camembert(self):
        """
        Retourne un QWidget contenant un graphique circulaire type camembert.
        """

        # Si aucune donnée, retourner un widget informatif au lieu de lever une exception
        if not self.liste_fichiers:
            container = QWidget()
            layout = QVBoxLayout(container)
            label = QLabel("Aucun fichier à afficher. Exécutez d'abord l'analyse ou vérifiez le filtre de taille.")
            label.setAlignment(Qt.AlignCenter)
            layout.addWidget(label)
            return container

        # Création de la série de données
        series = QPieSeries()
        series.setLabelsVisible(True)

        # Calcul de la taille totale
        taille_totale = sum(fichier[1] for fichier in self.liste_fichiers)

        # Police des étiquettes
        font = QFont("Arial Narrow", 12, QFont.Bold)

        # Création des tranches
        for index, (chemin, taille) in enumerate(self.liste_fichiers):
            etiquette = f"{taille // 1048576} MiB"
            # On ajoute la valeur en octets ; QPieSeries calculera automatiquement les proportions
            slice_ = series.append(etiquette, taille)

            if index < len(self.liste_couleurs):
                slice_.setBrush(self.liste_couleurs[index])

            slice_.setLabelFont(font)
            # Position correcte de l'étiquette
            slice_.setLabelPosition(QPieSlice.LabelOutside)

        # Affichage des étiquettes seulement pour les grosses tranches
        for slice_ in series.slices():
            slice_.setLabelVisible(slice_.angleSpan() > 6)

        # Création du graphique
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Répartition des tailles des fichiers")
        chart.legend().hide()

        view = QChartView(chart)

        # Conteneur QWidget attendu par Onglets.add_onglet
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(view)
        return container
