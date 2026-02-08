# RNG Crypto Sign-Off Template

```markdown
# <Game/System> RNG Crypto Sign-Off

## 1. Scope
- Service/Game:
- Version/Commit:
- Date:
- Auditor:

## 2. Protocol
- Commit-reveal flow:
- Primitives:
- Serialization format:
- Seed rotation policy:
- Nonce policy:

## 3. Verification Inputs
- Transcript source:
- Sample size:
- Verification script/command:
- Range mapping method:

## 4. Findings
| Check | Result | Notes |
|---|---|---|
| Commitment hash verification | PASS/FAIL | |
| Outcome recomputation | PASS/FAIL | |
| Nonce monotonicity | PASS/FAIL | |
| Bias-safe mapping | PASS/FAIL | |
| Seed rotation enforcement | PASS/FAIL | |

## 5. Patch Plan
- `<path>:<line>` - required fix and rationale
- `<path>:<line>` - required fix and rationale

## 6. Residual Risks
- Blocking:
- Non-blocking:

## 7. Decision
- Sign-off status: PASS / FAIL
```
