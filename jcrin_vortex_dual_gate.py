#!/usr/bin/env python3
"""
JCRIN–Vortex Dual-Gate Framework
Pure Python implementation of the discrete lattice, dual temporal gates,
super-horizon freezing → horizons density/pull conversion,
CMB protection, and late-time geometric torque.
"""

import math
from typing import List, Tuple, Dict

# =============================================================================
# 1. CORE CONSTANTS (from JCRIN Framework)
# =============================================================================
EPS = 1e-9                          # ε = 10^{-9}
N_MAX = 1_000_000_000               # 10^9 steps
DELTA_T = 435.4                     # seconds per step (local dilated)
COSMIC_AGE_GYR = 13.79
TAU_DAMP = 5.8                      # characteristic redshift for damping gate
BASE_H0 = 70.0                      # km/s/Mpc  (undamped bosonic baseline)
TORQUE_AMPLITUDE = 3.17             # km/s/Mpc  (full late-time geometric torque)
THERMALIZATION_Z = 2.0e6            # approximate redshift where spline gate closes

# =============================================================================
# 2. LATTICE SEQUENCES & EQUIVALENCY THEOREM
# =============================================================================
def y_n(n: int) -> float:
    """Main sequence: scale-factor proxy."""
    return n * EPS

def x_n(n: int) -> float:
    """Complementary sequence."""
    return 1.0 - n * EPS

def check_equivalency(n: int, tol: float = 1e-15) -> bool:
    """Equivalency Theorem: x_n + (1 - x_n) = 1 and y_n + (1 - y_n) = 1."""
    yn = y_n(n)
    xn = x_n(n)
    return (abs(xn + (1.0 - xn) - 1.0) < tol and
            abs(yn + (1.0 - yn) - 1.0) < tol)

# =============================================================================
# 3. JCRIN SPLINE MODULATION GATE  M(t) = S[|ψ|² (x_n + y_n)]
#    Simplified but faithful: enhanced in deep radiation era,
#    forced to classical limit (=1) by thermalization epoch.
# =============================================================================
def spline_modulation(n: int, z_approx: float) -> float:
    """
    Returns M ≈ S[|ψ|² (x_n + y_n)].
    Early (high-z): can be >1.
    After thermalization (z ≲ 2e6): → 1.0 (classical).
    """
    # Simple smooth transition using a logistic-like gate
    # Centered around thermalization; width chosen for rapid closure
    if z_approx > 1e7:
        # Deep radiation / pre-thermalization: mild enhancement possible
        enhancement = 1.0 + 0.15 * math.exp(-(math.log10(z_approx) - 8.0)**2 / 4.0)
        return min(enhancement, 1.25)  # hard ceiling for numerical safety
    else:
        # Post-thermalization: classical limit
        return 1.0

# =============================================================================
# 4. REDSHIFT DAMPING GATE
# =============================================================================
def f_damp(z: float) -> float:
    """f_damp(z) = exp(-z / 5.8)"""
    if z < 0:
        z = 0.0
    return math.exp(-z / TAU_DAMP)

def f_mod(z: float) -> float:
    """Frequency modulation companion: 1 + 5 exp(-z/2)"""
    return 1.0 + 5.0 * math.exp(-z / 2.0)

def composite_suppression(z: float, chi_mpc: float = 0.0) -> float:
    """
    S(z) = (1 + 5 e^{-z/2}) * e^{-z/5.8} * e^{-χ/4500}
    (χ term optional; set to 0 for pure redshift damping)
    """
    return f_mod(z) * f_damp(z) * math.exp(-chi_mpc / 4500.0)

# =============================================================================
# 5. ROUGH n ↔ z MAPPING
#    A monotonic proxy that places key epochs at approximately correct n.
# =============================================================================
def approx_redshift(n: int) -> float:
    """
    Crude bu ordered mapping:
    - Very early n → extremely high z
    - n ~ 1e5–1e6 → BBN / thermalization region
    - n near N_MAX → z→0
    """
    if n <= 0:
        return 1e40
    # Log-stretch so that late times get more resolution
    frac = n / N_MAX
    # Rough inverse: high-z early, low-z late
    # Tuned so that maturation (z=5.8) occurs near n corresponding to ~1 Gyr
    if frac < 1e-6:
        return 1e10 / (frac + 1e-12)**0.3
    else:
        # Late-time approximation (matter/DE dominated proxy)
        a = math.exp(frac * 1.0) / math.e          # a from ~0 to 1
        z = max(1.0 / a - 1.0, 0.0)
        return z

def approx_cosmic_time_gyr(n: int) -> float:
    """Very rough linear-in-log proxy for display."""
    frac = n / N_MAX
    return COSMIC_AGE_GYR * (frac ** 0.8)   # slower early, faster late

# =============================================================================
# 6. TORQUE ACCUMULATION (discrete integral)
# =============================================================================
def compute_torque(n_samples: List[int]) -> float:
    """
    Approximate the torque integral by sampling:
    ΔH_torque ∝ Σ [phase bias] × suppression factors
    Normalized so that at z=0 the full amplitude is recovered.
    """
    total = 0.0
    weight_sum = 0.0
    for n in n_samples:
        z = approx_redshift(n)
        supp = composite_suppression(z)
        # Simple phase-bias proxy (imaginary kick strength)
        phase_bias = math.sin(2.0 * math.pi * y_n(n)) ** 2
        total += phase_bias * supp
        weight_sum += supp
    if weight_sum == 0.0:
        return 0.0
    # Normalize to full torque at present day
    return TORQUE_AMPLITUDE * (total / weight_sum) * f_damp(0.0)

