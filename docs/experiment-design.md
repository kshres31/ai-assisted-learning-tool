# A/B Experiment Design

## Research question

For introductory Python exercises, how does optional staged assistance affect successful
completion, attempts, active time, hint use, and self-reported confidence compared with a
traditional debugging workflow?

## Hypothesis

Learners with staged assistance will complete more exercises with fewer failed attempts, while
still doing the reasoning themselves because full explanations require a separate explicit action.
This is a hypothesis to test, not a measured result.

## Variables and groups

- **Independent variable:** access to staged hints and solution explanations.
- **Control condition (`control`):** exercises and submission feedback, with assistance disabled.
- **Experimental condition (`ai_assisted`):** the same exercises and feedback, plus staged hints.
- **Dependent variables:** completion, successful and failed submissions, client-reported active
  time, hint and explanation use, and a 1–5 confidence rating.

The backend assigns each new anonymous session with a cryptographically secure random choice. The
condition is stored once and enforced on assistance endpoints whenever the client supplies the
session ID. Assignment is not stratified, so a small pilot may produce unequal group sizes.

## Procedure

1. Explain the study, privacy boundaries, and voluntary participation; obtain any required consent.
2. Create one anonymous session for the participant and retain its assigned condition.
3. Give every participant the same instructions and exercise order.
4. Send the session ID with each experiment request in the `X-Session-ID` header.
5. Record submission duration as active working time since the learner's previous action.
6. Ask for a 1–5 confidence rating after the assigned exercises.
7. Export de-identified records only after checking the study's approval and retention rules.

## Metrics and analysis plan

Compare completion rate and the distribution of attempts, failures, active time, and confidence
between conditions. Report group sizes and uncertainty; do not treat a tiny convenience sample as
proof of a general learning effect. Hint usage is descriptive for the assisted group and should not
be compared as though control participants could request hints.

Active time is reported by the client and can be distorted by inactive tabs or interrupted
sessions. A future frontend should pause its timer when the page is hidden and send incremental
durations rather than total elapsed wall-clock time.

## Privacy and ethics

The database stores random session IDs, experiment conditions, exercise IDs, event timestamps,
outcomes, durations, hint levels, and confidence ratings. It does not request names, email
addresses, demographic fields, IP addresses, or submitted source code. The application is a study
prototype, not a consent system; real research must define recruitment, consent, withdrawal, data
retention, access, and institutional-review requirements before involving participants.

## Current status and limitations

The assignment, enforcement, and analytics infrastructure is implemented and tested. No
participants have been recruited and no experimental outcomes exist. The local SQLite store is
appropriate for a supervised prototype, but multi-instance deployment would require a shared
database and stronger operational controls.
