
#!/usr/bin/env python3
"""
Generate simulated data with an explicit mediation mechanism:

citation condition -> perceived verifiability -> trust

This dataset is for demonstrating and validating the planned
mediation-analysis pipeline. It is not empirical participant data.
"""

from pathlib import Path

import numpy as np
import pandas as pd


rng = np.random.default_rng(2026)
N_PER_CONDITION = 150

parameters = {
    "C1_none": {
        "verif_mean": 2.4,
        "direct_trust_effect": 0.0,
        "adopt_probability": 0.43,
        "click_probability": 0.00,
    },
    "C2_fake": {
        "verif_mean": 4.6,
        "direct_trust_effect": 0.35,
        "adopt_probability": 0.62,
        "click_probability": 0.08,
    },
    "C3_real": {
        "verif_mean": 5.1,
        "direct_trust_effect": 0.45,
        "adopt_probability": 0.50,
        "click_probability": 0.22,
    },
}

rows = []

for condition, values in parameters.items():
    perceived_verif = np.clip(
        rng.normal(
            loc=values["verif_mean"],
            scale=1.05,
            size=N_PER_CONDITION,
        ),
        1,
        7,
    )

    # Explicit mediation mechanism:
    # participants who perceive greater verifiability also show greater trust.
    trust = np.clip(
        3.4
        + values["direct_trust_effect"]
        + 0.40 * (perceived_verif - 3.5)
        + rng.normal(0, 0.85, N_PER_CONDITION),
        1,
        7,
    )

    confidence = np.clip(
        3.6
        + 0.22 * trust
        + rng.normal(0, 0.80, N_PER_CONDITION),
        1,
        7,
    )

    adopt_wrong = rng.binomial(
        1,
        values["adopt_probability"],
        N_PER_CONDITION,
    )

    clicked_source = rng.binomial(
        1,
        values["click_probability"],
        N_PER_CONDITION,
    )

    for index in range(N_PER_CONDITION):
        rows.append(
            {
                "condition": condition,
                "trust": round(float(trust[index]), 3),
                "perceived_verif": round(
                    float(perceived_verif[index]), 3
                ),
                "confidence": round(float(confidence[index]), 3),
                "adopt_wrong": int(adopt_wrong[index]),
                "clicked_source": int(clicked_source[index]),
            }
        )

data = pd.DataFrame(rows)

output_path = Path("data/simulated_mediation_data.csv")
output_path.parent.mkdir(parents=True, exist_ok=True)
data.to_csv(output_path, index=False)

print("Generated explicit-mediation dataset")
print(f"Rows: {len(data)}")
print(f"Saved to: {output_path}")

print("\nCondition means:")
print(
    data.groupby("condition")[
        ["trust", "perceived_verif", "confidence", "adopt_wrong"]
    ].mean().round(3)
)
