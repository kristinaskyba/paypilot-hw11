# AI Adoption Impact Report: assistant for tests of `app/engines/fx.py`

> **How to use this template.** Lab: fill sections 1-6, step by step (steps 1-6). Homework: add the cost in two currencies, the seven Impact Report rows and the residual risk (sections 7-10). Delete the italic hints and the section "How this template maps to the lab and the homework" before submitting. Back every row with a number, a file or a run output. An empty cell is better than an invented number. A negative result is a valid submission.

**System:** PayPilot · **Module:** `app/engines/fx.py` (kit `paypilot-l11-eval`) · **Date:** 2026-11-16 · **Mandate:** Ship it · **Author:** <name>
**Assistant:** Claude Code, `--model sonnet` · **What the assistant saw:** module code without the tariff table (`.claude/settings.json` of the kit, unchanged) · **Kit commit:** d6c471a

---

## How this template maps to the lab and the homework

*Delete this section from the final document.*

| Section | Lab | Homework | Rubric criterion |
| --- | --- | --- | --- |
| Prediction | before step 1, compare after step 6 | - | - |
| 1. Manual baseline | step 1 | stage 1 | 1. Baseline |
| 2. Mutant list | step 2 | stage 1 | 2. Fixed set |
| 3. Review criteria and prompt | step 3 | stage 1 | 3. Review log |
| 4. Generation and coverage | step 4 | stages 1-2 | 4. Breakdown · 5. Cost |
| 5. Generation Review Log | step 5 | stages 1-2 | 3. Review log · 5. Cost |
| 6. Results by mutant class | step 6 | stage 1 | 2. Fixed set · 4. Breakdown |
| 7. Cost in two currencies | - | stage 2 | 5. Cost |
| 8. Impact Report | - | stage 3 | 6. Decision |
| 9. Residual risk | - | stage 3 | 6. Decision |
| 10. AI declaration and chain-ready | - | stage 4 | 7. Chain-ready |

**Three things that make this a decision document, not a list:**

1. Row 3 "Where it does not work" names a mutant class and the set it survived in, not a list of IDs.
2. Row 5 "What we do about it" names the assistant's role (what it writes, what a human writes), not "useful / useless".
3. Row 7 "When we review this" names events that would change the decision, not "as needed".

**Generic version for another system (homework, stage 4).** Save as `ai-adoption-impact-report.generic.md` in the repo root. Copy this template and remove everything tied to PayPilot and `app/engines/fx.py`: module name, tariffs, mutant classes, examples `G-07` and `A-01`, kit commands. Keep the sections and rows that work for measuring an assistant in any system. Do not add your company's own cases.

---

## Prediction before step 1

*Lab: before step 1. Fill in before doing anything; the "Measured" column after step 6.*

| What you predict | Prediction | Measured |
| --- | --- | --- |
| How many of 12 mutants the manual set kills | 10 | 5 |
| How many of 12 mutants the generated set kills | 8 | 9 |
| Which class each set is weaker in (manual / generated) | result shape / result shape | tier value / tier value |

**Biggest gap and what it means:** Manual set: predicted 10, measured 5. The manual tests take expected values from `policy.…`, so all three tier-value mutants change the expectation together with the code and survive. 82 % coverage hid this.

---

## 1. Manual baseline (Manual Baseline Set)

*Lab: step 1 · Homework: stage 1 · Criterion 1. Do not open the assistant until this section is filled in.*

| Field | Value |
| --- | --- |
| Folder | `tests/manual/` |
| Number of test functions (5-8; a parametrized test counts as one) | 6 |
| What from the theory you consciously used in the baseline (e.g. a boundary test) | boundary test (M-01: exactly at the tier1 EUR 500 allowance limit) |
| Timer: start / finish | 11:00 / 11:45 |
| Actual time, min | 45 |
| All tests green on the original module (`pytest tests/manual`) | yes |
| Where expected values come from | tariff table `app/engines/policy.py` |
| Commit of the set | 087ce41 |

