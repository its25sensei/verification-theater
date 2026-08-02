#!/usr/bin/env python3
"""
Formal bootstrap mediation analysis for the Verification Theater project.

Research question:
Does citation condition affect trust partly through perceived verifiability?

Model:
    condition -> perceived_verif -> trust

The script compares one treatment condition against one reference condition,
estimates the indirect effect a*b, and reports a percentile bootstrap
confidence interval.

Expected CSV columns:
    condition, trust, perceived_verif

Example:
    python analysis/mediation_analysis.py \
        --data data/simulated_data.csv \
        --treatment C2_fake \
        --reference C1_none \
        --bootstrap 5000
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import pandas as pd


REQUIRED_COLUMNS = {"condition", "trust", "perceived_verif"}


@dataclass(frozen=True)
class MediationResult:
    treatment: str
    reference: str
    n: int
    a_path: float
    b_path: float
    indirect_effect: float
    indirect_ci_low: float
    indirect_ci_high: float
    direct_effect: float
    total_effect: float
    proportion_mediated: float | None


def _ols_coef(y: np.ndarray, *predictors: np.ndarray) -> np.ndarray:
    """Return OLS coefficients for an intercept plus supplied predictors."""
    if y.ndim != 1:
        raise ValueError("Outcome y must be one-dimensional.")
    if any(x.ndim != 1 for x in predictors):
        raise ValueError("Each predictor must be one-dimensional.")
    if any(len(x) != len(y) for x in predictors):
        raise ValueError("All variables must contain the same number of rows.")

    design = np.column_stack([np.ones(len(y)), *predictors])
    coefficients, *_ = np.linalg.lstsq(design, y, rcond=None)
    return coefficients


def _estimate_paths(
    sample: pd.DataFrame, treatment: str
) -> tuple[float, float, float, float]:
    """Estimate a, b, direct (c-prime), and total (c) paths."""
    x = (sample["condition"].to_numpy() == treatment).astype(float)
    mediator = sample["perceived_verif"].to_numpy(dtype=float)
    outcome = sample["trust"].to_numpy(dtype=float)

    # Mediator model: M = i_m + aX + error
    a_path = float(_ols_coef(mediator, x)[1])

    # Outcome model: Y = i_y + c-prime*X + bM + error
    outcome_coefficients = _ols_coef(outcome, x, mediator)
    direct_effect = float(outcome_coefficients[1])
    b_path = float(outcome_coefficients[2])

    # Total-effect model: Y = i_t + cX + error
    total_effect = float(_ols_coef(outcome, x)[1])

    return a_path, b_path, direct_effect, total_effect


def run_mediation(
    data: pd.DataFrame,
    treatment: str,
    reference: str,
    bootstrap: int = 5000,
    seed: int = 2026,
) -> MediationResult:
    if bootstrap < 100:
        raise ValueError("Use at least 100 bootstrap resamples.")
    if treatment == reference:
        raise ValueError("Treatment and reference conditions must differ.")

    missing = REQUIRED_COLUMNS.difference(data.columns)
    if missing:
        raise ValueError(f"CSV is missing required columns: {sorted(missing)}")

    subset = data.loc[data["condition"].isin([reference, treatment])].copy()
    subset = subset.dropna(
        subset=["condition", "trust", "perceived_verif"]
    )

    counts = subset["condition"].value_counts()
    for condition in (reference, treatment):
        if condition not in counts:
            raise ValueError(f"No rows found for condition: {condition}")
        if counts[condition] < 10:
            raise ValueError(
                f"Condition {condition!r} has only {counts[condition]} rows; "
                "at least 10 are required."
            )

    a_path, b_path, direct_effect, total_effect = _estimate_paths(
        subset, treatment=treatment
    )
    indirect_effect = a_path * b_path

    random_generator = np.random.default_rng(seed)
    bootstrap_indirect = np.empty(bootstrap, dtype=float)
    sample_size = len(subset)

    for index in range(bootstrap):
        row_indices = random_generator.integers(
            0, sample_size, size=sample_size
        )
        bootstrap_sample = subset.iloc[row_indices]
        bootstrap_a, bootstrap_b, _, _ = _estimate_paths(
            bootstrap_sample, treatment=treatment
        )
        bootstrap_indirect[index] = bootstrap_a * bootstrap_b

    ci_low, ci_high = np.percentile(bootstrap_indirect, [2.5, 97.5])

    if np.isclose(total_effect, 0.0):
        proportion_mediated = None
    else:
        proportion_mediated = indirect_effect / total_effect

    return MediationResult(
        treatment=treatment,
        reference=reference,
        n=sample_size,
        a_path=a_path,
        b_path=b_path,
        indirect_effect=indirect_effect,
        indirect_ci_low=float(ci_low),
        indirect_ci_high=float(ci_high),
        direct_effect=direct_effect,
        total_effect=total_effect,
        proportion_mediated=proportion_mediated,
    )


def _format_result(result: MediationResult) -> str:
    mediated = (
        "undefined because the total effect is approximately zero"
        if result.proportion_mediated is None
        else f"{result.proportion_mediated:.1%}"
    )
    interval_excludes_zero = not (
        result.indirect_ci_low <= 0.0 <= result.indirect_ci_high
    )

    interpretation = (
        "The indirect effect is statistically distinguishable from zero "
        "because the bootstrap interval excludes zero."
        if interval_excludes_zero
        else
        "The bootstrap interval includes zero, so this sample does not "
        "provide clear evidence of mediation."
    )

    return f"""
Bootstrap mediation: {result.treatment} vs {result.reference}
N = {result.n}

a path  (condition -> perceived verifiability): {result.a_path:.3f}
b path  (perceived verifiability -> trust, controlling condition): {result.b_path:.3f}
Indirect effect a*b: {result.indirect_effect:.3f}
95% bootstrap CI: [{result.indirect_ci_low:.3f}, {result.indirect_ci_high:.3f}]
Direct effect c-prime: {result.direct_effect:.3f}
Total effect c: {result.total_effect:.3f}
Proportion mediated: {mediated}

Interpretation:
{interpretation}
""".strip()


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Bootstrap mediation for Verification Theater."
    )
    parser.add_argument(
        "--data",
        type=Path,
        default=Path("data/simulated_data.csv"),
        help="Path to the project CSV file.",
    )
    parser.add_argument(
        "--treatment",
        default="C2_fake",
        help="Treatment condition label.",
    )
    parser.add_argument(
        "--reference",
        default="C1_none",
        help="Reference condition label.",
    )
    parser.add_argument(
        "--bootstrap",
        type=int,
        default=5000,
        help="Number of bootstrap resamples.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=2026,
        help="Random seed for reproducibility.",
    )
    return parser.parse_args()


def main() -> None:
    arguments = parse_arguments()
    if not arguments.data.exists():
        raise FileNotFoundError(
            f"Data file not found: {arguments.data}. "
            "Run simulate_and_analyze.py first or provide --data."
        )

    data = pd.read_csv(arguments.data)
    result = run_mediation(
        data=data,
        treatment=arguments.treatment,
        reference=arguments.reference,
        bootstrap=arguments.bootstrap,
        seed=arguments.seed,
    )
    print(_format_result(result))


if __name__ == "__main__":
    main()
