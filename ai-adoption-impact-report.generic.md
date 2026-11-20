# AI Adoption Impact Report: assistant for tests of `<module under test>`

> **How to use this template.** Measure a test-writing assistant on one module against a manual baseline, using one fixed list of mutants. Fill the sections in order. Back every row with a number, a file or a run output. An empty cell is better than an invented number. A negative result is a valid result.

**System:** <system> · **Module:** `<module under test>` · **Date:** <date> · **Mandate:** <e.g. ship fast / zero regulatory risk> · **Author:** <name>
**Assistant:** <tool, model> · **What the assistant saw:** <code only / code + requirements / …> · **Repo commit at start:** <SHA>

**Order of commits (each step its own commit):** manual set → mutant list → review criteria and prompt → generated set → mutant reports.

---

## Prediction before step 1

*Fill in before doing anything; the "Measured" column after step 6.*

| What you predict | Prediction | Measured |
| --- | --- | --- |
| How many of <N> mutants the manual set kills | <…> | <…> |
| How many of <N> mutants the generated set kills | <…> | <…> |
| Which mutant class each set is weaker in (manual / generated) | <…> | <…> |

**Biggest gap and what it means:** <…>

---

## 1. Manual baseline

*Write the manual set before you see any generated code. Use a timer.*

| Field | Value |
| --- | --- |
| Folder | `<manual set folder>` |
| Number of test functions (5-8; a parametrized test counts as one) | <…> |
| What from the theory you consciously used (e.g. a boundary test) | <… / nothing> |
| Timer: start / finish | <hh:mm> / <hh:mm> |
| Actual time, min | <…> *(exact number)* |
| All tests green on the original module | yes / no |
| Where expected values come from | <requirements source> |
| Commit of the set | <SHA> |

| ID | Test name | Rule it checks | Mutant class |
| --- | --- | --- | --- |
| M-01 | <…> | <…> | <…> |
| M-02 | <…> | <…> | <…> |

---

## 2. Mutant list

*The list is fixed by a commit before generation and before the first mutant run, and does not change afterwards. Choose 3-4 classes of defects that matter for this module, the same number of mutants per class.*

**List file:** `<mutant list file>` · **Commit / date fixed:** <SHA> / <date> · **First mutant run:** <date> *(must be later; the run must use the committed list)*

| ID | Class | What changed (original → mutant) | Place in code |
| --- | --- | --- | --- |
| <class 1>-01 | <mutant class 1> | <…> | <…> |
| <class 1>-02 | <mutant class 1> | <…> | <…> |
| … | … | … | … |

---

## 3. Review criteria and prompt

*Write before generation. Commit the criteria and the prompt before the generated set appears.*

**Commit / date criteria and prompt were fixed:** <SHA> / <date>

| Criterion | Accept | Reject |
| --- | --- | --- |
| Oracle | expected value comes from the requirements and is written into the test | expected value taken from the code's own output or constants, or from a replaced (mocked) requirements table |
| Assertion level | comparison with a concrete value | type checks, "not None", "> 0" |
| Edge case | test exactly at the boundary from the requirements, or a test that does not claim to check a boundary | test that says it checks a boundary but sits far from it |
| Independence | result does not depend on test order or the clock | current time, shared state between tests |
| Name | name states the rule being checked | `test_1`, `test_works` |
| Novelty | new input class or new check of the result (not in the manual set or already accepted tests) | same input class and same check with a different number |
| *Own criterion (optional)* | <…> | <…> |

*Exception and property tests: judge by "Assertion level" and "Novelty". A test with several asserts is judged by the rule in its name.*

**Generation prompt** (word for word, as in the prompt file):

```
<prompt text>
```

**Files:** `<criteria file>`, `<prompt file>`

---

## 4. Generation and coverage

| Field | Value |
| --- | --- |
| Generation command | `<command>` |
| Model | <…> |
| Machine time for generation, min | <…> |
| Generation cost, USD | <…> |
| Test functions generated | <…> |
| Generated set green on the original module | yes / no (red tests: <…>) |

