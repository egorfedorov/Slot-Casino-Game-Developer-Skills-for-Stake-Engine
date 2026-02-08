# Books Package Sign-Off Template

```markdown
# <Game Name> Books Package Sign-Off

## 1. Scope
- Game:
- Version/Commit:
- Package path:
- Date:

## 2. Modes
| Mode | Cost | Events File | Weights File |
|---|---:|---|---|
| base | 1 | books_base.jsonl.zst | lookUpTable_base_0.csv |

## 3. Validation Results
| Mode | Files Exist | Book Schema | Book IDs Unique | Weights Valid | ID Coverage | Status |
|---|---|---|---|---|---|---|
| base | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL | PASS/FAIL |

## 4. Findings
- Blocking findings:
- Non-blocking findings:

## 5. Patch Plan
- `<path>:<line>` - change and reason
- `<path>:<line>` - change and reason

## 6. Evidence
- Validator command:
- Validator summary:

## 7. Decision
- Sign-off status: PASS / FAIL
```
