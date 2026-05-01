# Proof Packet

Project: unit27-stack-engine
Generated: 2026-05-01T01:09:29+00:00

## Verified Claims

- Stack Engine can convert saved operational goals into scored AI workflow architecture artifacts.
  - Case: `core-cli-acceptance`
  - Command: `/bin/zsh -lc '/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 -m unittest discover -s tests'`
  - Evidence: `u27/evidence/run-0001.txt`

- Stack Engine's saved demo command runs without requiring an API key.
  - Case: `first-use-demo`
  - Command: `/bin/zsh -lc '/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 stack_engine.py --example musician --saved'`
  - Evidence: `u27/evidence/run-0002.txt`

- Stack Engine's eval runner completes against the repository eval cases.
  - Case: `eval-runner`
  - Command: `/bin/zsh -lc '/Users/joshuabloodworth/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3 evals/run_evals.py'`
  - Evidence: `u27/evidence/run-0003.txt`

## Open Failures

- No failing, blocked, or regression runs are recorded.

## Known Limits
- This evidence covers saved examples and deterministic local paths only.
- It does not prove OpenAI API generation quality or every possible user input.
- Saved demo evidence proves the offline first-use path only.
- Eval evidence covers the local eval cases only; it does not certify universal workflow recommendations.

## Case Inventory
- `core-cli-acceptance`: pass - Stack Engine can convert saved operational goals into scored AI workflow architecture artifacts.
- `eval-runner`: pass - Stack Engine's eval runner completes against the repository eval cases.
- `first-use-demo`: pass - Stack Engine's saved demo command runs without requiring an API key.
