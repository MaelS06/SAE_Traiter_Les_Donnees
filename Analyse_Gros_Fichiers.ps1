Write-Output "==============================================="
Write-Output " SAE 1.05 - Analyse des gros fichiers"
Write-Output "==============================================="
Write-Output ""

# -----------------------------------------------
# Configuration
# -----------------------------------------------
$pythonCandidates = @("python", "python3")
$python = $null
foreach ($p in $pythonCandidates) {
    try {
        $ver = & $p --version 2>&1
        if ($LASTEXITCODE -eq 0 -or $ver) { $python = $p; break }
    } catch { }
}
if (-not $python) { Write-Output "Python introuvable dans le PATH."; exit }

$script_selecteur = "select_repertoire.py"
$script_analyse   = "analyse_fichiers.py"
$script_affichage = "affichage_resultats.py"
$fichier_json     = "resultats.json"

# Assurer que le script s'execute depuis son dossier (ou se trouvent les scripts Python)
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $scriptDir

# -----------------------------------------------
# Selection du repertoire
# -----------------------------------------------
Write-Output "Selection du repertoire a analyser..."
# Exécute le sélecteur et capture sa sortie (chemin) et d'evenuelles erreurs
$selectOutput = & $python $script_selecteur 2>&1
$selectExit = $LASTEXITCODE
if ($selectExit -ne 0) {
    Write-Output "Le selecteur a echoue (code $selectExit). Sortie :"
    Write-Output $selectOutput
    exit
}

$rep_base = $selectOutput -split "`n" | Select-Object -Last 1
$rep_base = $rep_base.Trim()

if (-not $rep_base) {
    Write-Output "Repertoire invalide (selection vide). Fin du script."
    exit
}

if (-not (Test-Path $rep_base)) {
    Write-Output "Repertoire invalide ou inaccessible : $rep_base. Fin du script."
    exit
}

Write-Output "Repertoire selectionne : $rep_base"

# -----------------------------------------------
# Analyse de l'arborescence
# -----------------------------------------------
Write-Output ""
Write-Output "Analyse en cours..."
# Passe le repertoire de base et le nom du fichier JSON a creer, capture la sortie
$analyseOutput = & $python $script_analyse $rep_base $fichier_json 2>&1
$analyseExit = $LASTEXITCODE
if ($analyseExit -ne 0) {
    Write-Output "L'analyse a echoue (code $analyseExit). Sortie :"
    Write-Output $analyseOutput
    exit
}

if (-not (Test-Path $fichier_json)) {
    Write-Output "Le fichier JSON n'a pas ete cree : $fichier_json"
    Write-Output "Sortie du script d'analyse :"
    Write-Output $analyseOutput
    Write-Output "Contenu du dossier courant ($scriptDir) :"
    Get-ChildItem -Force | ForEach-Object { Write-Output $_.Name }
    exit
}

Write-Output "Analyse terminee"

# -----------------------------------------------
# Lancement de l'IHM
# -----------------------------------------------
Write-Output ""
Write-Output "Ouverture de l'interface graphique..."
# Passe le nom du fichier JSON au script d'affichage et capture sa sortie
$ihmOutput = & $python $script_affichage $fichier_json 2>&1
$ihmExit = $LASTEXITCODE
if ($ihmExit -ne 0) {
    Write-Output "L'IHM a retourne le code $ihmExit. Sortie :"
    Write-Output $ihmOutput
}

Write-Output ""
Write-Output "Fin du script principal."
