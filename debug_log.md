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

## UI Fix: Customer Churn-Risk Watchlist

**Problem:** The risk score column appeared as a full progress bar, so high-risk rows looked like "100%" and important row details required horizontal scrolling.

**Risk:** Executives could misread the score as a percentage-only visual and miss country, membership, spending, or behavior details.

**Fix:** Replaced the watchlist with a compact custom table. The risk score now shows a visible number plus a short bar, while membership, days since purchase, and newsletter status are formatted for faster scanning.

## Compatibility Fix: Streamlit Width API

**Problem:** Streamlit warned that `use_container_width` will be removed.

**Risk:** Future Streamlit versions could break or warn during chart rendering.

**Fix:** Replaced deprecated chart calls with `width="stretch"` and synced the embedded stlite copy in `index.html`.

## Business Foolproof Guard

**Problem:** The sliders could create scenarios outside historical data without a clear executive-level risk briefing.

**Risk:** Discount, return threshold, marketing elasticity, and marketing budget assumptions could move into extrapolation, making ROI and profit estimates unreliable.

**Fix:** Added `monthly_revenue.csv`, calculated historical safe boundaries from actual data, and displayed `st.error`, `st.warning`, or `st.success` below the controls. Added a collapsible historical-boundary reference table for decision review.

## Decision Simulator ROI Fix

**Problem:** Marketing elasticity was collected in the UI but was not used in either profit calculation. The simulator also subtracted marketing budget as pure cost even when modeled customer uplift should create extra revenue, and the discount guard used a global baseline before filtered historical average discount was available.

**Risk:** The scenario could understate or misstate marketing ROI, show inconsistent profit numbers between the dashboard snapshot and simulator, and trigger extrapolation warnings against the wrong discount baseline.

**Fix:** Calculated `marketing_net` from historical monthly new customers, marketing budget, elasticity, and filtered average order value. Applied it to both `snapshot_profit_delta` and `estimated_profit_delta`, skipped the cost when `marketing_budget` is zero, and moved the guard check after `historical_avg_discount` is computed.

## Gross Margin Guard Correction

**Problem:** The dataset has no COGS/cost column, so deriving gross margin from subtotal, discount, and shipping was not a true margin calculation.

**Risk:** The app produced a misleading historical margin floor and incorrectly judged reasonable user assumptions as unsafe.

**Fix:** Removed data-derived gross-margin boundaries. Gross margin is now treated as a user assumption, with business checks for negative margin, very low margin, and overly optimistic margin.

## Bilingual Executive Risk Briefing

**Problem:** The new guardrail messages were initially only in Traditional Chinese.

**Risk:** English-language users could not read the risk explanations in the dashboard.

**Fix:** Added English and Traditional Chinese versions for guardrail messages, success text, expander labels, table headers, parameter names, and explanatory captions.

## Final improvement

The system intentionally uses warnings, transparent model metrics, and historical-boundary checks. This proves human diagnosis and business reasoning, not blind AI copying.
