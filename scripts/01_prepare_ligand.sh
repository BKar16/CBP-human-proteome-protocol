#!/usr/bin/env bash
# Prepare kinetin for AutoDock Vina docking.
# Requires: Open Babel (https://openbabel.org)
set -euo pipefail

IN_SMI="../data/ligands/kinetin.smi"
OUT_3D="../data/ligands/kinetin_3d.sdf"
OUT_PDBQT="../data/ligands/kinetin.pdbqt"

echo "[1/2] Generating 3D conformer from SMILES..."
obabel "${IN_SMI}" -O "${OUT_3D}" --gen3d

echo "[2/2] Converting to PDBQT (adds Gasteiger charges, merges nonpolar H)..."
obabel "${OUT_3D}" -O "${OUT_PDBQT}" --partialcharge gasteiger -h

echo "Done: ${OUT_PDBQT}"
