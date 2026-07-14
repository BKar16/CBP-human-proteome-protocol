#!/usr/bin/env bash
# Fetch a receptor PDB, strip waters/heteroatoms/original ligand, add polar
# hydrogens, and convert to PDBQT for AutoDock Vina.
#
# Usage: ./02_prepare_receptor.sh <PDB_ID>
# Example: ./02_prepare_receptor.sh 6HGP
#
# Requires: curl, Open Babel (https://openbabel.org)
set -euo pipefail

PDB_ID="${1:?Usage: 02_prepare_receptor.sh <PDB_ID>}"
OUT_DIR="../data/receptors"
mkdir -p "${OUT_DIR}"

RAW_PDB="${OUT_DIR}/${PDB_ID}.pdb"
CLEAN_PDB="${OUT_DIR}/${PDB_ID}_clean.pdb"
OUT_PDBQT="${OUT_DIR}/${PDB_ID}.pdbqt"

echo "[1/3] Downloading ${PDB_ID} from RCSB PDB..."
curl -sSL "https://files.rcsb.org/download/${PDB_ID}.pdb" -o "${RAW_PDB}"

echo "[2/3] Stripping waters (HOH) and heteroatoms (HETATM), keeping protein only..."
grep -E '^(ATOM|TER|END)' "${RAW_PDB}" > "${CLEAN_PDB}"

echo "[3/3] Adding polar hydrogens and converting to PDBQT..."
obabel "${CLEAN_PDB}" -O "${OUT_PDBQT}" -xr --partialcharge gasteiger -h

echo "Done: ${OUT_PDBQT}"
echo "NOTE: inspect ${CLEAN_PDB} manually if the structure contains multiple chains/altlocs."
