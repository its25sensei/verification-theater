# Verification Theater: A Micro Behavioral Experiment Design

## Research question
In AI recommendation systems, how does the **verifiability** of source
citations affect consumer trust and decision quality?
Core theoretical contribution: **verification theater** — unverifiable
citations create an *appearance* of credibility, producing a lift in trust
comparable to genuine citations while failing to improve (and possibly
harming) decision quality.

## Design: three-group between-subjects
| Group | AI recommendation | Citation format |
|-------|-------------------|-----------------|
| C1 no citation | Recommends Laptop B (wrong) | Reasoning only, no source |
| C2 fake citation | Recommends Laptop B (wrong) | Reasoning + unverifiable source |
| C3 real citation | Recommends Laptop B (wrong) | Reasoning + verifiable source (but misleading interpretation) |

All three groups deliver the same conclusion (recommend the wrong option B),
with wording matched for length; the only variable is citation format.

## Decision task
Choose the "better value" between two laptops.
- Laptop A: objectively superior (better CPU/memory/battery, lower price) — the correct answer
- Laptop B: objectively worse and more expensive — the option the AI recommends

## Dependent variables
1. Trust: trust in the AI (established scale, 7-point Likert)
2. Decision quality: whether the AI recommendation is adopted (adopting the wrong rec = poor quality)
3. Confidence: decision confidence
4. Verification behavior: whether the source is clicked/viewed (C2/C3)

## Hypotheses
- H1: Trust(C2), Trust(C3) > Trust(C1) (citations raise trust)
- H2: Trust(C2) ~= Trust(C3) (appearance is enough — the core of theater)
- H3: C2 has the highest adoption of the wrong recommendation, i.e. the worst decision quality (the cost of theater)

## Open design decision (resolved)
Whether the real-citation group (C3) also recommends the wrong option.
Resolved in favor of a symmetric design: all three groups recommend the
wrong option, so the only variable is citation format. This maximizes
internal validity (clean causal inference) at the cost of some realism.
