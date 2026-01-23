Write-Output "==============================================="
Write-Output " SAE 1.05 - Analyse des gros fichiers"
Write-Output "==============================================="
Write-Output ""

# -----------------------------------------------
# Configuration
# -----------------------------------------------
$python = "python"
$script_selecteur = "select_repertoire.py"
$script_analyse   = "analyse_fichiers.py"
$script_affichage = "Creation_Camembert.py"
$fichier_json     = "resultat_gros_fichiers.json"

# -----------------------------------------------
# Sélection du répertoire
# -----------------------------------------------
Write-Output "Sélection du répertoire à analyser..."
$rep_base = & $python $script_selecteur
if (-not $rep_base) {
    Write-Output "Répertoire invalide. Fin du script."
    exit
}
$rep_base = $rep_base.Trim()

if (-not $rep_base -or -not (Test-Path $rep_base)) {
    Write-Output "❌ Répertoire invalide. Fin du script."
    exit
}

Write-Output "✔ Répertoire sélectionné : $rep_base"

# -----------------------------------------------
# Analyse de l'arborescence
# -----------------------------------------------
Write-Output ""
Write-Output "Analyse en cours..."
& $python $script_analyse $rep_base $fichier_json

if (-not (Test-Path $fichier_json)) {
    Write-Output "❌ Le fichier JSON n'a pas été créé."
    exit
}

Write-Output "✔ Analyse terminée"

# -----------------------------------------------
# Lancement de l'IHM
# -----------------------------------------------
Write-Output ""
Write-Output "Ouverture de l'interface graphique..."
& $python $script_affichage $rep_base $fichier_json

Write-Output ""
Write-Output "Fin du script principal."
