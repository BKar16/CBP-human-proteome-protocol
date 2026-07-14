# Computational Protocol for Identifying Human Cytokinin-Binding Proteins (CBPs)

Companion repository for:

> Naseem M, Kar B, Kohail S, Wilson K, Lafi FF, Akash A, Iqbal M, Muhammad K, Mehmood R, Bencurova E, Othman EM, Dandekar T.
> **A Computational Perspective on Identifying Cytokinin-Binding Proteins in Human Proteome.**
> *Briefings in Bioinformatics* (submitted).

This repository contains the scripts, input files, and result tables needed to reproduce the six illustrative validation examples described in the manuscript and its Supplementary Material ("Demonstration of our Problem-Solving Protocol applied to Cytokinin Binding Proteins"). It is provided so that reviewers and readers can inspect and rerun the computational protocol underlying the illustrative applications.

## Scope

This is a **methods/protocol demonstration repository**, not a distributable software package. The manuscript is a perspective/protocol article that benchmarks and chains together several existing, independently published tools (SwissTargetPrediction, TargetNet, ProBiS, PharmMapper, AutoDock Vina, STITCH) around a shared ligand (kinetin) and a small set of control proteins. What is original here is the **pipeline, the parameter choices, and the input/output files** used to generate the results reported in Table 1 (manuscript) and Tables 1–3 (supplement), not the underlying third-party tools themselves.

## Study design (summary)

Four-stage tiered screen, converging on candidate cytokinin-binding proteins (CBPs) in the human proteome, using kinetin as the probe ligand:

1. **Broad ligand-based similarity screening** — SwissTargetPrediction, TargetNet
2. **Structure- and pharmacophore-based filtering** — ProBiS, PharmMapper
3. **High-accuracy molecular docking** — AutoDock Vina
4. **Network-based inference** — STITCH

### Ligand
- Kinetin (N6-furfuryladenine), PubChem CID 3830
- SMILES: `C1=COC(=C1)CNC2=NC=NC3=C2NC=N3`

### Controls used throughout
| Role | Protein | Structure | UniProt |
|---|---|---|---|
| Positive control | AHK4/CRE1 cytokinin receptor, sensor (CHASE) domain | PDB 3T4S | — |
| Test protein | Adenine phosphoribosyltransferase (APRT) | PDB 6HGP | P07741 |
| Negative control | DinB DNA polymerase (Pol IV) | *PDB ID to be confirmed — see `data/receptors/README.md`* | Q02886 |

## Repository layout

```
CBP-human-proteome-protocol/
├── README.md                  # this file
├── LICENSE                    # CC-BY 4.0 (matches BiB open-access license)
├── data/
│   ├── ligands/                # kinetin structure files
│   ├── receptors/               # receptor PDB IDs / retrieval notes
│   └── controls/                # positive/negative control definitions (JSON)
├── scripts/
│   ├── 01_prepare_ligand.sh     # SMILES -> 3D -> PDBQT (Open Babel)
│   ├── 02_prepare_receptor.sh   # fetch PDB, strip waters/heteroatoms, add polar H, -> PDBQT
│   ├── 03_run_vina_docking.sh   # runs the 3 AutoDock Vina jobs (APRT, AHK4/CRE1, DinB)
│   ├── vina_configs/             # one Vina config file per target (grid box center/size)
│   └── 04_query_stitch.py       # programmatic STITCH chemical-protein interaction query
├── results/
│   ├── table1_swisstargetprediction.csv
│   ├── table2_targetnet.csv
│   ├── table3_probis.csv
│   ├── pharmmapper_top_hits.csv
│   ├── docking_summary.csv
│   └── stitch_kinetin_targets.csv
└── docs/
    └── methods_full_text.md     # verbatim methods section copied from the Supplementary Material
```

## Reproducing the docking results (Section 2.5 of the Supplement)

```bash
bash scripts/01_prepare_ligand.sh
bash scripts/02_prepare_receptor.sh 6HGP     # APRT
bash scripts/02_prepare_receptor.sh 3T4S     # AHK4/CRE1 sensor domain
bash scripts/03_run_vina_docking.sh
```

Expected output (see `results/docking_summary.csv` and Supplement Section 2.5 / Fig. "Docking interaction between kinetin and AHK4"):

| Target | PDB | Grid box center (Å) | Box size (Å) | Binding energy (kcal/mol) |
|---|---|---|---|---|
| AHK4/CRE1 (positive control) | 3T4S | 5, 23, 27 | 20×20×20 | −7.6 |
| APRT (test protein) | 6HGP | −27, 2, 10 | 20×20×20 | −6.8 |
| DinB (negative control) | *see note above* | 5, −6, −19 | 20×20×20 | −5.4 |

## Web-server-based steps (not scriptable, documented for transparency)

SwissTargetPrediction, TargetNet, PharmMapper, and STITCH were run through their public web servers rather than local software. Where the server preserves a permanent job/record, the identifier is given so the run can be retrieved or repeated:

- **PharmMapper** job ID: `260619064905`
- **STITCH** query: kinetin, organism = *Homo sapiens*, confidence threshold medium (≥0.4) / high (≥0.7)
- **SwissTargetPrediction / TargetNet**: query ligand = kinetin SMILES above (PubChem CID 3830); TargetNet fingerprint = ECFP4, AUC threshold > 7

Full narrative methods for each tool are reproduced in `docs/methods_full_text.md` (copied verbatim from the Supplementary Material so reviewers do not need to cross-reference the manuscript).

## Notes for reviewers

- All raw docking log files produced by `03_run_vina_docking.sh` will be written to `results/vina_logs/` (git-ignored by default; remove from `.gitignore` if you want them version-controlled).
- Software versions used: AutoDock Vina 1.2.x, Open Babel 3.x, Python 3.10+.
- This repository accompanies the manuscript under single-anonymized review at *Briefings in Bioinformatics*; author identity is intentionally not hidden here per the journal's peer-review policy.

## Citation

If you reuse these scripts or data, please cite the manuscript above. A `CITATION.cff` is included for automated citation tools.

## License

Scripts and data are released under CC-BY 4.0 unless otherwise noted (see `LICENSE`).
