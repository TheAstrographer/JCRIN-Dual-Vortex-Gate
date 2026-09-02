# ==============================================================================
# Cobaya Configuration – JCRIN Dual-Vortex-Gate + Multi-Probe Likelihoods
# ==============================================================================

likelihood:
  planck_2018_highl_plik.TTTEEE:
  planck_2018_lowl.TT:
  planck_2018_lowl.EE:
  planck_2018_lensing.baseline:
  desi_2024_dr1_bao.main:          # replace with official DR2 when available
  pantheon_plus.binned:
  des_y6.3x2pt:
  kids_legacy.cosmic_shear:

theory:
  camb:
    # path to a CAMB installation that includes the Dual-Gate background patch
    # (see implementation note below)
    stop_at_error: false
    extra_args:
      lens_potential_accuracy: 2
      AccuracyBoost: 1.5
      lSampleBoost: 1.5
      lAccuracyBoost: 1.5
      halofit_version: mead2020
      # Dual-Gate flags (passed to the modified CAMB)
      jcrin_base_H0: 70.0
      jcrin_torque: 3.17
      jcrin_tau: 5.8

params:
  # Standard six parameters (early-universe sector identical to ΛCDM)
  ombh2:
    prior: {min: 0.005, max: 0.1}
    ref: 0.0224
    proposal: 0.0001
    latex: \Omega_\mathrm{b} h^2

  omch2:
    prior: {min: 0.001, max: 0.99}
    ref: 0.120
    proposal: 0.001
    latex: \Omega_\mathrm{c} h^2

  # Note: H0 is no longer a free parameter in the usual sense;
  # the local H0 is derived from the Dual-Gate formula.
  # We still sample a “base” H0 around 70 for numerical convenience.
  H0_base:
    prior: {min: 65.0, max: 75.0}
    ref: 70.0
    proposal: 0.3
    latex: H_0^\mathrm{base}

  logA:
    prior: {min: 1.61, max: 3.91}
    ref: 3.05
    proposal: 0.001
    drop: true
    latex: \ln(10^{10} A_s)

  As:
    value: "lambda logA: 1e-10*np.exp(logA)"
    latex: A_s

  ns:
    prior: {min: 0.8, max: 1.2}
    ref: 0.965
    proposal: 0.004
    latex: n_s

  tau:
    prior: {min: 0.01, max: 0.2}
    ref: 0.054
    proposal: 0.005
    latex: \tau

  # Dual-Gate parameters (can be fixed or varied)
  jcrin_torque:
    value: 3.17          # fixed to repository value; free if desired
    latex: \Delta H_\mathrm{torque}

  jcrin_tau:
    value: 5.8
    latex: \tau

  # Derived parameters
  Omega_m:
    latex: \Omega_m
  sigma8:
    latex: \sigma_8
  S8:
    derived: "lambda sigma8, Omega_m: sigma8 * (Omega_m/0.3)**0.5"
    latex: S_8
  H0_local:
    derived: "lambda H0_base, jcrin_torque: H0_base + jcrin_torque"
    latex: H_0^\mathrm{local}

  # Weak-lensing nuisance parameters
  A_IA:
    prior: {min: -5.0, max: 5.0}
    ref: 0.5
    proposal: 0.1
    latex: A_\mathrm{IA}

  alpha_IA:
    prior: {min: -5.0, max: 5.0}
    ref: 0.0
    proposal: 0.2
    latex: \eta_\mathrm{IA}

  logT_AGN:
    prior: {min: 7.0, max: 9.0}
    ref: 7.8
    proposal: 0.05
    latex: \log_{10}(T_\mathrm{AGN}/K)

sampler:
  mcmc:
    burn_in: 0
    max_tries: 100000
    covmat: auto
    Rminus1_stop: 0.01
    Rminus1_cl_stop: 0.15
    output_every: 60s
    learn_proposal: true

output: chains/jcrin_dual_gate_joint
