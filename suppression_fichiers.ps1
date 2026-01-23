Write-Output "==============================================="
Write-Output " Suppression de fichiers volumineux"
Write-Output " ATTENTION : SUPPRESSION DEFINITIVE"
Write-Output "==============================================="
Write-Output ""

$jsonFile = "resultat_gros_fichiers.json"

if (-not (Test-Path $jsonFile)) {
    Write-Output "❌ Fichier JSON introuvable."
    exit
}

$fichiers = Get-Content $jsonFile | ConvertFrom-Json

Write-Output "Liste des fichiers détectés :"
Write-Output ""

for ($i = 0; $i -lt $fichiers.Count; $i++) {
    $chemin = $fichiers[$i][0]
    $taille = [math]::Round($fichiers[$i][1] / 1MB, 2)
    Write-Output "[$i] $chemin ($taille MiB)"
}

Write-Output ""
Write-Output "Entrez les numéros des fichiers à supprimer"
Write-Output "Exemple : 0,3,7"
$selection = Read-Host "Votre sélection"

if (-not $selection) {
    Write-Output "❌ Aucune sélection."
    exit
}

$indexes = $selection -split "," | ForEach-Object { $_.Trim() }

# -----------------------------------------------
# Double confirmation
# -----------------------------------------------
$reponse = Read-Host "Confirmez-vous la suppression ? (OUI)"
if ($reponse -ne "OUI") { exit }

$confirmation = Read-Host "Etes-vous bien certain(e) ? (OUI)"
if ($confirmation -ne "OUI") { exit }

# -----------------------------------------------
# Suppression
# -----------------------------------------------
Write-Output ""
Write-Output "Suppression en cours..."
Write-Output ""

foreach ($index in $indexes) {

    if ($index -match '^\d+$' -and $index -lt $fichiers.Count) {

        $chemin = $fichiers[$index][0]

        if (Test-Path $chemin) {
            Remove-Item -Path $chemin -Force
            Write-Output "✔ Supprimé : $chemin"
        } else {
            Write-Output "⚠ Fichier introuvable : $chemin"
        }

    } else {
        Write-Output "⚠ Index invalide : $index"
    }
}

Write-Output ""
Write-Output "Fin du script de suppression."
