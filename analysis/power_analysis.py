"""
Power analysis for the verification-theater experiment.
Estimates the per-cell sample size for the three-group between-subjects design.
Two core tests drive the sample size:
  (A) H3 - difference in adoption rate of the wrong recommendation
      (two-proportion test, C2 vs C1)
  (B) H1 - difference in trust across groups (one-way ANOVA / two-group means)
Take the larger of the two N values as the per-cell sample size.
"""
import numpy as np
from scipy import stats

# ---------- (A) Two-proportion test: adoption of wrong rec, C2 vs C1 ----------
# Conservative expectation: no-citation adoption p1=0.45, fake-citation p2=0.65
# (fake citations push adoption up by ~20 percentage points -- the cost of theater)
def n_two_proportions(p1, p2, alpha=0.05, power=0.80):
    z_a = stats.norm.ppf(1 - alpha/2)
    z_b = stats.norm.ppf(power)
    pbar = (p1 + p2) / 2
    num = (z_a*np.sqrt(2*pbar*(1-pbar)) + z_b*np.sqrt(p1*(1-p1)+p2*(1-p2)))**2
    den = (p1 - p2)**2
    return num / den

for (p1, p2) in [(0.45, 0.65), (0.45, 0.60), (0.40, 0.60)]:
    n = n_two_proportions(p1, p2)
    print(f"[proportions] p1={p1}, p2={p2}  ->  n per group = {np.ceil(n):.0f}")

print()

# ---------- (B) Two-group means (trust), Cohen's d ----------
# Expected citation vs no-citation effect on trust: d=0.4~0.5 (medium)
def n_two_means(d, alpha=0.05, power=0.80):
    z_a = stats.norm.ppf(1 - alpha/2)
    z_b = stats.norm.ppf(power)
    return 2 * ((z_a + z_b)/d)**2

for d in [0.4, 0.45, 0.5]:
    n = n_two_means(d)
    print(f"[means] Cohen's d={d}  ->  n per group = {np.ceil(n):.0f}")

print()
# ---------- Rough ANOVA correction for three groups ----------
# Pairwise comparisons across three groups require a Bonferroni-corrected alpha -> 0.05/3
def n_two_means_bonf(d, alpha=0.05/3, power=0.80):
    z_a = stats.norm.ppf(1 - alpha/2)
    z_b = stats.norm.ppf(power)
    return 2 * ((z_a + z_b)/d)**2
print("With Bonferroni correction for three pairwise comparisons (more conservative):")
for d in [0.4, 0.5]:
    n = n_two_means_bonf(d)
    print(f"[means, Bonf] d={d}  ->  n per group = {np.ceil(n):.0f}")
