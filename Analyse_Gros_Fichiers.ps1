Write-Output "Sélection du répertoire de base..."

$rep_base = python select_repertoire.py

if (-not $rep_base) {
    Write-Output "Aucun répertoire sélectionné"
    exit
}

if (-not (Test-Path $rep_base)) {
    Write-Output "Répertoire invalide"
    exit
}

python analyse_fichiers.py $rep_base
python affichage_resultats.py
