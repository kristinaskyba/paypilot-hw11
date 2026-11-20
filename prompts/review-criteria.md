# Review criteria (L11, step 3)

Written before generation. Every generated test gets one verdict (accepted / rejected) with a criterion and a reason.

| Criterion | Accept | Reject |
| --- | --- | --- |
| Oracle | expected value is a number from the tariff table in the requirements, written into the test (`0.9`) | expected value taken from the function's own output, via `policy.…` or other constants the module reads, or from a table replaced with `monkeypatch` |
| Assertion level | comparison with a concrete value (levels 1-2 of the L03 ladder) | `isinstance`, `is not None`, `> 0` |
| Edge case | test exactly at its tier's limit (EUR 500 / 1 000 / 5 000), or a test that does not pretend to check the boundary | test whose name or comment says it checks the boundary (boundary, limit) but sits far from it |
| Independence | result does not depend on test order or the clock | `datetime.now()`, shared state between tests |
| Name | name states the rule being checked | `test_quote_1`, `test_works` |
| Novelty | new input class or new check of the result (a field not checked by the manual set or by already accepted tests) | same input class and same check with a different number |

## How to apply

- Exception tests (`pytest.raises`) and property tests: "Oracle" does not apply; judge them by "Assertion level" and "Novelty".
- "Edge case" applies only to tests that by name or comment claim to check the limit.
- A test with several asserts is judged by the rule it claims in its name; that rule is the main one, also for service parameters.
- "Novelty" is relative to the manual set and the generated tests already accepted.
