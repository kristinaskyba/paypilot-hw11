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
| How many of 12 mutants the manual set kills | 10 | <…> |
| How many of 12 mutants the generated set kills | 8 | <…> |
| Which class each set is weaker in (manual / generated) | result shape / result shape | <…> |

**Biggest gap and what it means:** <…>

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

**List file:** `mutants.toml` · **Commit / date fixed:** `cedf5c5` / 2026-11-20 13:56 *(`git log -1 -- mutants.toml`)* · **First mutant run:** <date> *(field `started_at` in the first `reports/mutants-…json` report; must be later; same report shows `"uncommitted": false`)*

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
| Model | <…> |
| Machine time for generation, min | <…> |
| Generation cost, USD | <…> |
| Test functions generated | <…> |
| Generated set green on the original module | yes / no (red tests: <…>) |

| Set | Command | Line coverage of `app/engines/fx.py` |
| --- | --- | --- |
| Manual | `pytest tests/manual --cov=app.engines.fx` | <…> % |
| Generated | `pytest tests/generated --cov=app.engines.fx` | <…> % |

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
| Tests generated (log entries) | <N> |
| Accepted as is | <…> |
| Rejected | <…> |
| Of the rejected, rewritten by hand | <…> |
| Share rejected, % | <rejected / N> |
| Most frequent rejection criterion | <…> |
| Classes covered by accepted tests and missing from the manual set | <…> |
| Review minutes, total | <…> |
| Rewrite minutes, total | <…> |

---

## 6. Results by mutant class

*Lab: step 6 · Homework: stage 1 · Criteria 2 and 4. The same `mutants.toml` for all three sets.*

| Set | Mutant run command | Report |
| --- | --- | --- |
| Manual | `python tools/run_mutants.py --set manual` | `reports/mutants-manual-…json` |
| Generated | `python tools/run_mutants.py --set generated` | `reports/mutants-generated-…json` |
| Combined | `python tools/run_mutants.py --set all` | `reports/mutants-all-…json` |

| Mutant class (3 each) | Manual | Generated | Combined |
| --- | --- | --- | --- |
| Tier value | _/3 | _/3 | _/3 |
| EUR 1 000 boundary | _/3 | _/3 | _/3 |
| Arithmetic | _/3 | _/3 | _/3 |
| Result shape | _/3 | _/3 | _/3 |
| **Total of 12** | **__** | **__** | **__** |
| **Mutation score** | **__ %** | **__ %** | **__ %** |
| Line coverage (from section 4) | __ % | __ % | - |

**Surviving mutants (IDs):** manual <…> · generated <…> · combined <…>

**One sentence about the surviving class:** <which class survived, in which set and why>

**Class where the assistant is stronger than me:** <…>

---

## 7. Cost in two currencies

*Homework: stage 2 · Criterion 5. Numbers come from sections 1, 4, 5.*

| Row | Manual set | Generated set |
| --- | --- | --- |
| Human time writing, min | <from section 1> | 0 |
| Machine time generating, min | - | <from section 4> |
| Generation cost, USD | - | <from section 4> |
| Human time reviewing and selecting, min | 0 | <from section 5> |
| Human time rewriting rejected tests, min | 0 | <from section 5> |
| **Total human minutes** | **<…>** | **<…>** |
| Mutants killed of 12 | <…> | <…> |

**What follows from this (one sentence):** <…>

---

## 8. AI Adoption Impact Report

*Homework: stage 3 · Criterion 6. Seven rows in three blocks (can be shown as three slides). The main number is the mutation score with its breakdown; time comes second and always next to review time.*

### Block 1. What we measured

| Row | Content |
| --- | --- |
| 1. What we measured on | one module `app/engines/fx.py`, one list of 12 mutants (commit <date>), both sets on a fresh clone <SHA of the homework repo>; assistant <model> saw <what exactly> |
| 2. The number | mutation score: manual <…> % · generated <…> % · combined <…> %; breakdown by class in section 6; share of rejected generated tests <…> % |

### Block 2. Where it does not work and what it costs

| Row | Content |
| --- | --- |
| 3. Where it does not work | <mutant class no set killed / the assistant misses, as a class, not a list> |
| 4. Cost | <…> human min (manual) vs <…> human min (generated, with review and rewrite), plus <…> machine min and $<…> |

### Block 3. Decision

| Row | Content |
| --- | --- |
| 5. What we do about it | <assistant's role: what it writes, what a human adds> |
| 6. Mandate | under Ship it: <…>; under Zero regulatory risk: <…> |
| 7. When we review this | <conditions: assistant model change, module change, tariff table appearing in the assistant's context, …> |

**Answer to the CTO in one sentence** *(to "Does anyone have a number?")*: <…>

---

## 9. Residual risk

*Homework: stage 3 · Criterion 6. What from the lesson section "What this method does not catch" applies to your measurement. L03 format.*

| Not covered | What will happen | Why we live with it now | Defer or accept |
| --- | --- | --- | --- |
| <…> | <…> | <…> | <…> |

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
