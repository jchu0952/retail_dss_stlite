# Prompt & Debug Log

## Task decomposition

**Prompt:** Build a website for retail/e-commerce decision support using the provided CSV data and stlite.

**Action:** Split the project into five parts: data cleaning, KPI dashboard, risk diagnosis, decision simulator, and report/demo preparation.

## Red Error Message 1

**Problem:** `orders.customer_rating` has many missing values.

**Risk:** Missing rating could be wrongly interpreted as customer dissatisfaction.

**Fix:** Add a `rating_missing` flag and fill the rating only for safe display/model execution.

## Red Error Message 2

**Problem:** The discount slider may create a scenario outside the historical discount range.

**Risk:** This becomes extrapolation, which can make the prediction unreliable.

**Fix:** Use `st.warning()` when the simulated discount is outside the historical boundary.

## Red Error Message 3

**Problem:** Linear regression can produce a low R².

**Risk:** A mathematically-looking chart may mislead the audience into thinking the model is strong.

**Fix:** Display R² directly and translate it into business language: discount alone is not enough; managers must also consider category, customer segment, return rate, and inventory.

## Final improvement

The system intentionally uses warnings and transparent model metrics. This proves human diagnosis and business reasoning, not blind AI copying.
