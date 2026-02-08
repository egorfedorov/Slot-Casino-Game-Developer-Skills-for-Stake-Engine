# Performance Sign-Off Template

```markdown
# <Project> C++ Performance Sign-Off

## 1. Scope
- Commit:
- Benchmark suite:
- Date:

## 2. Environment
- Compiler + flags:
- CPU/OS:
- Run parameters:

## 3. Summary
- Total benchmarks compared:
- Regressions above threshold:
- Improvements above threshold:
- Overall status: PASS / FAIL

## 4. Top Regressions
| Benchmark | Baseline | Current | Delta % |
|---|---:|---:|---:|

## 5. Top Improvements
| Benchmark | Baseline | Current | Delta % |
|---|---:|---:|---:|

## 6. Patch Plan
- `<path>:<line>` - optimization/fix and rationale
- `<path>:<line>` - optimization/fix and rationale

## 7. Risks
- Measurement noise:
- Functional risk:
- Maintainability risk:
```
