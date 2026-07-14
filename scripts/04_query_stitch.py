#!/usr/bin/env python3
"""
Query the STITCH database (http://stitch.embl.de) for kinetin's predicted and
known chemical-protein interactions in Homo sapiens, as described in
Supplement Section 2.6.

STITCH provides a public API mirroring the STRING API. This script resolves
the compound identifier for kinetin, retrieves its interaction network for
Homo sapiens, and filters by confidence score (medium >= 0.4, high >= 0.7).

Requires: requests (`pip install requests`)
"""
import csv
import sys
import requests

STITCH_API = "http://stitch.embl.de/api"
SPECIES_HUMAN = 9606
COMPOUND_NAME = "kinetin"
CONFIDENCE_THRESHOLDS = {"medium": 0.4, "high": 0.7}


def resolve_compound(name: str, species: int = SPECIES_HUMAN):
    """Resolve a free-text compound name to a STITCH/STRING identifier."""
    resp = requests.get(
        f"{STITCH_API}/tsv/get_string_ids",
        params={"identifiers": name, "species": species},
        timeout=30,
    )
    resp.raise_for_status()
    lines = [l for l in resp.text.splitlines() if l]
    if len(lines) < 2:
        raise RuntimeError(f"Could not resolve compound identifier for '{name}'")
    header, first_hit = lines[0].split("\t"), lines[1].split("\t")
    return dict(zip(header, first_hit))


def get_interaction_partners(stitch_id: str, species: int = SPECIES_HUMAN, limit: int = 50):
    resp = requests.get(
        f"{STITCH_API}/tsv/interaction_partners",
        params={"identifiers": stitch_id, "species": species, "limit": limit},
        timeout=30,
    )
    resp.raise_for_status()
    lines = resp.text.splitlines()
    header = lines[0].split("\t")
    rows = [dict(zip(header, l.split("\t"))) for l in lines[1:] if l]
    return rows


def main(out_csv="../results/stitch_kinetin_targets.csv"):
    compound = resolve_compound(COMPOUND_NAME)
    stitch_id = compound.get("stringId") or compound.get("queryItem")
    partners = get_interaction_partners(stitch_id)

    filtered = [
        p for p in partners
        if float(p.get("score", 0)) / 1000.0 >= CONFIDENCE_THRESHOLDS["medium"]
    ]

    with open(out_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(filtered[0].keys()) if filtered else [])
        writer.writeheader()
        writer.writerows(filtered)

    print(f"Wrote {len(filtered)} kinetin-associated proteins (score >= 0.4) to {out_csv}")


if __name__ == "__main__":
    main(*sys.argv[1:])
