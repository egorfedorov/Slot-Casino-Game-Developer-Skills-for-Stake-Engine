# Latency Sign-Off Template

```markdown
# <Service> Low-Latency Sign-Off

## 1. Scope
- Service/Endpoint:
- Commit:
- Date:

## 2. Environment
- Host/runtime:
- Concurrency/load profile:
- Dataset/payload profile:

## 3. Percentile Summary
| Metric | Baseline (ms) | Current (ms) | Delta % |
|---|---:|---:|---:|
| p50 |  |  |  |
| p95 |  |  |  |
| p99 |  |  |  |
| p999 |  |  |  |

## 4. Findings
- Top regressions:
- Top improvements:
- Tail risk notes:

## 5. Patch Plan
- `<path>:<line>` - change and rationale
- `<path>:<line>` - change and rationale

## 6. Decision
- Thresholds:
- Status: PASS / FAIL
```
