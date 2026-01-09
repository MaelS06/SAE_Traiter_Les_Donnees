#--------------------------------------------------------
# Script : Creation_Camembert.py
# Destiné à la SAE 1.05 : traitement des données
# Dev : O. ECKLE - Ver : 1.1 - Janvier 2026
#--------------------------------------------------------

from PyQt5.QtChart import QChart, QChartView, QPieSeries
from PyQt5.QtGui import QFont

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

        if not self.liste_fichiers:
            raise ValueError("La liste doit contenir au moins un fichier.")

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
            pourcentage = taille / taille_totale * 100

            slice_ = series.append(etiquette, pourcentage)

            if index < len(self.liste_couleurs):
                slice_.setBrush(self.liste_couleurs[index])

            slice_.setLabelFont(font)
            slice_.setLabelPosition(slice_.LabelOutside)

        # Affichage des étiquettes seulement pour les grosses tranches
        for slice_ in series.slices():
            slice_.setLabelVisible(slice_.angleSpan() > 6)

        # Création du graphique
        chart = QChart()
        chart.addSeries(series)
        chart.setTitle("Répartition des tailles des fichiers")
        chart.legend().hide()

        return QChartView(chart)
