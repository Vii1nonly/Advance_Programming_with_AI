# Assignment 03 — CHANGES

**Name:** Lin Khant Pyae  **Student ID:** 6705140055

This is the written part of your submission. Explain **what you changed and why**, then record your **prompt log**. Keep before/after snippets to a line or two.

---

## 1 · What I changed

One row per change. Name the OOP concept and say how you checked the behaviour was unchanged.

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Products stored as bare tuples, read by position: `PRODUCTS[pi][1]` | `Product` class with `name`, `price`, `category`; the catalogue is named objects (`LAPTOP`, `PEN`, …) | Classes (Week 2) | Ran `python Assignment_03.py` → PASS |
| 2 | Orders were nested tuples whose items pointed at products by list index: `("Alice", "gold", [(0, 1), …])` | `Order` has-a `Customer` and has-many `OrderItem`; each `OrderItem` has-a `Product` | Composition / has-a (Week 5) | PASS; checked every index mapped to the right product (e.g. `(5, 2)` → `OrderItem(MONITOR, 2)`) |
| 3 | Two repeated `if t == "none" / "silver" / …` chains, one for the discount and one for points | `Customer` base class + `SilverCustomer`, `GoldCustomer`, `PlatinumCustomer` subclasses that override `small_order_rate`, `large_order_rate`, `points_multiplier`; `Order` just calls `customer.discount_rate(subtotal)` | Inheritance & polymorphism (Week 4) | PASS; all four tiers appear in the test data, so every subclass is exercised |
| 4 | `calc()` did the maths **and** printed the receipt **and** returned the total | Pure methods `subtotal()`, `discount()`, `tax()`, `total()`, `points()` return numbers; `receipt()` only lays out text; `refactored_main()` is the only place that prints | Pure functions vs modifiers; interface vs implementation (Week 5) | PASS; also called every calculation method with stdout captured → printed nothing |
| 5 | No checks at all on the data (a quantity of 0 or a negative price would be accepted) | Constructors validate: non-empty names, price ≥ 0, known category, quantity is a whole number ≥ 1, `Order` needs a `Customer` and at least one `OrderItem` | Encapsulation & validation (Week 3) | PASS (real data still accepted); tried 9 kinds of bad input — each raised `ValueError`/`TypeError` |
| 6 | Magic numbers `0.07`, `100`, `10`, `0.03`, `10`, `"-" * 40`; lowercase `foodtax`; an unnecessary `global TAXRATE` | Named constants (`STANDARD_TAX_RATE`, `FOOD_TAX_RATE`, `DISCOUNT_THRESHOLD`, `BULK_QTY_THRESHOLD`, `BULK_DISCOUNT_RATE`, `POINTS_DIVISOR`, `RECEIPT_RULE`); no `global` | Clean code | PASS |
| 7 | `if cat == "food": … else: …` inside the totals loop (stretch F) | `Product.tax_rate()` looks up `TAX_RATE_BY_CATEGORY`; `OrderItem.tax()` uses it, so the totals have no category `if` | Polymorphic behaviour / encapsulation | PASS |
| 8 | Receipt lines built with `+` and `str()` (stretch G) | `__str__` on `OrderItem` (`Laptop x1 = 1200.0`) and `Customer` (`Alice (gold)`); one `money()` helper keeps the legacy `str(round(x, 2))` format | `__str__` / DRY | PASS |

## 2 · Short reflection (4–6 sentences)

Which change improved the code the most, and why? Where did keeping the behaviour identical force you to be careful?

> Replacing the two `if tier == ...` chains with a `Customer` class family improved the code the most, because each tier's discount rates and points multiplier now live together in one small class, and adding a new tier would mean adding one class instead of editing two chains. Keeping the behaviour identical forced me to copy the rules exactly rather than "tidy" them: the bulk discount uses `>= 10`, and Charlie has exactly 10 items, so writing `> 10` would have changed his discount from 124.2 to 103.5. I also had to keep the legacy number format `str(round(x, 2))` — a nicer `f"{x:.2f}"` would print `1645.00` instead of `1645.0` and fail the self-test. The tier name "none" had to stay exactly as the original prints it in the receipt header. Because the test data never has a subtotal of exactly 100, the self-test alone could not catch a `>=` vs `>` mistake there, so I checked that edge case separately.

---

## 3 · Prompt log (Level 2 — required)

Record **every** prompt where AI helped. If you wrote a part yourself, say so in one row. AI-shaped code with an empty log does **not** meet the Level-2 policy.

AI tool used: Claude (Claude Code, model Claude Opus 5).

| # | My prompt to the AI | What it suggested (summary) | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | "this is an assignment files, I want you to deeply analyze this and tell me what excatly are in it and what are the things need to be fix" | An analysis: what each section of the file does, the code smells mapped to tasks A–G, and output traps (bulk rule is `>= 10` and Charlie has exactly 10 items; `f"{x:.2f}"` breaks the format; prices must stay floats; tier name must stay `"none"`) | Accepted | Compared its points with the TARGET output printed by `python Assignment_03.py` |
| 2 | "I want you to continue to do the assignment, if you can, i will provide any information you want, also after doing an assignment I want you to create a folder in download folder just for two of these files" | Wrote the full refactor (`Product`, `OrderItem`, `Customer` + 3 tier subclasses, `Order`, `receipt()`, named constants, `build_orders()`, `refactored_main()`) and drafted this CHANGES.md | Accepted | Self-test PASS; validation tested with 9 bad inputs; confirmed calculation methods print nothing; confirmed the legacy and self-test sections were not edited |
| 3 |  |  |  |  |

**Ownership statement.** *By submitting, I confirm I understand and can explain every line of code I submitted, and that this prompt log reflects my actual AI use.*

---

## 4 · Before-you-submit checklist

- [x] `python Assignment_03.py` prints **PASS**.
- [x] No tuples / parallel lists left — products, orders, and items are objects.
- [x] No `if tier == ...` chains — tiers are a class family.
- [x] Calculation methods **return** values and do not `print`; printing is separate.
- [x] Constructors validate state; no leftover `global`; magic numbers are named.
- [x] The change table and reflection above are filled in.
- [ ] The prompt log is complete and the ownership statement is signed.
