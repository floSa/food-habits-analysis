#!/usr/bin/env bash
# Régénère, depuis les sources jupytext (.md), les notebooks exécutés (.ipynb)
# et les rapports sans code (reports/*.md + images).
#
# Source de vérité = les .md de ce dossier. On ne modifie jamais les .ipynb à la main.
#
#   bash notebooks/build.sh            # tout régénérer
#   bash notebooks/build.sh 03_sociologie_acm   # un seul notebook
set -euo pipefail
cd "$(dirname "$0")/.."

PY=.venv/bin
NB=(01_population 02_habitudes 03_sociologie_acm 04_croyances_pratiques 05_marketing_choix)
[ "$#" -gt 0 ] && NB=("$@")

for n in "${NB[@]}"; do
  echo "==> $n"
  "$PY/jupytext" --to ipynb --output "notebooks/$n.ipynb" "notebooks/$n.md"
  "$PY/jupyter" nbconvert --to notebook --execute --inplace \
      --ExecutePreprocessor.timeout=300 "notebooks/$n.ipynb"
  "$PY/jupyter" nbconvert --to markdown --no-input \
      --output-dir reports --output "$n" "notebooks/$n.ipynb"
done
echo "OK — notebooks exécutés + rapports régénérés dans reports/"
