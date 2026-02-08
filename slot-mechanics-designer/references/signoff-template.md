# Slot Mechanics Sign-Off Template

```markdown
# <Game Name> Mechanics Sign-Off

## 1. Scope
- Game:
- Version/Commit:
- Date:

## 2. State Graph
- Initial state:
- States:
- Terminal states:
- Transition count:

## 3. Mechanics
| ID | Trigger Event | Entry State | Target State | Actions | Notes |
|---|---|---|---|---|---|
| free_spins | scatter_trigger | base | free_spins | award_spins,set_multiplier | |

## 4. Validation
| Check | Result | Notes |
|---|---|---|
| State references valid | PASS/FAIL | |
| Reachability | PASS/FAIL | |
| Exit paths for non-terminal states | PASS/FAIL | |
| Mechanic-transition alignment | PASS/FAIL | |

## 5. Patch Plan
- `<path>:<line>` - change and rationale
- `<path>:<line>` - change and rationale

## 6. Risks
- Blocking:
- Non-blocking:

## 7. Decision
- Sign-off status: PASS / FAIL
```
