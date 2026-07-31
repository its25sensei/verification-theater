# MTurk HIT Setup

## 1. Sample size (from the power analysis)
- Target: effective n ≈ 100 per cell (power = .80, α = .05)
- Coverage: a 20pp adoption-rate difference (needs 96); a medium trust effect d = .4–.5 (needs 63–99)
- Recruitment: accounting for MTurk data loss (~15–20% from failed attention
  and manipulation checks), **recruit 120 per cell, 360 total**
- Random assignment: on entry, participants are randomized with equal
  probability into C1/C2/C3

## 2. Payment (rates change; verify current standards online)
- Estimated survey length: 8–12 minutes (read specs + recommendation + scales)
- Target hourly rate: ~$9–12/hour (above typical MTurk levels, to buy data quality)
- Per-response reward: **~$1.50–2.00**
- Note: underpaying → poor data quality and more careless responding; this is a key investment in data quality

## 3. MTurk platform fees (verify current commission online)
- Amazon charges a platform fee on the reward (historically 20%, possibly higher for large-sample HITs)
- For budgeting, estimate reward × 1.4 (covers platform fee + a small bonus buffer)

## 4. Cost estimate (finalize after verifying current rates online)
| Item | Unit price | Quantity | Subtotal |
|------|-----------|----------|----------|
| Participant reward | $1.75 | 360 | $630 |
| Platform fee (~40% buffer) | — | — | ~$252 |
| **Total (rough)** | | | **~$880** |

> If budget-sensitive: first run a pilot (30 per cell, 90 total, ~$220) to
> validate the procedure and effect direction, then decide on the full run.
> For a "demonstrable output" goal, pilot data is often already enough to
> write into an application.

## 5. Worker qualifications (MTurk)
- HIT approval rate ≥ 95% (historical approval rate)
- Number of HITs completed ≥ 500 or 1000 (filters out new/bot accounts)
- Location restricted to the US (language and cultural consistency; avoids non-native-speaker noise)
- Each Worker may participate only once (use a qualification or external-platform de-duplication)

## 6. Anti-cheating / data-quality measures
- Attention-check item (AC1): embedded in the scale; failures pre-registered for exclusion
- Manipulation check (MC1): used for a sensitivity analysis
- Minimum completion time: unusually fast completions (e.g. < 3 minutes) are flagged as suspect
- Optional: minimum word count on open-ended items / consistency checks
- Completion-code mechanism: the survey ends with a unique code entered back into MTurk to claim payment, preventing empty submissions

## 7. Survey platform
- Recommended: Qualtrics (mature randomization, click logging, display logic), or
  free alternatives: Google Forms (weaker, hard to log clicks) / SoSci Survey (free, powerful)
- **Click logging matters**: C3 verification behavior needs real click data;
  Qualtrics Timing / JavaScript can record it, Google Forms cannot
- MTurk external-link survey → completion code at the end → Workers enter it back into MTurk

## 8. Informed consent (IRB / ethics)
- See materials/04_consent_debrief.md
- Anonymous, withdraw at any time, minimal risk
- Note: the deception element (the AI deliberately gives a wrong recommendation) must be explained in the closing debrief
- For formal publication, the researcher's institutional IRB approval is required;
  as an individual pilot/learning project, basic ethics (consent + debrief) should still be followed

## Items to verify online
- [ ] MTurk 2026 current platform commission rate
- [ ] MTurk vs Prolific current rates and data-quality comparison
- [ ] Whether Qualtrics offers a usable free/educational allotment