| ID | Test name | Rule it checks | Class (tier value / boundary / arithmetic / result shape) |
| --- | --- | --- | --- |
| M-01 | `test_quote_at_allowance_limit_has_no_spread` | exactly at the EUR 500 allowance: no spread | boundary |
| M-02 | `test_quote_above_allowance_uses_tier_spread` | above the allowance: tier1 spread applies | tier value |
| M-03 | `test_quote_with_partial_allowance_charges_only_excess_amount` | partial allowance: spread only on the excess | arithmetic |
| M-04 | `test_quote_uses_spread_override_above_allowance` | override replaces the tier spread | arithmetic |
| M-05 | `test_quote_rejects_unknown_tier` | unknown tier raises an error | none of the 4 |
| M-06 | `test_quote_rejects_unknown_currency` | unknown currency raises an error | none of the 4 |

---

## 2. Mutant list

*Lab: step 2 · Homework: stage 1 · Criterion 2. The list does not change after the commit. The `class` field in `mutants.toml` must be, word for word, one of four Ukrainian values (the kit script groups by them): `значення тіру` (tier value), `межа EUR 1 000` (EUR 1 000 boundary), `арифметика` (arithmetic), `форма результату` (result shape).*

**List file:** `mutants.toml` · **Commit / date fixed:** `cedf5c5` / 2026-11-20 13:56 *(`git log -1 -- mutants.toml`)* · **First mutant run:** 2026-11-20 14:41 *(field `started_at` in the first `reports/mutants-…json` report; must be later; same report shows `"uncommitted": false`)*

| ID | Class | What changed (original → mutant) | Place in code |
| --- | --- | --- | --- |
| A-01 | tier value | `tier2` spread: `0.9` → `1.5` (same effect as `D20`) | `app/engines/policy.py`, `FX_SPREAD_PCT` |
| A-02 | tier value | `tier3` free allowance: `5000` → `500` | `app/engines/policy.py`, `FX_FREE_MONTHLY_ALLOWANCE_EUR` |
| A-03 | tier value | all tiers get the tier1 spread: `FX_SPREAD_PCT[tier]` → `FX_SPREAD_PCT["tier1"]` | `app/engines/fx.py`, `quote()` |
| B-01 | EUR 1 000 boundary | `<= allowance_total` → `< allowance_total` | `app/engines/fx.py`, `quote()`, `within` |
| B-02 | EUR 1 000 boundary | `amount_eur` → `amount` (original currency) in the limit check | `app/engines/fx.py`, `quote()`, `within` |
| B-03 | EUR 1 000 boundary | used allowance ignored: `allowance_used_eur + amount_eur <=` → `amount_eur <=` | `app/engines/fx.py`, `quote()`, `within` |
| C-01 | arithmetic | `charged_eur / amount_eur` → `remaining_eur / amount_eur` | `app/engines/fx.py`, `quote()`, partial allowance |
| C-02 | arithmetic | `gross - spread_amount` → `gross + spread_amount` | `app/engines/fx.py`, `quote()`, `final_amount` |
| C-03 | arithmetic | rate inverted: `from / to` → `to / from` | `app/engines/fx.py`, `mid_rate()` |
| D-01 | result shape | `allowance_applied=within` → `not within` | `app/engines/fx.py`, `FxQuote` return |
| D-02 | result shape | `mid_rate=rate` → `1 / rate` | `app/engines/fx.py`, `FxQuote` return |
| D-03 | result shape | `allowance_used_before_eur` → `0.0` | `app/engines/fx.py`, `FxQuote` return |

---

## 3. Review criteria and prompt

*Lab: step 3 · Homework: stage 1 · Criterion 3. Fill in before generation. Commit `prompts/` before `tests/generated/` appears.*

**Commit / date criteria and prompt were fixed:** `1e209d9` / 2026-11-20 14:04

| Criterion | Accept | Reject |
| --- | --- | --- |
| Oracle | expected value is a number from the tariff table in the requirements, written into the test (`0.9`) | expected value taken from the function's own output, via `policy.…` or other constants the module reads, or from a table replaced with `monkeypatch` |
| Assertion level | comparison with a concrete value (levels 1-2 of the L03 ladder) | `isinstance`, `is not None`, `> 0` |
| Edge case | test exactly at its tier's limit (EUR 500 / 1 000 / 5 000), or a test that does not pretend to check the boundary | test whose name or comment says it checks the boundary (boundary, limit) but sits far from it |
| Independence | result does not depend on test order or the clock | `datetime.now()`, shared state between tests |
| Name | name states the rule being checked | `test_quote_1`, `test_works` |
| Novelty | new input class or new check of the result (a field not checked by your manual set or by already accepted tests) | same input class and same check with a different number |
| *Your own seventh criterion (optional)* | not used | not used |

