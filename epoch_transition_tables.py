# JCRIN–Vortex Dual-Gate Framework
# Status of spline modulation S[|ψ|²](t)(x_n + y_n) 
# and redshift damping f_damp(z) = e^{-z/5.8}

import pandas as pd

data = [
    {"Epoch / Transition": "Planck / earliest universe",
     "Approximate Redshift z": "≫ 10³²",
     "Approximate Cosmic Time": "≪ 10⁻⁴³ s",
     "JCRIN Spline Modulation": "Highly active / unconstrained",
     "Redshift Damping f_damp(z)": "≈ 0 (total suppression)",
     "Physical Regime & Gate Status": "Quantum gravity regime; both gates formally suppress macroscopic effects"},
    
    {"Epoch / Transition": "Inflation / Reheating",
     "Approximate Redshift z": "∼ 10²⁵ – 10²⁸",
     "Approximate Cosmic Time": "∼ 10⁻³⁶ – 10⁻³² s",
     "JCRIN Spline Modulation": "Rapidly evolving",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "Standard inflationary dynamics protected"},
    
    {"Epoch / Transition": "Deep Radiation Era",
     "Approximate Redshift z": "10¹⁰ – 10⁷",
     "Approximate Cosmic Time": "seconds – years",
     "JCRIN Spline Modulation": "Can be enhanced (source of potential distortions)",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "Strong dual suppression of late-time effects"},
    
    {"Epoch / Transition": "Thermalization Epoch",
     "Approximate Redshift z": "≈ 2 × 10⁶",
     "Approximate Cosmic Time": "∼ months – years",
     "JCRIN Spline Modulation": "Rapidly approaches classical limit (→ 1)",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "Critical JCRIN gate closes; residual energy thermalized or erased"},
    
    {"Epoch / Transition": "Neutrino decoupling / e⁺e⁻ annihilation",
     "Approximate Redshift z": "∼ 10⁹ – 10⁸",
     "Approximate Cosmic Time": "seconds – minutes",
     "JCRIN Spline Modulation": "Near classical",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "Standard BBN physics fully protected"},
    
    {"Epoch / Transition": "Big Bang Nucleosynthesis (BBN)",
     "Approximate Redshift z": "∼ 10⁹ – 10⁸",
     "Approximate Cosmic Time": "∼ 1 – 200 s",
     "JCRIN Spline Modulation": "Classical (≈ 1)",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "Light-element abundances unaffected"},
    
    {"Epoch / Transition": "Matter–Radiation Equality",
     "Approximate Redshift z": "≈ 3400",
     "Approximate Cosmic Time": "∼ 50 000 yr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "Standard growth of perturbations begins"},
    
    {"Epoch / Transition": "Recombination / CMB Last Scattering",
     "Approximate Redshift z": "≈ 1090",
     "Approximate Cosmic Time": "≈ 380 000 yr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "≈ 0",
     "Physical Regime & Gate Status": "CMB blackbody fidelity fully protected"},
    
    {"Epoch / Transition": "Dark Ages",
     "Approximate Redshift z": "1100 → ∼ 30",
     "Approximate Cosmic Time": "380 kyr – ∼100 Myr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "Extremely small",
     "Physical Regime & Gate Status": "No coherent vortex torque"},
    
    {"Epoch / Transition": "First stars / Reionization begins",
     "Approximate Redshift z": "∼ 15 – 10",
     "Approximate Cosmic Time": "∼200 – 500 Myr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "∼ 0.03 – 0.18",
     "Physical Regime & Gate Status": "Weak residual damping"},
    
    {"Epoch / Transition": "Reionization / First Galaxies",
     "Approximate Redshift z": "∼ 6 – 10",
     "Approximate Cosmic Time": "∼500 Myr – 1 Gyr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "∼ 0.18 – 0.37",
     "Physical Regime & Gate Status": "Transition window opens"},
    
    {"Epoch / Transition": "Maturation Transition (τ = 5.8)",
     "Approximate Redshift z": "5.8",
     "Approximate Cosmic Time": "≈ 0.97 Gyr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "= 1/e ≈ 0.368",
     "Physical Regime & Gate Status": "Critical damping gate: coherent coupling efficiency reaches 1/e"},
    
    {"Epoch / Transition": "Post-maturation (structure formation)",
     "Approximate Redshift z": "5.8 → 1",
     "Approximate Cosmic Time": "1 – 6 Gyr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "0.37 → 0.84",
     "Physical Regime & Gate Status": "Gradual unlocking of vortex torque"},
    
    {"Epoch / Transition": "Matter–Dark Energy Equality",
     "Approximate Redshift z": "≈ 0.3",
     "Approximate Cosmic Time": "≈ 10.3 Gyr",
     "JCRIN Spline Modulation": "Classical",
     "Redshift Damping f_damp(z)": "≈ 0.95",
     "Physical Regime & Gate Status": "Near-full coupling"},
    
    {"Epoch / Transition": "Present Day",
     "Approximate Redshift z": "0",
     "Approximate Cosmic Time": "13.79 Gyr",
     "JCRIN Spline Modulation": "Classical (= 1)",
     "Redshift Damping f_damp(z)": "= 1",
     "Physical Regime & Gate Status": "Full vortex torque active (+3.17 km s⁻¹ Mpc⁻¹); local H₀ ≈ 73.17"}
]

df = pd.DataFrame(data)
print(df.to_string(index=False))
