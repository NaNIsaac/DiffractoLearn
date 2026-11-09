# Minimal reproducible powder-XRD example

A runnable **synthetic** baseline without the private `binxrd.db` database,
GPU, ASE, PyTorch, or trained network.

```sh
python examples/synthetic_powder.py --output synthetic_xrd.csv
python -m unittest discover -s tests -v
```

CSV columns are `two_theta_deg` and `relative_intensity`.
Use any plotting program to view the scan; data are deterministic.

## What is calculated

- A cubic cell of lattice constant `a = 4.0 Å` by default.
- Plane spacings `d_hkl = a / sqrt(h²+k²+l²)`.
- Bragg positions `2θ = 2 asin(λ / 2d_hkl)` for permitted geometric positions.
- A Gaussian peak at each unique position for **visualization only**.
- Unit peak amplitudes (not structure factors); the returned counts in `peak_positions`
  only count enumerated nonnegative integer index triplets, **not** physical intensities.

## What is not calculated

No structure factors, extinction rules, anomalous scattering, Debye–Waller
factors, crystallographic multiplicities, instrumental broadening, texture,
background, noise, phase fractions, or learned classification.

This example only establishes an independently reproducible input/output format
and a basic Bragg-law test. It must **not** be used to claim phase classification
or quantitative refinement performance.
