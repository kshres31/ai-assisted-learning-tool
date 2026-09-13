# Usability and Experiment Results Template

> **STATUS: NOT YET COLLECTED.** This file is an empty reporting structure. Replace placeholders
> only with verified observations and exported records from a real, approved study.

## Study record

- Application version or commit: `[commit hash]`
- Study dates: `[start date]` to `[end date]`
- Recruitment method: `[method]`
- Consent or review process: `[process]`
- Sessions started: `[verified count]`
- Sessions included in analysis: `[verified count]`
- Exclusion reasons: `[reasons and counts]`
- Control sessions: `[verified count]`
- AI-assisted sessions: `[verified count]`

Do not report a recruitment target as the achieved sample size. Document pilot sessions separately
from sessions included in the main analysis.

## Data-quality checks

- [ ] Every analyzed session maps to exactly one condition.
- [ ] Duplicate or restarted sessions are handled by a documented rule.
- [ ] Durations outside the planned range are reviewed without silently deleting them.
- [ ] Missing questionnaire responses remain missing rather than being converted to zero.
- [ ] Conditional assistance questions are analyzed only for eligible participants.
- [ ] No names, emails, submitted code, or recruitment records appear in the analysis dataset.
- [ ] The analysis script or calculations can be reproduced from the retained de-identified data.

## Quantitative results

Report count, denominator, median, and spread where appropriate. With a small pilot, show individual
points or distributions rather than relying only on averages.

| Measure | Control | AI-assisted | Comparison and uncertainty |
| --- | ---: | ---: | --- |
| Exercise completion rate | `[value]` | `[value]` | `[method and interval]` |
| Attempts per exercise | `[value]` | `[value]` | `[method and interval]` |
| Failed attempts per exercise | `[value]` | `[value]` | `[method and interval]` |
| Active time per exercise | `[value]` | `[value]` | `[method and interval]` |
| Confidence rating | `[value]` | `[value]` | `[method and interval]` |
| Hint requests | Not available | `[value]` | Descriptive only |

### Questionnaire

| Item | Eligible responses | Median | Distribution or range |
| --- | ---: | ---: | --- |
| Q1: Find an exercise | `[n]` | `[value]` | `[value]` |
| Q2: Instructions clear | `[n]` | `[value]` | `[value]` |
| Q3: Run and view results | `[n]` | `[value]` | `[value]` |
| Q4: Feedback supports next step | `[n]` | `[value]` | `[value]` |
| Q5: Condition understandable | `[n]` | `[value]` | `[value]` |
| Q6: Interface supports learning | `[n]` | `[value]` | `[value]` |
| Q7: Confidence | `[n]` | `[value]` | `[value]` |
| Q8: Frustration | `[n]` | `[value]` | `[value]` |
| Q9: Intent to reuse | `[n]` | `[value]` | `[value]` |
| Q10–Q12: Assisted-only items | `[n]` | `[value]` | `[value]` |

## Usability observations

| Issue | Evidence | Severity | Sessions affected | Recommended change |
| --- | --- | ---: | ---: | --- |
| `[concise issue]` | `[observed behavior or short compliant quote]` | `[0–3]` | `[count]` | `[change]` |

Separate observed behavior from interpretation. Do not write that a participant “did not care” or
“was confused” unless the evidence shows what they said or did.

## Qualitative themes

For each theme, document the coding rule, supporting sessions, contradictory evidence, and one or
two short de-identified excerpts when consent permits quoting.

### Theme: `[name]`

- Coding rule: `[rule]`
- Supporting sessions: `[anonymous IDs or count]`
- Contradictory evidence: `[evidence]`
- Interpretation: `[bounded interpretation]`

## Limitations

Discuss recruitment bias, sample size, prior experience, random group imbalance, exercise order,
moderator effects, client-reported active time, local environment, missing data, and whether the
mock or external provider produced assistance. Do not generalize beyond the studied population and
tasks.

## Conclusions and next actions

- Findings supported by the data: `[findings]`
- Questions that remain unanswered: `[questions]`
- Changes to implement: `[prioritized changes]`
- Follow-up study needed: `[design]`