*For exception tests (`pytest.raises`) and property tests, "Oracle" does not apply: judge them by "Assertion level" and "Novelty". Apply "Edge case" only to tests that by name or comment claim to check the limit. A test with several asserts is judged by the rule it claims in its name; that rule is the main one, also for service parameters. "Novelty" is relative to your manual set and the generated tests already accepted.*

**Generation prompt** (in the lab: the weak prompt, word for word from `prompts/generation-prompt.md`):

```
Згенеруй unit-тести для модуля app/engines/fx.py. Поклади їх у tests/generated/test_fx_generated.py.
```

**Files:** `prompts/review-criteria.md`, `prompts/generation-prompt.md`

---

## 4. Generation and coverage

*Lab: step 4 · Homework: stages 1-2 · Criteria 4 and 5. Generation numbers from `python tools/generation_summary.py reports/generation.json`.*

| Field | Value |
| --- | --- |
| Generation command | `claude -p … --model sonnet --allowedTools "Read,Write,Glob,Grep" --output-format json > reports/generation.json` |
| Model | `claude-sonnet-5-5` (the `sonnet` alias at run time; the lab reference runs used `claude-sonnet-5`) |
| Machine time for generation, min | 0.5 |
| Generation cost, USD | 0.10 |
| Test functions generated | 26 (27 passed: one test is parametrized) |
| Generated set green on the original module | yes (red tests: none) |

| Set | Command | Line coverage of `app/engines/fx.py` |
| --- | --- | --- |
| Manual | `pytest tests/manual --cov=app.engines.fx` | 82 % |
| Generated | `pytest tests/generated --cov=app.engines.fx` | 100 % |

---

## 5. Generation Review Log

*Lab: step 5 · Homework: stages 1-2 · Criteria 3 and 5. One entry per generated test, accepted ones too. A parametrized test is one entry. If a test was rewritten, `minutes` has two parts: review + rewrite. Rewritten tests go to `tests/rewritten/` with ids `R-01`, `R-02`, …; do not change the file in `tests/generated/`. Exception: tests red on the original module are deleted in a separate commit and logged as `rejected`.*

```
id: G-01
verdict: accepted / rejected
criterion: <criterion from section 3, or ->
reason: <what exactly the test checks or does not check>
action: <accepted as is / rejected / rewritten by hand as R-… in tests/rewritten/>
minutes: <review> + <rewrite>   # e.g. 1 + 2; without rewrite, review only

id: G-02
…
```

**Log** (review timer 14:15-14:23; G-07…G-26 were reviewed together in one pass, 1 min in total; rewrite timer 14:30-14:40):

