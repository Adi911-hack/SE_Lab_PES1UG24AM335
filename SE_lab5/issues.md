# Lab 5: Static Code Analysis — Issue Report

**SRN:** PES1UG24AM335  
**Python file:** event_manager.py  
**Original Pylint score:** 4.64/10

## Identified Issues

| Issue | Type | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| B605 — Shell command injection | Security — High | 56 | `os.system()` constructs a shell command using the event name, potentially allowing command injection. | Replace shell execution with a safe method that does not invoke a shell. |
| B301 — Unsafe deserialization | Security — Medium | 51 | `pickle.load()` can execute malicious code when reading an untrusted file. | Replace pickle serialization with JSON. |
| B403 — Pickle import | Security — Low | 2 | The pickle module introduces security risks when handling untrusted data. | Remove pickle and use the JSON module. |
| B311 — Insecure random generator | Security — Low | 72 | `random.choice()` uses a pseudorandom generator unsuitable for security-sensitive random selection. | Use `secrets.choice()` for the lucky draw. |
| W0102 — Mutable default argument | Bug | 9 | The default guest list is shared between events, causing incorrect guest lists and seat counts. | Use `None` as the default and create a new list for each event. |
| W0613 — Unused argument | Code quality | 39 | The `sortOrder` parameter is declared but never used. | Implement sorting according to the requested order. |
| C0103 — Invalid naming convention | Style | 9, 15, 27, 32, 39, 44, 49, 54 | Function and argument names do not follow snake_case naming conventions. | Rename functions and variables using snake_case. |
| C0114/C0116 — Missing docstrings | Documentation | 1, 9, 15, 27, 32, 39, 44, 49, 54, 59 | The module and functions do not contain docstrings. | Add short descriptions explaining their purpose. |
| R1705 — Unnecessary else | Code quality | 33 | An `else` statement follows a return statement unnecessarily. | Remove the else statement and simplify the function. |
| E231 — Missing whitespace | Formatting | 61 | Missing space after a comma. | Add the required space. |
| E225 — Missing whitespace around operator | Formatting | 66 | Assignment operator does not have surrounding spaces. | Add spaces around the operator. |
| E261 — Inline comment spacing | Formatting | 75 | Insufficient spacing before an inline comment. | Correct the spacing or remove the comment. |
| E305 — Missing blank line | Formatting | 79 | Two blank lines are required after a top-level function definition. | Add the missing blank line. |

## Initial Static Analysis Results

- Pylint score: 4.64/10
- Bandit findings: 4
- Bandit high-severity findings: 1
- Bandit medium-severity findings: 1
- Flake8 findings: 4

## Target Results

- Pylint score above 9.5/10
- No remaining Bandit findings
- No remaining Flake8 violations
- Correct event registration and seat counts
- All existing core functionality preserved

## Final Verification

To be completed after fixing and rerunning all three tools.