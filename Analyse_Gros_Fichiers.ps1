Write-Output "Lancement de l'analyse des gros fichiers..."

# Charger les assemblies WinForms pour les dialogues
Add-Type -AssemblyName System.Windows.Forms

# Dialogue de sélection du répertoire
$folderBrowser = New-Object System.Windows.Forms.FolderBrowserDialog
$folderBrowser.Description = 'Sélectionnez le répertoire de base'
$folderBrowser.SelectedPath = [Environment]::GetFolderPath('MyDocuments')
if ($folderBrowser.ShowDialog() -ne [System.Windows.Forms.DialogResult]::OK) {
    Write-Output "Aucun répertoire sélectionné."
    exit
}

$rep_base = $folderBrowser.SelectedPath
if (-not (Test-Path $rep_base)) {
    Write-Output "Répertoire invalide : $rep_base"
    exit
}

Write-Output "Répertoire sélectionné : $rep_base"

# Lancer l'analyse Python (génère resultat.json)
Write-Output "Analyse des fichiers en cours..."
python analyse_fichiers.py "$rep_base"

# Préparer la liste des fichiers candidats à la suppression
$filesToDelete = @()
$resultsFile = Join-Path -Path (Get-Location) -ChildPath 'resultat.json'

if (Test-Path $resultsFile) {
    try {
        $json = Get-Content $resultsFile -Raw | ConvertFrom-Json
        # s'attend à une liste d'éléments [chemin, taille]
        $paths = $json | ForEach-Object { $_[0] } | Where-Object { $_ -ne $null }

        if ($paths.Count -gt 0) {
            # Si Out-GridView est disponible, l'utiliser pour une sélection conviviale
            if (Get-Command Out-GridView -ErrorAction SilentlyContinue) {
                $sel = $paths | Out-GridView -Title 'Sélectionnez les fichiers à supprimer' -PassThru -OutputMode Multiple
                if ($sel) { $filesToDelete = $sel }
            }
        }
    } catch {
        Write-Output "Impossible de lire $resultsFile : $_"
    }
}

# Si aucune sélection par resultat.json (ou Out-GridView absent), ouvrir un OpenFileDialog dans le répertoire
if ($filesToDelete.Count -eq 0) {
    $ofd = New-Object System.Windows.Forms.OpenFileDialog
    $ofd.InitialDirectory = $rep_base
    $ofd.Multiselect = $true
    $ofd.Title = 'Sélectionnez les fichiers à supprimer'
    if ($ofd.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
        $filesToDelete = $ofd.FileNames
    }
}

if ($filesToDelete.Count -eq 0) {
    Write-Output "Aucun fichier sélectionné."
    exit
}

Write-Output "Fichiers sélectionnés :"
$filesToDelete | ForEach-Object { Write-Output " - $_" }

# Demande de confirmation explicite
$confirmation = Read-Host "Confirmez-vous la suppression de ces fichiers ? Tapez OUI pour confirmer"
if ($confirmation -ne 'OUI') {
    Write-Output "Suppression annulée par l'utilisateur."
    exit
}

# Suppression des fichiers sélectionnés
$success = @()
$failed = @()

foreach ($f in $filesToDelete) {
    try {
        if (Test-Path $f) {
            Remove-Item -LiteralPath $f -Force -ErrorAction Stop
            $success += $f
        } else {
            $failed += "$f : fichier introuvable"
        }
    } catch {
        $failed += "$f : $_"
    }
}

Write-Output "Suppression terminée. Réussis: $($success.Count). Échecs: $($failed.Count)"
if ($success.Count -gt 0) { $success | ForEach-Object { Write-Output "Supprimé: $_" } }
if ($failed.Count -gt 0) { $failed | ForEach-Object { Write-Output "Échec: $_" } }

# Optionnel : relancer l'affichage graphique pour rafraîchir l'interface
Write-Output "Relance de l'affichage des résultats..."
python affichage_resultats.py