```
id: G-01
verdict: rejected
criterion: oracle
reason: expected 4.0 comes from the monkeypatched table (GBP 2.0 / USD 0.5), not the real tariff table
action: rejected
minutes: 1

id: G-02
verdict: accepted
criterion: -
reason: same currency gives rate 1.0, true with any table (real or monkeypatched); concrete value; new check, mid_rate not in the manual set
action: accepted as is
minutes: 3

id: G-03
verdict: accepted
criterion: -
reason: exact error message checked; unknown to-currency is a new input, the manual set only tests an unknown from-currency
action: accepted as is
minutes: 1

id: G-04
verdict: rejected
criterion: novelty
reason: same input class and same check as manual M-05 (unknown tier -> exact error), only the tier name differs
action: rejected
minutes: 1

id: G-05
verdict: rejected
criterion: novelty
reason: unknown currency already covered by M-06 and accepted G-03 (same check in mid_rate); also checks only the start of the message
action: rejected
minutes: 0.5

id: G-06
verdict: rejected
criterion: novelty
reason: main rule (inside allowance -> no spread) already checked by M-01 with the same asserts; the only extra assert, gross 100.0, comes from the monkeypatched rate
action: rejected
minutes: 0.5

id: G-07
verdict: rejected
criterion: edge case
reason: the "boundary" is the fake limit 100 of the monkeypatched tier "basic", not a real tier limit (500 / 1 000 / 5 000); same rule as M-01
action: rejected
minutes: 0.05

id: G-08
verdict: rejected
criterion: oracle
reason: expected spread 2 % and limit 100 come from the monkeypatched table
action: rejected
minutes: 0.05

id: G-09
verdict: rejected
criterion: oracle
reason: expected spread from the monkeypatched 2 %; limit 100 is fake
action: rejected
minutes: 0.05

id: G-10
verdict: rejected
criterion: oracle
reason: result depends on the monkeypatched USD rate 0.5 and limit 100; the idea (allowance counted in EUR, not the source currency) is new
action: rewritten by hand as R-01 in tests/rewritten/ (real table: USD 540 = EUR 496.80, inside the tier1 EUR 500 allowance)
minutes: 0.05 + 5

id: G-11
verdict: rejected
criterion: oracle
reason: spread 2.0 % and allowance 1 000 come from the monkeypatched tiers "basic" / "premium"
action: rejected
minutes: 0.05

id: G-12
verdict: rejected
criterion: novelty
reason: same input class and check as manual M-04 (spread override above the allowance)
action: rejected
minutes: 0.05

id: G-13
verdict: accepted
criterion: -
reason: new input (override 0.0 is not replaced by the tier spread); expected 0 written into the test
action: accepted as is
minutes: 0.05

id: G-14
verdict: accepted
criterion: -
reason: new rule not in the manual set (override has no effect inside the allowance); expected 0 written into the test
action: accepted as is
minutes: 0.05

id: G-15
verdict: rejected
criterion: oracle
reason: spread 2 % and limit 100 come from the monkeypatched table; same rule as M-03
action: rejected
minutes: 0.05

id: G-16
verdict: rejected
criterion: oracle
reason: expected value from the monkeypatched 2 %; the case (allowance already used up, partial_allowance) is new
action: rewritten by hand as R-02 in tests/rewritten/ (real table: tier1 1.5 %, EUR 600 used of 500, EUR 100 -> spread 1.5, final 98.5)
minutes: 0.05 + 5

id: G-17
verdict: accepted
criterion: -
reason: new input (partial_allowance inside the allowance); expected 0 written into the test
action: accepted as is
minutes: 0.05

id: G-18
verdict: accepted
criterion: -
reason: new input (zero amount); expected 0 values hold with any table
action: accepted as is
minutes: 0.05

id: G-19
verdict: accepted
criterion: -
reason: new input (zero amount with the allowance used up, no division error); expected 0 written into the test
action: accepted as is
minutes: 0.05

id: G-20
verdict: rejected
criterion: novelty
reason: same check (final = gross - spread) as manual M-02, M-03, M-04
action: rejected
minutes: 0.05

id: G-21
verdict: accepted
criterion: -
reason: new check (as_dict rounds floats to 6 places, keeps other types and all fields); values built by hand, no table
action: accepted as is
minutes: 0.05

id: G-22
verdict: rejected
criterion: oracle
reason: expected fee 1.0 is the monkeypatched sepa fee (real: 0.35)
action: rejected
minutes: 0.05

id: G-23
verdict: rejected
criterion: oracle
reason: expected fees are the monkeypatched swift fee 5 + 0.1 % (real: 15 + 0.3 %)
action: rejected
minutes: 0.05

id: G-24
verdict: rejected
criterion: oracle
reason: 5.03 comes from the monkeypatched swift fee
action: rejected
minutes: 0.05

id: G-25
verdict: rejected
criterion: oracle
reason: 5.0 is the monkeypatched swift flat fee
action: rejected
minutes: 0.05

id: G-26
verdict: accepted
criterion: -
reason: exception test, exact message; transfer_fee is not in the manual set
action: accepted as is
minutes: 0.05
```

*Example entry from the lesson:*

```
id: G-07
verdict: rejected
criterion: assertion level
reason: checks isinstance(q.final_amount, float); does not fail
        when the tier spread is swapped
action: rewritten by hand as R-01 in tests/rewritten/
minutes: 1 + 2
```

