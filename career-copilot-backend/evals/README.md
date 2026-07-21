# AI evaluation set

`evaluation_cases.json` is the release rubric for Career Copilot's AI behavior. It
contains 30 cases covering résumé quality, document detection, coaching, job match,
grounding, and provider failures.

Before changing a prompt or model:

1. Update `PROMPT_VERSION`.
2. Run the automated test suite.
3. Exercise the relevant cases with a fixed test profile.
4. Score each expected behavior pass/fail and record regressions.
5. Do not ship a prompt that improves style while reducing grounding or safety.

The provider-failure and structural expectations are automated in `tests/test_api.py`.
Subjective coaching quality remains a human-reviewed evaluation to avoid spending
free-tier quota on an unreliable model-as-judge loop.
