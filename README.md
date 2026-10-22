# DiffractoLearn

An early-stage repository. What it holds now (2026-10-23):

- `main.py` and `scripts/main.py`: placeholder entry points that only print a greeting.
- `notebooks/test.ipynb`: one cell that reads a local ASE database `binxrd.db` (not in the repository) and, per structure, its element list, lattice spacings, peak intensities, space group and crystal system: a powder X-ray diffraction dataset.
- `pyproject.toml`: dependencies for planned machine-learning work (PyTorch from the CUDA 12.6 index, scikit-learn, ase, refnx, hydra-core, mlcroissant) and no package code yet.

The GitHub description and `pyproject.toml` say "Machine learning tools for X-ray reflectivity analysis", while the only data code here reads powder diffraction data and the reflectivity work lives in [ReflectoLearn](https://github.com/NaNIsaac/ReflectoLearn). Which of the two this repository is for is not stated anywhere in it.
