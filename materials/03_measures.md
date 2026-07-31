# Measurement Instruments (Dependent and Control Variables)

All Likert items use a 7-point scale: 1 = strongly disagree ... 7 = strongly agree.
Presentation order: decision → confidence → trust scale → verification behavior
→ manipulation check → demographics.

---

## 1. Primary decision (core decision-quality measure)

**Q_choice.** Considering the specs you saw and the AI assistant's
recommendation, which laptop would you choose?
- ( ) Laptop A
- ( ) Laptop B   ← adopts the AI's wrong recommendation

> Coding: choice_B = 1 indicates adoption of the wrong recommendation.
> **This is the core dependent variable for H3.**

---

## 2. Decision confidence

**Q_conf.** How confident are you in the choice you just made?
1 (not at all confident) — 7 (very confident)

---

## 3. Trust in the AI (adapted from McKnight et al. 2002 trust scale)

Source: McKnight, Choudhury & Kacmar (2002), *Information Systems Research*.
This scale is widely used in the IS field and has three dimensions:
competence / benevolence / integrity. Adapted below for the shopping-AI
context (2 items per dimension, 6 items total; the mean is the trust score):

**Competence**
- T1. This AI shopping assistant is capable of giving good purchasing advice.
- T2. This AI assistant is competent at recommending products.

**Benevolence**
- T3. This AI assistant acts in my best interest.
- T4. This AI assistant puts my needs first.

**Integrity**
- T5. The information this AI assistant provides is honest.
- T6. The recommendation this AI assistant gives is trustworthy.

> trust_score = mean(T1..T6). Cronbach's α can be reported.
> **Core dependent variable for H1 and H2.**

---

## 4. Perceived verifiability (part manipulation check, part mediator)

**V1.** The information sources the AI assistant provided appear to be verifiable.
**V2.** I could check the materials the AI assistant based its advice on.

> perceived_verifiability = mean(V1, V2).
> Expectation: C3 > C2 ≈ C1? — This is itself an interesting finding:
> if C2 (fake citation) also shows higher perceived verifiability than C1,
> it shows that "fake sources" can create an *appearance* of verifiability —
> mechanistic evidence for theater.

---

## 5. Verification behavior (meaningful mainly for C2/C3, but asked of all)

**B1.** Before making your decision, did you click or view the sources the AI provided?
- ( ) Yes, I viewed them  ( ) No, I did not

> If the survey platform can log clicks, use **actual click logs** rather than
> self-report (self-report has social-desirability bias).
> Key metric: the actual verification rate in C3. Expectation: very low —
> "verifiable ≠ verified".

**B2.** (only for those who answered "Yes") After viewing the sources, did your view of the recommendation change?
- ( ) Trusted it more  ( ) No change  ( ) More skeptical

---

## 6. Manipulation check

**MC1.** Thinking back, did the AI assistant **provide information sources / references** with its recommendation?
- ( ) Yes  ( ) No  ( ) Don't remember

> C1 should mostly choose "No"; C2/C3 should mostly choose "Yes."
> Those who fail are flagged for a sensitivity analysis (run both with and
> without them).

---

## 7. Attention check (guards against careless MTurk responding)

**AC1.** (embedded in the middle of the trust scale) For this item, please select "3" to show you are reading carefully.
1 — 2 — 3 — 4 — 5 — 6 — 7

> Those who fail are pre-registered for exclusion (necessary for MTurk data quality).

---

## 8. Demographics and control variables

- Age (numeric)
- Gender
- Highest education
- Experience/familiarity with buying laptops (1-7)
- Frequency of daily AI-tool use (1-7)
- Self-rated AI literacy (1-7)

> Familiarity and AI literacy are important covariates: tech-savvy participants
> may be more resistant to inducement and should be controlled for in the model.

---

## Variable summary (for alignment with the analysis scripts)
| Variable | Meaning | Type |
|----------|---------|------|
| condition | C1/C2/C3 | factor |
| choice_B | adopted wrong rec = 1 | binary (primary DV) |
| trust_score | mean trust | continuous (primary DV) |
| confidence | decision confidence | continuous |
| perceived_verif | perceived verifiability | continuous (mediator) |
| verified | verified the source or not | binary |
| passed_mc | passed manipulation check | binary |
| passed_ac | passed attention check | binary |
| + demographics/controls | | |
