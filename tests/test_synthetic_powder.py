"""Offline smoke tests for the deterministic XRD example."""

import importlib.util
import math
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "examples" / "synthetic_powder.py"
spec = importlib.util.spec_from_file_location("synthetic_powder", FILE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SyntheticPatternTests(unittest.TestCase):
    def test_first_simple_cubic_peak_matches_bragg_law(self):
        peaks = module.peak_positions(4.0, 1.5406)
        first = 2 * math.degrees(math.asin(1.5406 / 8))
        self.assertAlmostEqual(peaks[0][0], first, places=10)

    def test_peak_shifts_to_lower_angles_for_larger_lattice(self):
        a = module.peak_positions(4.0)[0][0]
        b = module.peak_positions(5.0)[0][0]
        self.assertLess(b, a)

    def test_generated_pattern_is_finite_and_deterministic(self):
        x1, y1 = module.synthetic_pattern()
        x2, y2 = module.synthetic_pattern()
        self.assertEqual((x1, y1), (x2, y2))
        self.assertEqual(len(x1), len(y1))
        self.assertTrue(all(math.isfinite(v) and v >= 0 for v in y1))

    def test_parameter_validation(self):
        invalid = [
            {"lattice_a": 0},
            {"wavelength": float("nan")},
            {"fwhm": 0},
            {"step": -1},
            {"two_theta_min": 90, "two_theta_max": 80},
        ]
        for args in invalid:
            with self.subTest(args=args), self.assertRaises(ValueError):
                module.synthetic_pattern(**args)


if __name__ == "__main__":
    unittest.main()
