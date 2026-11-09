# DiffractoLearn

An early-stage project for machine learning on powder X-ray diffraction (XRD) patterns, with crystal-phase identification and phase-fraction estimation as longer-term goals. What the repository currently contains (2026-11-09):

- `main.py` and `scripts/main.py`: placeholder entry points that only print a greeting.
- `examples/synthetic_powder.py`: runnable standard-library geometric powder-XRD toy baseline, with offline tests; no private database required.
- `notebooks/test.ipynb`: one cell that reads a local ASE database `binxrd.db` (not in the repository) and, per structure, its element list, lattice spacings, peak intensities, space group and crystal system: a powder X-ray diffraction dataset.
- `pyproject.toml`: dependencies for planned machine-learning work (PyTorch from the CUDA 12.6 index, scikit-learn, ase, refnx, hydra-core, mlcroissant) and no package code yet.

X-ray reflectivity (XRR) fitting is out of scope and is developed separately in [ReflectoLearn](https://github.com/NaNIsaac/ReflectoLearn). The current notebook is exploratory; there is not yet a trained powder-XRD classifier or phase-fraction predictor.

## Reproducible baseline (no external data)

```sh
python examples/synthetic_powder.py --output synthetic_xrd.csv
python -m unittest discover -s tests -v
```

The example writes a deterministic synthetic CSV of simple-cubic Bragg peak positions with Gaussian display peaks. It is **not** a physical diffraction-intensity calculation, phase classifier or phase-fraction estimator. See [assumptions and limitations](docs/synthetic-baseline.md).

## Current versus planned workflow

![The project currently parses an externally supplied diffraction database; training and phase quantification are goals, not shipped features.](docs/media/readme-overview.svg)

The project currently parses an externally supplied diffraction database; training and phase quantification are goals, not shipped features.

To understand the present code, open `notebooks/test.ipynb`; it expects a local `binxrd.db`. The model block in this figure is deliberately **planned**, not an implemented pipeline.

## The notebook's data format

`notebooks/test.ipynb` expects `binxrd.db` in the working directory, an [ASE database](https://wiki.fysik.dtu.dk/ase/ase/db/db.html) with one row per crystal structure and three string-valued key-value pairs per row:

| key | content after parsing |
| --- | --- |
| `latt_dis` | list of lattice spacings |
| `intensity` | list of peak intensities |
| `tager` | `(space group number, crystal system)` |

The strings are parsed with `ast.literal_eval`, which accepts Python literals only. An earlier revision used `eval`, which runs any expression stored in a database field; a database from an untrusted source could execute code on the reader's machine. `literal_eval` raises `ValueError` on such a field instead. The database itself is not in the repository, so the notebook has not been run on the real data; it was checked against a synthetic one-row database and a row carrying a hostile expression.
