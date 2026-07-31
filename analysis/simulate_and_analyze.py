"""
Verification Theater — simulated data + full analysis pipeline.
Simulate data under the hypothesized effects, then run the full analysis pipeline.

Three-group between-subjects design: C1 no citation / C2 fake citation / C3 real citation
Hypotheses:
  H1  Trust(C2), Trust(C3) > Trust(C1)   (citations raise trust)
  H2  Trust(C2) ~= Trust(C3)             (appearance is enough -- the core of theater)
  H3  C2 has the highest adoption of the wrong recommendation (the cost of theater)
Mechanism: perceived verifiability mediates trust;
     C3 is checkable, yet few actually check -- "verifiable != verified".

Code and comments in English; narrative interpretation in the README.
"""
import numpy as np
from scipy import stats

rng = np.random.default_rng(42)
N_PER = 100  # effective n per cell after exclusions

# ---------- 1. Simulate ----------
# Ground-truth cell means chosen to instantiate H1-H3.
# trust on 1-7 scale; adoption is P(choose the WRONG laptop B).
params = {
    "C1_none":  dict(trust_mu=3.6, verif_mu=2.4, adopt_p=0.45),
    "C2_fake":  dict(trust_mu=4.7, verif_mu=4.6, adopt_p=0.66),  # fake cite: high trust, high perceived verif, worst adoption
    "C3_real":  dict(trust_mu=4.8, verif_mu=5.1, adopt_p=0.52),  # real cite: trust ~ C2 (H2), but fewer adopt wrong
}
# real-cite verification behavior: link is clickable, but few actually click
verify_click_p = {"C1_none": 0.0, "C2_fake": 0.10, "C3_real": 0.18}

rows = []
for cond, p in params.items():
    trust = np.clip(rng.normal(p["trust_mu"], 1.1, N_PER), 1, 7)
    verif = np.clip(rng.normal(p["verif_mu"], 1.2, N_PER), 1, 7)
    adopt = rng.binomial(1, p["adopt_p"], N_PER)          # 1 = chose wrong Laptop B
    conf  = np.clip(rng.normal(4.8, 1.0, N_PER), 1, 7)
    clicked = rng.binomial(1, verify_click_p[cond], N_PER)
    for i in range(N_PER):
        rows.append((cond, trust[i], verif[i], adopt[i], conf[i], clicked[i]))

cond_arr  = np.array([r[0] for r in rows])
trust_arr = np.array([r[1] for r in rows])
verif_arr = np.array([r[2] for r in rows])
adopt_arr = np.array([r[3] for r in rows])
click_arr = np.array([r[5] for r in rows])

def cell(c): return cond_arr == c
c1, c2, c3 = cell("C1_none"), cell("C2_fake"), cell("C3_real")

print("="*60)
print("Cell summary (simulated)")
print("="*60)
for name, m in [("C1 none", c1), ("C2 fake", c2), ("C3 real", c3)]:
    print(f"{name}: trust={trust_arr[m].mean():.2f}  "
          f"verif={verif_arr[m].mean():.2f}  "
          f"adopt_wrong={adopt_arr[m].mean():.2%}  "
          f"clicked_source={click_arr[m].mean():.2%}")

# ---------- 2. H1 & H2: trust ----------
print("\n" + "="*60)
print("H1 / H2 — Trust")
print("="*60)
F, p = stats.f_oneway(trust_arr[c1], trust_arr[c2], trust_arr[c3])
print(f"One-way ANOVA on trust:  F={F:.2f}, p={p:.4g}")

def cohens_d(a, b):
    na, nb = len(a), len(b)
    sp = np.sqrt(((na-1)*a.var(ddof=1)+(nb-1)*b.var(ddof=1))/(na+nb-2))
    return (a.mean()-b.mean())/sp

# H1: C2 vs C1, C3 vs C1  (expect significant, positive)
for lbl, a, b in [("C2 vs C1", trust_arr[c2], trust_arr[c1]),
                  ("C3 vs C1", trust_arr[c3], trust_arr[c1])]:
    t, pp = stats.ttest_ind(a, b)
    print(f"  H1 {lbl}: t={t:.2f}, p={pp:.4g}, d={cohens_d(a,b):.2f}")

# H2: C2 vs C3  (expect NON-significant — the theater point)
t, pp = stats.ttest_ind(trust_arr[c2], trust_arr[c3])
print(f"  H2 C2 vs C3: t={t:.2f}, p={pp:.4g}, d={cohens_d(trust_arr[c2],trust_arr[c3]):.2f}"
      f"   -> {'NS (supports H2)' if pp>0.05 else 'sig (H2 not supported)'}")

# ---------- 3. H3: adoption of the wrong recommendation ----------
print("\n" + "="*60)
print("H3 — Adoption of the WRONG recommendation")
print("="*60)
from itertools import combinations
counts = {"C1_none": adopt_arr[c1].sum(), "C2_fake": adopt_arr[c2].sum(), "C3_real": adopt_arr[c3].sum()}
ns     = {"C1_none": c1.sum(), "C2_fake": c2.sum(), "C3_real": c3.sum()}
# Chi-square across three groups
table = np.array([[counts[k], ns[k]-counts[k]] for k in ["C1_none","C2_fake","C3_real"]])
chi2, pchi, dof, _ = stats.chi2_contingency(table)
print(f"3x2 chi-square on adoption: chi2={chi2:.2f}, p={pchi:.4g}")
# pairwise two-proportion z-tests
def two_prop_z(x1,n1,x2,n2):
    p1,p2 = x1/n1, x2/n2
    pp = (x1+x2)/(n1+n2)
    se = np.sqrt(pp*(1-pp)*(1/n1+1/n2))
    z = (p1-p2)/se
    return z, 2*(1-stats.norm.cdf(abs(z)))
for a,b in combinations(["C1_none","C2_fake","C3_real"],2):
    z,pp = two_prop_z(counts[a],ns[a],counts[b],ns[b])
    print(f"  {a} ({counts[a]/ns[a]:.0%}) vs {b} ({counts[b]/ns[b]:.0%}): z={z:.2f}, p={pp:.4g}")

# ---------- 4. Mechanism: perceived verifiability mediates trust ----------
print("\n" + "="*60)
print("Mechanism — does perceived verifiability track the fake cite?")
print("="*60)
# Key theater evidence: C2 (fake) perceived verifiability >> C1, approaching C3
for lbl,a,b in [("C2 vs C1", verif_arr[c2],verif_arr[c1]),
                ("C3 vs C2", verif_arr[c3],verif_arr[c2])]:
    t,pp = stats.ttest_ind(a,b)
    print(f"  perceived_verif {lbl}: t={t:.2f}, p={pp:.4g}, d={cohens_d(a,b):.2f}")
# simple mediation: verif -> trust correlation
r,pr = stats.pearsonr(verif_arr, trust_arr)
print(f"  corr(perceived_verif, trust): r={r:.2f}, p={pr:.4g}")

print("\n" + "="*60)
print("Verification behavior — 'verifiable != verified'")
print("="*60)
print(f"  C3 (real, clickable) actual click-through rate: {click_arr[c3].mean():.0%}")
print("  -> Even when sources are genuinely checkable, few check them.")

# save tidy data
import csv
with open("data/simulated_data.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["condition","trust","perceived_verif","adopt_wrong","clicked_source"])
    for r in rows:
        w.writerow([r[0], f"{r[1]:.3f}", f"{r[2]:.3f}", r[3], r[5]])
print("\nSaved -> data/simulated_data.csv")