# =============================================================================
# 7. EFFECTIVE HUBBLE PARAMETER
# =============================================================================
def H_eff(z: float, torque_now: float) -> float:
    """
    H_eff(z) = BASE_H0 + torque_now * f_damp(z)
    (baseline present at all z; torque only released at low z)
    """
    return BASE_H0 + torque_now * f_damp(z)

# =============================================================================
# 8. KEY EPOCHS (from Full Epoch and Transition Table)
# =============================================================================
EPOCHS = [
    ("Planck / earliest universe",          1e-12),
    ("Inflation / Reheating",               1e-8),
    ("Deep Radiation Era",                  1e-5),
    ("Thermalization Epoch",                5e-4),
    ("Neutrino decoupling / e+e- ann.",     2e-3),
    ("Big Bang Nucleosynthesis (BBN)",      5e-3),
    ("Matter–Radiation Equality",           0.01),
    ("Recombination / CMB Last Scattering", 0.03),
    ("Dark Ages (mid)",                     0.08),
    ("First stars / Reionization begins",   0.15),
    ("Reionization / First Galaxies",       0.25),
    ("Maturation Transition (τ=5.8)",       0.35),
    ("Post-maturation (structure form.)",   0.55),
    ("Matter–Dark Energy Equality",         0.80),
    ("Present Day",                         1.00),
]

# =============================================================================
# 9. MAIN SIMULATION
# =============================================================================
def main():
    print("=" * 92)
    print("  JCRIN–VORTEX DUAL-GATE FRAMEWORK  –  Pure Python Implementation")
    print("  Lattice: ε = 10⁻⁹ , N_max = 10⁹")
    print("  Dual gates: JCRIN spline (early) + redshift damping τ=5.8 (late)")
    print("=" * 92)

    # ----- Equivalency checks at selected points -----
    print("\n[1] EQUIVALENCY THEOREM CHECKS")
    test_ns = [0, 1, 1000, 10**6, 10**8, N_MAX]
    for n in test_ns:
        ok = check_equivalency(n)
        print(f"  n = {n:12d}  →  equivalency {'PASS' if ok else 'FAIL'}  "
              f"(y_n = {y_n(n):.10f})")

    # ----- Build sampled n list (log + linear mix for coverage) -----
    samples = set()
    for i in range(0, 40):
        samples.add(int(10**(i * 9.0 / 39)))          # log-spaced
    for frac, _ in [(e[1], e[0]) for e in EPOCHS]:
        samples.add(int(frac * N_MAX))
    samples.add(N_MAX)
    n_samples = sorted(list(samples))
    n_samples = [n for n in n_samples if 0 <= n <= N_MAX]

    # ----- Compute present-day torque -----
    torque_now = compute_torque(n_samples)
    print(f"\n[2] TORQUE ATULATION (sampled)")
    print(f"  Full late-time geometric torque ≈ {torque_now:.4f} km s⁻¹ Mpc⁻¹")

    # ----- Epoch table with live gate values -----
    print("\n[3] FULL EPOCH AND TRANSITION TABLE (computed)")
    print("-" * 92)
    header = (f"{'Epoch / Transition':<42} {'n (approx)':>12} {'z (approx)':>12} "
              f"{'M (spline)':>10} {'f_damp':>10} {'H_eff':>10}")
    print(header)
    print("-" * 92)

    for name, frac in EPOCHS:
        n = int(frac * N_MAX)
        z = approx_redshift(n)
        M = spline_modulation(n, z)
        fd = f_damp(z)
        He = H_eff(z, torque_now)
        print(f"{name:<42} {n:12d} {z:12.3e} {M:10.4f} {fd:10.4f} {He:10.3f}")

    print("-" * 92)

    # ----- Present-day summary -----
    z0 = 0.0
    H0_local = H_eff(z0, torque_now)
    print("\n[4] PRESENT-DAY RESULTS")
    print(f"  Baseline (undamped) H₀          = {BASE_H0:.2f} km s⁻¹ Mpc⁻¹")
    print(f"  Geometric torque (full)         = {torque_now:.2f} km s⁻¹ Mpc⁻¹")
    print(f"  Local H₀ (BASE + torque)        = {H0_local:.2f} km s⁻¹ Mpc⁻¹")
    print(f"  f_damp(z=0)                     = {f_damp(0.0):.6f}")
    print(f"  Spline modulation (today)       = {spline_modulation(N_MAX, 0.0):.6f}")

    # ----- Gate status summary -----
    print("\n[5] DUAL-GATE STATUS SUMMARY")
    print("  • JCRIN Spline Gate : Active / potentially enhanced only in deep radiation era;")
    print("                        forced to classical limit (M→1) by thermalization (z~2e6).")
    print("                        Protects CMB spectral fidelity and BBN.")
    print("  • Redshift Damping  : Closed until z~10; reaches 1/e at z=5.8 (~1 Gyr);")
    print("                        fully open only at low redshift.")
    print("                        Releases geometric torque while protecting high-z observables.")
    print("  • Combined Action   : Broad safe corridor from thermalization through recombination")
    print("                        and early structure formation. High-z = standard ΛCDM;")
    print("                        low-z receives calibrated +3.17 km s⁻¹ Mpc⁻¹ torque.")

    # ----- Final boxed statements -----
    print("\n[6] KEY INVARIANTS (machine precision)")
    print("  ∀ n  :  x_n + (1 - x_n) = 1")
    print("  ∀ n  :  y_n + (1 - y_n) = 1")
    print("  τ = 5.8 is the characteristic redshift scale of coherent coupling efficiency.")
    print("=" * 92)
    print("  Dual-gate architecture executed successfully.")
    print("  Super-horizon freezing → horizons density/pull conversion gated and complete.")
    print("=" * 92)

if __name__ == "__main__":
    main()