| Set | Command | Line coverage of `<module under test>` |
| --- | --- | --- |
| Manual | `<coverage command>` | <…> % |
| Generated | `<coverage command>` | <…> % |

---

## 5. Generation Review Log

*One entry per generated test, accepted ones too. A parametrized test is one entry. If a test was rewritten, `minutes` has two parts: review + rewrite. Rewritten tests go to a separate folder with ids R-01, R-02, …; do not edit the generated file.*

```
id: G-01
verdict: accepted / rejected
criterion: <criterion from section 3, or ->
reason: <what exactly the test checks or does not check>
action: <accepted as is / rejected / rewritten by hand as R-…>
minutes: <review> + <rewrite>
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

*The same committed mutant list for all three sets.*

| Set | Mutant run command | Report |
| --- | --- | --- |
| Manual | `<mutation run command>` | `<report file>` |
| Generated | `<mutation run command>` | `<report file>` |
| Combined | `<mutation run command>` | `<report file>` |

| Mutant class | Manual | Generated | Combined |
| --- | --- | --- | --- |
| <mutant class 1> | _/_ | _/_ | _/_ |
| <mutant class 2> | _/_ | _/_ | _/_ |
| <mutant class 3> | _/_ | _/_ | _/_ |
| <mutant class 4> | _/_ | _/_ | _/_ |
| **Total of <N>** | **__** | **__** | **__** |
| **Mutation score** | **__ %** | **__ %** | **__ %** |
| Line coverage (from section 4) | __ % | __ % | - |

**Surviving mutants (IDs):** manual <…> · generated <…> · combined <…>

**One sentence about the surviving class:** <which class survived, in which set and why>

**Class where the assistant is stronger than me:** <…>

---

## 7. Cost in two currencies

| Row | Manual set | Generated set |
| --- | --- | --- |
| Human time writing, min | <…> | 0 |
| Machine time generating, min | - | <…> |
| Generation cost, USD | - | <…> |
| Human time reviewing and selecting, min | 0 | <…> |
| Human time rewriting rejected tests, min | 0 | <…> |
| **Total human minutes** | **<…>** | **<…>** |
| Mutants killed of <N> | <…> | <…> |

**What follows from this (one sentence):** <…>

---

## 8. AI Adoption Impact Report

*Seven rows in three blocks. The main number is the mutation score with its breakdown; time comes second and always next to review time.*

### Block 1. What we measured

| Row | Content |
| --- | --- |
| 1. What we measured on | one module `<module under test>`, one list of <N> mutants (commit <date>), both sets on a fresh clone <SHA>; assistant <model> saw <what exactly> |
| 2. The number | mutation score: manual <…> % · generated <…> % · combined <…> %; breakdown by class in section 6; share of rejected generated tests <…> % |

### Block 2. Where it does not work and what it costs

| Row | Content |
| --- | --- |
| 3. Where it does not work | <mutant class the assistant misses, and in which set; a class, not a list> |
| 4. Cost | <…> human min (manual) vs <…> human min (generated, with review and rewrite), plus <…> machine min and $<…> |

### Block 3. Decision

| Row | Content |
| --- | --- |
| 5. What we do about it | <assistant's role: what it writes, what a human writes> |
| 6. Mandate | under <current mandate>: <…>; under <stricter mandate>: <…> |
| 7. When we review this | <at least two events: model change, module change, requirements given to the assistant, …> |

**Answer to the decision maker in one sentence:** <…>

---

## 9. Residual risk

*What this method does not catch in your measurement.*

| Not covered | What will happen | Why we live with it now | Defer or accept |
| --- | --- | --- | --- |
| <…> | <…> | <…> | <…> |

---

## 10. AI declaration and reproducibility

**AI declaration:** where exactly I used AI: <…> · what I rejected from its output: <link to section 5> · other: <…>

**Reproducible on a fresh clone** after installing dependencies:

| Check on a fresh clone | Command | Passes |
| --- | --- | --- |
| Manual set | `<test command>` | yes / no |
| Generated set | `<test command>` | yes / no |
| Mutant run from the committed list | `<mutation run command>` | yes / no |