**Log summary:**

| Metric | Value |
| --- | --- |
| Tests generated (log entries) | 26 |
| Accepted as is | 9 (G-02, G-03, G-13, G-14, G-17, G-18, G-19, G-21, G-26) |
| Rejected | 17 |
| Of the rejected, rewritten by hand | 2 (G-10 -> R-01, G-16 -> R-02) |
| Share rejected, % | 65 % (17 / 26) |
| Most frequent rejection criterion | oracle (11 of 17; novelty 5, edge case 1): the generated file replaces the tariff table with a monkeypatched one |
| Classes covered by accepted tests and missing from the manual set | zero override, override inside the allowance, partial_allowance inside the allowance, zero amount, as_dict rounding (result shape), same-currency rate, unknown to-currency, unknown transfer type |
| Review minutes, total | 8 |
| Rewrite minutes, total | 10 |

---

## 6. Results by mutant class

*Lab: step 6 · Homework: stage 1 · Criteria 2 and 4. The same `mutants.toml` for all three sets.*

| Set | Mutant run command | Report |
| --- | --- | --- |
| Manual | `python tools/run_mutants.py --set manual` | `reports/mutants-manual-20261120-134116Z.json` |
| Generated | `python tools/run_mutants.py --set generated` | `reports/mutants-generated-20261120-134119Z.json` |
| Combined | `python tools/run_mutants.py --set all` | `reports/mutants-all-20261120-134123Z.json` |

| Mutant class (3 each) | Manual | Generated | Combined |
| --- | --- | --- | --- |
| Tier value | 0/3 | 1/3 | 1/3 |
| EUR 1 000 boundary | 2/3 | 3/3 | 3/3 |
| Arithmetic | 2/3 | 3/3 | 3/3 |
| Result shape | 1/3 | 2/3 | 2/3 |
| **Total of 12** | **5** | **9** | **9** |
| **Mutation score** | **42 %** | **75 %** | **75 %** |
| Line coverage (from section 4) | 82 % | 100 % | - |

**Surviving mutants (IDs):** manual A-01, A-02, A-03, B-02, C-01, D-02, D-03 · generated A-01, A-02, D-02 · combined A-01, A-02, D-02

**One sentence about the surviving class:** Tier value survives in both sets: the manual set reads expected values from `policy.py`, and the generated set replaces `policy.py` with a monkeypatched table, so neither notices a wrong tariff.

**Class where the assistant is stronger than me:** EUR 1 000 boundary and arithmetic (3/3 vs 2/3), and result shape (2/3 vs 1/3); but most of these kills come from tests I rejected in review (G-09, G-10, G-15).

---

## 7. Cost in two currencies

*Homework: stage 2 · Criterion 5. Numbers come from sections 1, 4, 5.*

| Row | Manual set | Generated set |
| --- | --- | --- |
| Human time writing, min | 45 | 0 |
| Machine time generating, min | - | 0.5 |
| Generation cost, USD | - | 0.10 |
| Human time reviewing and selecting, min | 0 | 8 |
| Human time rewriting rejected tests, min | 0 | 10 |
| **Total human minutes** | **45** | **18** |
| Mutants killed of 12 | 5 | 9 |

**What follows from this (one sentence):** The generated set cost 18 human minutes plus 0.5 machine minutes and $0.10, against 45 minutes by hand, and killed 9 mutants instead of 5; but 17 of its 26 tests failed review, and most of its extra kills come from rejected tests, so the saving only holds together with the review.

---

## 8. AI Adoption Impact Report

*Homework: stage 3 · Criterion 6. Seven rows in three blocks (can be shown as three slides). The main number is the mutation score with its breakdown; time comes second and always next to review time.*

### Block 1. What we measured

| Row | Content |
| --- | --- |
| 1. What we measured on | one module `app/engines/fx.py`, one list of 12 mutants (commit `cedf5c5`, 2026-11-20), both sets on a fresh clone <SHA of the homework repo>; assistant `claude-sonnet-5-5` saw only `fx.py` (not `policy.py`, the manual set, the mutant list or the review criteria) |
| 2. The number | mutation score: manual 42 % · generated 75 % · combined 75 %; breakdown by class in section 6; share of rejected generated tests 65 % |

