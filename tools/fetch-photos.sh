#!/usr/bin/env bash
# Récupère les photos de chantier du site actuel (its-entreprise.com) dans
# photos-src/, puis lance la génération des images optimisées.
#
# Usage : bash tools/fetch-photos.sh
#
# L'environnement de génération de la maquette n'avait pas accès à
# its-entreprise.com : complétez les URL ci-dessous avec celles des photos
# choisies (clic droit > « Copier l'adresse de l'image » sur le site actuel),
# en respectant les noms de fichiers attendus par tools/build-images.py.
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p photos-src

declare -A PHOTOS=(
  [hero-chantier]="https://www.its-entreprise.com/wp-content/uploads/A-COMPLETER.jpg"
  [parc-des-princes]="https://www.its-entreprise.com/wp-content/uploads/A-COMPLETER.jpg"
  [parking-lorilleux]="https://www.its-entreprise.com/wp-content/uploads/A-COMPLETER.jpg"
  [centre-commercial]="https://www.its-entreprise.com/wp-content/uploads/A-COMPLETER.jpg"
  [equipe-chantier]="https://www.its-entreprise.com/wp-content/uploads/A-COMPLETER.jpg"
)

for name in "${!PHOTOS[@]}"; do
  url="${PHOTOS[$name]}"
  if [[ "$url" == *A-COMPLETER* ]]; then
    echo "⚠  $name : URL à compléter dans tools/fetch-photos.sh"
    continue
  fi
  echo "↓  $name"
  curl -fsSL -A "Mozilla/5.0" "$url" -o "photos-src/$name.jpg"
done

python3 tools/build-images.py
