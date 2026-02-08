---
name: stake-game-developer
description: End-to-end Stake game development workflow for math, RGS contract, frontend playback, and compliance gating. Use when building or updating Stake games, defining game modes and RTP targets, validating generated books/index metadata, validating event streams, integrating frontend event playback, or preparing publication checks including social-language and jurisdiction requirements.
---

# Stake Game Developer

Use this skill to design, validate, and ship Stake games with deterministic event playback and compliance gates.

## Workflow

1. Define or review the game brief, modes, and constraints.
Load `references/workflow.md`.
2. Validate book/index integrity before UI assumptions.
Run `scripts/validate-books-index.mjs`.
3. Validate event stream contract and sequencing.
Run `scripts/validate-rgs-events.mjs`.
4. Validate frontend integration expectations.
Load `references/frontend-integration.md` and `references/rgs-event-contract.md`.20→ 5. Run compliance gate checks before release review.
21→ Run `scripts/audit-checklist.mjs` using `references/compliance-rules.json` and `references/compliance-checklist.md`.
22→
23→ 6. Final Approval Check.
24→ Validate full game against `references/game-approval-checklist.md` (PreChecks, Math, Frontend, Jurisdiction).
25→
26→ ## Commands```bash
node scripts/validate-books-index.mjs --index <path/to/index.json> --format text
node scripts/validate-rgs-events.mjs --input <path/to/events.jsonl> --format text
node scripts/audit-checklist.mjs --rules references/compliance-rules.json --target <project-or-doc-path> --social true --format text
```

Treat non-zero exits as hard blockers for release readiness.

## References

- `references/workflow.md`: End-to-end process and required gates.
- `references/book-generation-validation.md`: Book generation and index validation expectations.
- `references/rgs-event-contract.md`: Required event order and field expectations.
- `references/frontend-integration.md`: Deterministic player integration patterns.40→ - `references/compliance-checklist.md`: Stake checklist and jurisdiction requirements.
41→ - `references/compliance-rules.json`: Machine-readable restricted phrase and required-phrase checks.
42→ - `references/game-approval-checklist.md`: Comprehensive QA/Release sign-off gates.
43→
44→ ## Execution Rules
- Keep frontend stateless: never re-calculate payouts if events already provide them.
- Validate data contracts before tuning UX or animation details.
- Enforce compliance checks by default (`--social true`) unless user explicitly says otherwise.
- When reporting findings, include file path and line when available.
