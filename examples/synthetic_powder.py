"""Deterministic *toy* powder-XRD pattern, independent of local ASE databases.

Geometric simple-cubic Bragg positions and Gaussian display peaks only.
This is NOT a structure-factor, line-profile, or trained-ML model.
"""
import argparse
import csv
from math import asin, degrees, exp, isfinite, log, sqrt
from pathlib import Path


def peak_positions(lattice_a=4.0, wavelength=1.5406, max_index=3):
    """Return unique (2theta degrees, multiplicity-like count) for cubic hkl.

    Lattice constants and wavelength are in angstroms. Counts are only the
    number of enumerated nonnegative hkl triplets sharing the same h²+k²+l².
    They are NOT physical reflection intensities or crystallographic multiplicities.
    """
    if not all(isfinite(x) and x > 0 for x in (lattice_a, wavelength)):
        raise ValueError("lattice_a and wavelength must be positive finite numbers")
    if not isinstance(max_index, int) or max_index < 1:
        raise ValueError("max_index must be a positive integer")
    shells = {}
    for h in range(max_index + 1):
        for k in range(max_index + 1):
            for l in range(max_index + 1):
                n = h*h + k*k + l*l
                if not n:
                    continue
                sine = wavelength * sqrt(n) / (2 * lattice_a)
                if sine >= 1:
                    continue
                shells[n] = shells.get(n, 0) + 1
    return [(2 * degrees(asin(wavelength * sqrt(n) / (2 * lattice_a))), count)
            for n, count in sorted(shells.items())]


def synthetic_pattern(*, lattice_a=4.0, wavelength=1.5406, fwhm=0.2,
                      two_theta_min=10.0, two_theta_max=80.0, step=0.05):
    """Return angle and dimensionless intensity arrays, no instrument model."""
    if not all(isfinite(x) for x in (fwhm, two_theta_min, two_theta_max, step)):
        raise ValueError("scan parameters must be finite")
    if fwhm <= 0 or step <= 0 or not 0 <= two_theta_min < two_theta_max <= 180:
        raise ValueError("invalid scan limits, step or FWHM")
    if (two_theta_max-two_theta_min)/step > 200_000:
        raise ValueError("scan exceeds maximum of 200000 intervals")
    peaks = peak_positions(lattice_a, wavelength)
    sigma = fwhm / (2 * sqrt(2 * log(2)))
    length = int((two_theta_max - two_theta_min) / step) + 1
    angles = [two_theta_min + i * step for i in range(length)]
    intensities = [sum(exp(-0.5 * ((angle - center)/sigma)**2) for center, _ in peaks)
                   for angle in angles]
    return angles, intensities


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--a", type=float, default=4.0, help="cubic lattice spacing in angstrom")
    parser.add_argument("--wavelength", type=float, default=1.5406, help="angstrom")
    parser.add_argument("--output", type=Path, default=Path("synthetic_xrd.csv"))
    args = parser.parse_args()
    angles, intensities = synthetic_pattern(lattice_a=args.a, wavelength=args.wavelength)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["two_theta_deg", "relative_intensity"])
        writer.writerows(zip(angles, intensities))
    print(f"Wrote {len(angles)} points to {args.output}")


if __name__ == "__main__":
    main()