### Block 2. Where it does not work and what it costs

| Row | Content |
| --- | --- |
| 3. Where it does not work | Tier value: no set catches a wrong tariff (manual 0/3, generated 1/3). The generated tests replace the tariff table with a fake one, so they only test the calculation, never the real tariffs. |
| 4. Cost | 45 human min (manual) vs 18 human min (generated, 8 review + 10 rewrite), plus 0.5 machine min and $0.10 |

### Block 3. Decision

| Row | Content |
| --- | --- |
| 5. What we do about it | Let the assistant write the logic tests, where it did better than me. I write the tariff tests myself with real numbers from the tariff table, and in review I reject every generated test that uses a fake table. |
| 6. Mandate | under Ship it: we use the reviewed generated set and a human adds tier-value tests before release; under Zero regulatory risk: no generated test is accepted without an expected value from the real tariff table, and release waits until all 3 tier-value mutants are killed |
| 7. When we review this | (1) the assistant model changes; (2) `fx.py` or the tariff table changes; (3) the tariff table or the review criteria are given to the assistant as input (the "strong prompt"); (4) the generated set starts killing tier-value mutants |

**Answer to the CTO in one sentence** *(to "Does anyone have a number?")*: Yes: on `fx.py` the assistant's tests kill 9 of 12 planted bugs vs 5 by hand, for 18 vs 45 human minutes and $0.10, but no set catches a wrong tariff, so a human still writes the tariff tests.

---

## 9. Residual risk

*Homework: stage 3 · Criterion 6. What from the lesson section "What this method does not catch" applies to your measurement. L03 format.*

| Not covered | What will happen | Why we live with it now | Defer or accept |
| --- | --- | --- | --- |
| A wrong number in the tariff table itself (no set kills the tier-value mutants A-01, A-02) | a customer is charged the wrong spread or gets the wrong free allowance, and no test fails | the tests that would catch it are planned for a human (row 5) but not written yet | defer: add tier-value tests with real tariff numbers before release |
| Bugs outside my 12 mutants (for example `transfer_fee`, `as_dict` rounding, other currencies) | the mutation score says nothing about them; a bug there can pass unnoticed | the list covers only the four classes from the lab and must stay fixed for this measurement | accept for this measurement; add classes in the next one |

---

## 10. AI declaration and chain-ready

*Homework: stage 4.*

**AI declaration:** where exactly I used AI: <…> · what I rejected from its output: <link to section 5> · other: <…>

**Chain-ready**: on a fresh clone of your repo after `pip install -r requirements.txt`:

| Check on a fresh clone | Command | Passes |
| --- | --- | --- |
| Manual set | `pytest tests/manual` | yes / no |
| Generated set | `pytest tests/generated` | yes / no |
| Mutant run from the committed list | `python tools/run_mutants.py --set all` | yes / no |

**Attachments:** `tests/manual/` · `tests/generated/` · `tests/rewritten/` · `mutants.toml` · `prompts/` · `reports/` · `ai-adoption-impact-report.generic.md`.

## Before submitting

- [ ] Section 1 has timer start, finish and minutes, not "≈40".
- [ ] Last commit of `mutants.toml` is earlier than the `tests/generated/` commit and the first `reports/mutants-*.json` report; reports committed; same list for all three sets.
- [ ] `tests/manual` commit is earlier than `tests/generated/`, and `tests/manual` was not changed after generation.
- [ ] Last commit of `prompts/` is earlier than `tests/generated/`; `tests/generated/` not edited after generation, except deleting red tests.
- [ ] Log has an entry for every generated test: verdict, criterion, reason, minutes.
- [ ] Section 6: four class rows for three sets, list of survivors, coverage.
- [ ] Section 7: separate rows for review, rewrite, machine minutes and cost.
- [ ] Impact Report rows 3, 5, 6, 7 are concrete and based on your breakdown.
- [ ] "Residual risk" section filled in.
- [ ] Chain-ready commands pass on a fresh clone; `ai-adoption-impact-report.generic.md` and the AI declaration exist.
