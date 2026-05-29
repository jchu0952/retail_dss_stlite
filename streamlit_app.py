import streamlit as st
import pandas as pd
import numpy as np
from html import escape

st.set_page_config(
    page_title="Retail AI Decision Support System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1180px;
}

.sticky-title {
    position: sticky;
    top: 0;
    z-index: 1000;
    background: #ffffff;
    box-sizing: border-box;
    padding: 1.1rem 0 0.9rem;
    margin: 0 0 1.4rem 0;
    border-bottom: 1px solid #e5e7eb;
    box-shadow: 0 8px 18px rgba(15, 23, 42, 0.04);
}

.app-header {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    margin: 0 0 0.45rem 0;
}

.app-icon {
    font-size: 1.65rem;
    line-height: 1;
    flex: 0 0 auto;
}

.big-title {
    display: block;
    color: #1f2937;
    font-size: clamp(1.35rem, 2.4vw, 1.95rem);
    font-weight: 750;
    line-height: 1.25;
    margin: 0;
    padding: 0;
    white-space: normal;
}

.subtitle {
    color: #64748b;
    font-size: 0.95rem;
    line-height: 1.45;
    margin: 0;
}
.card {border: 1px solid #e5e7eb; border-radius: 14px; padding: 1rem; background: #ffffff;}
.risk-box {border-left: 6px solid #ef4444; background: #fff7f7; padding: 0.8rem 1rem; border-radius: 8px;}
.ok-box {border-left: 6px solid #22c55e; background: #f0fdf4; padding: 0.8rem 1rem; border-radius: 8px;}
.small-note {font-size: 0.85rem; color: #64748b;}
.chart-shell {border: 1px solid #e5e7eb; border-radius: 8px; padding: 0.9rem; background: #ffffff;}
.line-chart-svg {display: block; width: 100%; height: auto;}
.chart-axis {stroke: #cbd5e1; stroke-width: 1;}
.chart-grid {stroke: #e2e8f0; stroke-width: 1;}
.chart-line {fill: none; stroke: #2563eb; stroke-width: 3; stroke-linecap: round; stroke-linejoin: round;}
.chart-dot {fill: #2563eb; stroke: #ffffff; stroke-width: 2;}
.chart-hit {fill: transparent; cursor: crosshair;}
.chart-point:hover .chart-dot {fill: #0f766e; r: 6;}
.chart-tooltip {opacity: 0; transition: opacity 120ms ease; pointer-events: none;}
.chart-point:hover .chart-tooltip {opacity: 1;}
.tooltip-box {fill: #111827; rx: 6;}
.tooltip-text {fill: #ffffff; font-size: 12px; font-weight: 650;}
.chart-label {fill: #64748b; font-size: 12px;}
.bar-list {display: grid; gap: 0.55rem;}
.bar-row {display: grid; grid-template-columns: minmax(8rem, 1fr) minmax(9rem, 2fr) auto; gap: 0.7rem; align-items: center;}
.bar-label {font-size: 0.85rem; color: #334155; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;}
.bar-track {height: 0.7rem; background: #e2e8f0; border-radius: 999px; overflow: hidden;}
.bar-fill {height: 100%; background: #0f766e; border-radius: 999px;}
.bar-value {font-size: 0.82rem; color: #475569; font-variant-numeric: tabular-nums;}
.kpi-primary-grid {display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1.2rem; margin: 1rem 0 1.5rem;}
.kpi-secondary-grid {display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.85rem; margin: 0 0 1.5rem;}
.kpi-tile {border: 1px solid #e5e7eb; border-radius: 10px; padding: 1.1rem; background: #ffffff; transition: all 200ms ease;}
.kpi-tile.primary {border: 2px solid #e5e7eb; border-left: 6px solid #334155; padding: 1.4rem; min-height: 7.5rem; background: linear-gradient(135deg, #ffffff 0%, #fafafa 100%);}
.kpi-tile.primary.ok {border-left-color: #0f766e; background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);}
.kpi-tile.primary.warn {border-left-color: #ca8a04; background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);}
.kpi-tile.primary.danger {border-left-color: #dc2626; background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);}
.kpi-tile.secondary {border-top: 4px solid #334155; padding: 0.9rem;}
.kpi-tile.secondary.ok {border-top-color: #0f766e;}
.kpi-tile.secondary.warn {border-top-color: #ca8a04;}
.kpi-tile.secondary.danger {border-top-color: #dc2626;}
.kpi-label {font-size: 0.78rem; color: #64748b; margin-bottom: 0.4rem; text-transform: uppercase; letter-spacing: 0.5px; font-weight: 700;}
.kpi-tile.primary .kpi-label {font-size: 0.82rem; color: #475569; margin-bottom: 0.6rem;}
.kpi-value {font-size: clamp(1.35rem, 2.4vw, 2rem); line-height: 1.1; font-weight: 720; color: #111827; font-variant-numeric: tabular-nums;}
.kpi-tile.primary .kpi-value {font-size: clamp(1.8rem, 3.5vw, 2.4rem); font-weight: 750; line-height: 1.05;}
.snapshot-title {font-size: 1.05rem; font-weight: 800; color: #111827; margin: 0.6rem 0 1rem; letter-spacing: -0.3px;}
.signal-grid {display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 1rem; margin: 1rem 0 1.5rem;}
.signal-card {border: 1px solid #e5e7eb; border-left: 6px solid #e5e7eb; border-radius: 10px; padding: 1.1rem 1.25rem; background: #ffffff; min-height: 8rem; display: flex; flex-direction: column; justify-content: space-between; transition: all 200ms ease;}
.signal-card:hover {box-shadow: 0 4px 12px rgba(15, 23, 42, 0.08);}
.signal-card.ok {background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%); border-left-color: #16a34a; border-color: #86efac;}
.signal-card.warn {background: linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%); border-left-color: #ca8a04; border-color: #fde68a;}
.signal-card.danger {background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%); border-left-color: #dc2626; border-color: #fca5a5;}
.signal-label {display: flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; color: #64748b; margin-bottom: 0.5rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.5px;}
.signal-dot {width: 0.65rem; height: 0.65rem; border-radius: 999px; background: #334155; flex: 0 0 auto;}
.signal-card.ok .signal-dot {background: #16a34a;}
.signal-card.warn .signal-dot {background: #ca8a04;}
.signal-card.danger .signal-dot {background: #dc2626;}
.signal-value {font-size: 1.35rem; line-height: 1.2; font-weight: 760; color: #111827; margin-bottom: 0.5rem; font-variant-numeric: tabular-nums;}
.signal-note {font-size: 0.84rem; line-height: 1.4; color: #475569;}
.decision-focus {border: 1px solid #e5e7eb; border-left: 8px solid #0f766e; border-radius: 8px; padding: 1rem; background: #ffffff; margin: 0.5rem 0 1rem;}
.decision-focus.danger {border-left-color: #dc2626; background: #fef2f2;}
.decision-focus.warn {border-left-color: #ca8a04; background: #fffbeb;}
.decision-kicker {font-size: 0.78rem; color: #64748b; margin-bottom: 0.35rem;}
.decision-main {font-size: clamp(1.6rem, 3vw, 2.45rem); font-weight: 780; line-height: 1.05; color: #111827; font-variant-numeric: tabular-nums;}
.decision-note {font-size: 0.95rem; color: #334155; margin-top: 0.5rem; line-height: 1.4;}
.detail-muted {font-size: 0.86rem; color: #64748b; line-height: 1.45;}
.dm-card {border: 1px solid #e5e7eb; border-radius: 8px; background: #ffffff; margin: 0.85rem 0 1.25rem; overflow: hidden;}
.dm-title {padding: 0.85rem 1rem; font-size: 0.98rem; font-weight: 760; color: #111827; border-bottom: 1px solid #e5e7eb;}
.dm-scroll {overflow-x: auto;}
.dm-table {width: 100%; border-collapse: collapse; table-layout: fixed;}
.dm-table th {position: sticky; top: 0; z-index: 1; background: #f8fafc; color: #64748b; font-size: 0.68rem; line-height: 1.2; font-weight: 780; letter-spacing: 0; text-transform: uppercase; padding: 0.68rem 0.75rem; border-bottom: 1px solid #e5e7eb; text-align: left;}
.dm-table td {padding: 0.72rem 0.75rem; border-bottom: 1px solid #eef2f7; color: #334155; font-size: 0.86rem; line-height: 1.35; vertical-align: middle; overflow: hidden; text-overflow: ellipsis; white-space: nowrap;}
.dm-table tr:hover td {background: #f8fafc;}
.dm-table tr:last-child td {border-bottom: 0;}
.dm-table .num {text-align: right; font-variant-numeric: tabular-nums;}
.dm-table .money {color: #047857; font-weight: 760; font-variant-numeric: tabular-nums;}
.dm-table .product {font-weight: 650; color: #111827;}
.dm-rank {display: inline-flex; align-items: center; justify-content: center; width: 1.6rem; height: 1.6rem; border-radius: 999px; background: #f1f5f9; color: #334155; font-size: 0.78rem; font-weight: 760;}
.badge {display: inline-flex; align-items: center; max-width: 100%; border-radius: 999px; padding: 0.16rem 0.52rem; font-size: 0.74rem; line-height: 1.25; font-weight: 760; border: 1px solid transparent; white-space: nowrap;}
.badge-cat {color: #0f766e; background: #ecfdf5; border-color: #a7f3d0;}
.badge-tier-free, .badge-tier-basic {color: #475569; background: #f1f5f9; border-color: #cbd5e1;}
.badge-tier-silver {color: #475569; background: #f8fafc; border-color: #94a3b8;}
.badge-tier-gold {color: #92400e; background: #fef3c7; border-color: #fcd34d;}
.badge-tier-platinum, .badge-tier-premium {color: #075985; background: #e0f2fe; border-color: #7dd3fc;}
.return-cell {display: grid; grid-template-columns: minmax(3rem, auto) 1fr; gap: 0.55rem; align-items: center; font-variant-numeric: tabular-nums;}
.return-track {height: 0.45rem; background: #e5e7eb; border-radius: 999px; overflow: hidden;}
.return-fill {height: 100%; border-radius: 999px; background: #0f766e;}
.return-fill.warn {background: #ca8a04;}
.return-fill.danger {background: #dc2626;}
.risk-score {display: grid; grid-template-columns: 2.2rem 1fr; gap: 0.55rem; align-items: center; font-variant-numeric: tabular-nums;}
.risk-track {height: 0.45rem; background: #e5e7eb; border-radius: 999px; overflow: hidden;}
.risk-fill {display: block; height: 100%; border-radius: 999px; background: #16a34a;}
.risk-fill.warn {background: #ca8a04;}
.risk-fill.danger {background: #dc2626;}
.risk-dot {display: inline-block; width: 0.58rem; height: 0.58rem; margin-right: 0.42rem; border-radius: 999px; background: #16a34a; vertical-align: middle;}
.risk-dot.warn {background: #ca8a04;}
.risk-dot.danger {background: #dc2626;}
.section-divider {display: flex; align-items: center; gap: 0.7rem; margin: 1.25rem 0 0.35rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;}
.section-label {font-size: 1rem; line-height: 1.25; font-weight: 780; color: #111827;}
.count-badge {display: inline-flex; align-items: center; justify-content: center; min-width: 1.75rem; height: 1.5rem; padding: 0 0.55rem; border-radius: 999px; background: #eff6ff; color: #1d4ed8; font-size: 0.78rem; font-weight: 780; font-variant-numeric: tabular-nums;}
@media (max-width: 1000px) {
    .kpi-primary-grid {grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 1rem;}
    .kpi-secondary-grid {grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.75rem;}
    .signal-grid {grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 0.9rem;}
}
@media (max-width: 640px) {
    .kpi-primary-grid {grid-template-columns: 1fr; gap: 0.9rem;}
    .kpi-secondary-grid {grid-template-columns: 1fr; gap: 0.7rem;}
    .signal-grid {grid-template-columns: 1fr; gap: 0.8rem;}
    .kpi-tile.primary {padding: 1.2rem;}
    .signal-card {padding: 0.95rem 1.1rem;}
}
</style>
""", unsafe_allow_html=True)

DATA_DIR = "data"

@st.cache_data(show_spinner=False)
def load_data():
    customers = pd.read_csv(f"{DATA_DIR}/customers.csv")
    orders = pd.read_csv(f"{DATA_DIR}/orders.csv")
    monthly_revenue = pd.read_csv(f"{DATA_DIR}/monthly_revenue.csv")
    products = pd.read_csv(f"{DATA_DIR}/product_summary.csv")

    customers["registration_date"] = pd.to_datetime(customers["registration_date"], errors="coerce")
    orders["order_date"] = pd.to_datetime(orders["order_date"], errors="coerce")
    orders["delivery_date"] = pd.to_datetime(orders["delivery_date"], errors="coerce")
    monthly_revenue["order_date"] = pd.to_datetime(
        monthly_revenue["year"].astype(str) + "-" + monthly_revenue["month"].astype(str).str.zfill(2) + "-01",
        errors="coerce",
    )

    # Data cleaning / landmine removal
    customers = customers.drop_duplicates(subset=["customer_id"]).copy()
    orders = orders.drop_duplicates(subset=["order_id"]).copy()
    orders = orders.dropna(subset=["order_id", "customer_id", "order_date", "total_amount_usd", "category"])

    # Missing ratings are normal for orders without review. Keep a flag and fill only for display/model safety.
    orders["rating_missing"] = orders["customer_rating"].isna().astype(int)
    orders["customer_rating"] = orders["customer_rating"].fillna(orders["customer_rating"].median())

    # Basic sanity guardrails
    orders = orders[(orders["total_amount_usd"] >= 0) & (orders["quantity"] > 0)]
    orders["month_period"] = orders["order_date"].dt.to_period("M").astype(str)

    merged = orders.merge(
        customers[[
            "customer_id", "country", "age", "gender", "membership_tier", "preferred_device",
            "acquisition_channel", "days_since_last_purchase", "total_spend_usd", "returns_made", "churned"
        ]],
        on="customer_id",
        how="left",
    )

    return customers, orders, monthly_revenue, products, merged

customers, orders, monthly_revenue, products, merged = load_data()

def quantile_or_zero(series, q):
    clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return 0.0 if clean.empty else float(clean.quantile(q))

def mean_or_zero(series):
    clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    return 0.0 if clean.empty else float(clean.mean())

def rate_series_to_percent(series):
    clean = pd.to_numeric(series, errors="coerce").replace([np.inf, -np.inf], np.nan).dropna()
    if clean.empty:
        return clean
    return clean * 100 if clean.max() <= 1 else clean

def calculate_historical_bounds(orders_df, monthly_df):
    return_rate_pct = rate_series_to_percent(monthly_df["return_rate"])
    monthly_avg_discounts = orders_df.groupby(
        orders_df["order_date"].dt.to_period("M")
    )["discount_pct"].mean()

    return {
        "discount_min": quantile_or_zero(monthly_avg_discounts, 0.05),
        "discount_max": quantile_or_zero(monthly_avg_discounts, 0.95),
        "return_min": quantile_or_zero(return_rate_pct, 0.05),
        "return_max": quantile_or_zero(return_rate_pct, 0.95),
        "elasticity_safe_max": 10.0,
        "budget_safe_max": mean_or_zero(monthly_df["revenue_usd"]) * 0.15,
    }

HISTORICAL_BOUNDS = calculate_historical_bounds(orders, monthly_revenue)
DISCOUNT_MIN = HISTORICAL_BOUNDS["discount_min"]
DISCOUNT_MAX = HISTORICAL_BOUNDS["discount_max"]
RETURN_MIN = HISTORICAL_BOUNDS["return_min"]
RETURN_MAX = HISTORICAL_BOUNDS["return_max"]
ELASTICITY_SAFE_MAX = HISTORICAL_BOUNDS["elasticity_safe_max"]
BUDGET_SAFE_MAX = HISTORICAL_BOUNDS["budget_safe_max"]

def check_extrapolation(discount, margin, return_threshold, elasticity, budget):
    warnings_list = []
    errors_list = []

    if discount > DISCOUNT_MAX:
        errors_list.append(
            t("guard_discount_error").format(
                discount=discount,
                discount_max=DISCOUNT_MAX,
            )
        )

    if margin < 0:
        errors_list.append(t("guard_margin_negative_error"))
    elif margin < 10:
        warnings_list.append(t("guard_margin_low_warning"))
    elif margin > 80:
        warnings_list.append(t("guard_margin_high_warning"))

    if return_threshold > RETURN_MAX:
        warnings_list.append(
            t("guard_return_threshold_warning").format(
                return_threshold=return_threshold,
                return_max=RETURN_MAX,
            )
        )

    if elasticity > ELASTICITY_SAFE_MAX:
        warnings_list.append(
            t("guard_elasticity_warning").format(
                elasticity=elasticity,
                elasticity_safe_max=ELASTICITY_SAFE_MAX,
            )
        )

    if budget > BUDGET_SAFE_MAX:
        errors_list.append(
            t("guard_budget_error").format(
                budget=budget,
                budget_safe_max=BUDGET_SAFE_MAX,
            )
        )

    return warnings_list, errors_list

# ---------- Language ----------
TEXT = {
    "English": {
        "all": "All",
        "sidebar_title": "⚙️ Decision Controls",
        "sidebar_caption": "Use filters first, then test the decision slider.",
        "category_filter": "1) Category filter",
        "country_filter": "2) Country filter",
        "tier_filter": "3) Membership filter",
        "start_date_filter": "4) Start date",
        "end_date_filter": "5) End date",
        "date_range_swapped": "Start date is after end date, so the app uses the earlier date as the start.",
        "extra_discount": "Decision simulation: extra marketing discount (%)",
        "gross_margin": "Gross margin assumption (%)",
        "marketing_budget": "Extra marketing budget (USD)",
        "marketing_elasticity": "Marketing elasticity assumption (%)",
        "return_threshold": "Product return warning threshold (%)",
        "guard_discount_error": "⚠️ Discount rate {discount:.1f}% is above the historical safe ceiling ({discount_max:.1f}%). This scenario has not occurred in actual operations, so the forecast should not be treated as decision-grade. Executive review is recommended before acting on it.",
        "guard_margin_negative_error": "⚠️ Gross margin is negative. Each order would directly lose money under this assumption. Please reset the margin before using this scenario.",
        "guard_margin_low_warning": "📋 Gross margin is below 10%, which represents an extremely low-profit scenario. Please confirm whether this assumption reflects actual operating conditions.",
        "guard_margin_high_warning": "📋 Gross margin is above 80%, which is materially optimistic. Please confirm that all relevant cost items have been included.",
        "guard_return_threshold_warning": "📋 Return warning threshold {return_threshold:.1f}% is above the historical 95th percentile ({return_max:.1f}%). This threshold is too loose and may fail to identify high-return products. Consider moving it back into a reasonable range.",
        "guard_elasticity_warning": "📋 Marketing elasticity assumption {elasticity:.1f}% exceeds the reasonable scenario ceiling ({elasticity_safe_max:.1f}%). This assumption is not supported by historical data; ROI should be treated as an optimistic projection, not as a direct budget request basis.",
        "guard_budget_error": "⚠️ Marketing budget ${budget:,.0f} is above 15% of historical average monthly revenue (safe ceiling ${budget_safe_max:,.0f}). This scale of spend has no matching case in the historical data, so forecast uncertainty is high. Risk committee review is recommended.",
        "guard_success": "✅ All parameters passed the historical-boundary and business-assumption checks. The forecast can be used as decision-support input.",
        "guard_bounds_expander": "📊 Historical data safe-boundary reference",
        "guard_bounds_col_param": "Parameter",
        "guard_bounds_col_lower": "Historical safe lower bound",
        "guard_bounds_col_upper": "Historical safe upper bound",
        "guard_param_discount": "Discount rate",
        "guard_param_return_threshold": "Return threshold",
        "guard_param_marketing_elasticity": "Marketing elasticity",
        "guard_param_marketing_budget": "Marketing budget",
        "guard_bounds_caption": "Boundaries are calculated from the 5th–95th percentiles of historical data. Forecasts outside this range are extrapolations and have lower reliability.",
        "guard_margin_caption": "Gross margin is a user assumption. The dataset does not contain actual cost/COGS data, so no historical boundary is available for comparison.",
        "empty_filter": "No data after filtering. Please loosen the filters.",
        "app_title": "Retail AI Decision Support System",
        "app_subtitle": "Goal: turn raw e-commerce CSV data into an interactive decision crystal ball: data cleaning → business metrics → risk warning → scenario simulation.",
        "kpi_revenue": "Revenue",
        "kpi_orders": "Orders",
        "kpi_active_customers": "Active customers",
        "kpi_avg_order_value": "Average order value",
        "kpi_return_rate": "Return rate",
        "kpi_churn_rate": "Churn rate",
        "snapshot_title": "At-a-glance decision signals",
        "snapshot_top_category": "Revenue focus",
        "snapshot_top_category_note": "Largest category in the selected filters.",
        "snapshot_return_risk": "Return risk",
        "snapshot_return_risk_note": "{count} products need review at the current threshold.",
        "snapshot_return_clear": "No products exceed the current return threshold.",
        "snapshot_profit_signal": "Scenario profit",
        "snapshot_profit_positive": "Positive under current assumptions.",
        "snapshot_profit_negative": "Negative after budget and margin assumptions.",
        "snapshot_model_signal": "Model confidence",
        "snapshot_model_strong": "Useful signal",
        "snapshot_model_medium": "Use with context",
        "snapshot_model_low": "Weak signal",
        "not_available": "Not available",
        "tab_overview": "Executive Dashboard",
        "tab_product": "Risk & Product Diagnosis",
        "tab_sim": "Decision Simulator",
        "tab_data": "Data Mining Table",
        "tab_log": "AI Debug Log",
        "overview_header": "Executive dashboard",
        "monthly_revenue_trend": "Monthly revenue trend",
        "top_categories_revenue": "Top categories by revenue",
        "business_interpretation": "Business interpretation",
        "no_chart_data": "No chart data available for the current filters.",
        "chart_tooltip_revenue": "Revenue",
        "chart_tooltip_orders": "Orders",
        "overview_info": "The strongest revenue category in the selected data is **{top_category}** ({top_category_rev}). Average discount is **{avg_discount:.2f}%**, return rate is **{return_rate:.1%}**, and repeat-customer share is **{repeat_share:.1%}**. This dashboard should be used to decide where to allocate promotions, not only to display charts.",
        "product_header": "Risk and product diagnosis",
        "high_return_products": "High-return products",
        "no_high_return": "No product exceeds the selected return-risk threshold.",
        "high_return_warning": "{count} products exceed the return threshold. These items need QA, logistics, or product-page review.",
        "best_revenue_products": "Best revenue products",
        "customer_churn_watchlist": "Customer churn-risk watchlist",
        "churn_top_n": "Rows",
        "churn_risk_threshold": "Risk score ≥",
        "sim_header": "Decision simulator: discount → revenue / traffic / profit",
        "sim_caption": "This is a cautious multi-factor linear-regression scenario estimator, not a guaranteed forecast. It uses business drivers beyond discount so users can judge both prediction and risk.",
        "sim_not_enough": "Not enough monthly data after filtering to build the simulator. Please select a broader period or category.",
        "current_avg_discount": "Current avg discount",
        "simulated_avg_discount": "Simulated avg discount",
        "predicted_revenue_delta": "Predicted monthly revenue Δ",
        "predicted_orders_delta": "Predicted monthly orders Δ",
        "model_transparency": "Model transparency",
        "revenue_model_r2": "Revenue model R²",
        "revenue_slope": "Revenue slope",
        "estimated_profit_delta": "Estimated monthly profit Δ",
        "sim_focus_label": "Most important number",
        "sim_focus_positive": "Profit improves in this scenario.",
        "sim_focus_negative": "Profit falls in this scenario.",
        "sim_focus_neutral": "Scenario is close to break-even.",
        "sim_key_changes": "Key changes to notice",
        "actual_vs_predicted_revenue": "Actual vs Predicted Revenue",
        "actual_predicted_by_month": "Actual and Predicted Revenue by Month",
        "perfect_prediction": "Perfect prediction",
        "actual_revenue": "Actual Revenue",
        "predicted_revenue": "Predicted Revenue",
        "model_fit_warning": "Discount alone has weak explanatory power. The simulator uses a multi-factor model for safer decision support.",
        "multi_model_explanation": "The main simulator uses monthly order volume, unit price, quantity, returns, delivery time, discount, month, and year. This is safer than using discount alone because revenue changes usually come from several business drivers at the same time.",
        "discount_model_limitation_header": "Model Limitation: discount-only regression",
        "discount_model_limitation_body": "The discount-only R² is **{r2:.3f}**. Its predictions collapse near the average monthly revenue, which means discount alone is not learning meaningful revenue variation. Keep this model as a debug/limitation example, not as the main decision model.",
        "sim_detail_table": "Show scenario detail table",
        "simulated_discount_line": "Current simulated discount: **{simulated_discount:.2f}%**",
        "historical_max_discount_line": "Historical highest average discount: **{historical_max_discount:.2f}%**",
        "discount_safe_success": "Current discount is still within the historical data range, so the simulation is relatively more reliable.",
        "discount_external_warning": "Notice: the current simulated discount exceeds the historical data range. The model is extrapolating, so the prediction is only a reference and must not be treated as guaranteed.",
        "discount_danger_error": "High risk: the current simulated discount is clearly beyond the historical range. Model reliability drops and profit may deteriorate quickly.",
        "profit_loss_dynamic_warning": "This scenario reduces profit. Estimated profit change is {profit_change}. Consider lowering the discount or resetting the marketing budget.",
        "sim_support_revenue": "Revenue change",
        "sim_support_orders": "Order change",
        "sim_support_discount": "Discount change",
        "sim_support_marketing": "Marketing ROI",
        "sim_support_confidence": "Confidence",
        "delta_points": "pts",
        "discount_point_unit": "USD / discount point",
        "boss_language": "In boss language: within the filtered historical data, every +1 percentage point of average discount is associated with about **{slope_money}** change in monthly revenue. The R² is **{r2:.3f}**, so the tool treats this as a decision-support signal, not as an automatic answer.",
        "external_push_warning": "External-push risk: simulated discount {new_discount:.2f}% is outside historical range ({x_min:.2f}% to {x_max:.2f}%). Do not overtrust this prediction.",
        "low_explainability_warning": "Low-explainability warning: discount alone does not explain revenue well. Combine this result with category, customer segment, product return rate, and inventory strategy.",
        "profit_warning": "Profit warning: after considering the marketing budget and gross-margin assumption, this scenario may reduce profit.",
        "scenario_success": "Scenario looks financially acceptable under the current assumptions, but still verify inventory and product-return risk.",
        "scenario_current": "Current",
        "scenario_simulated": "Simulated",
        "col_scenario": "Scenario",
        "col_avg_discount": "Avg discount %",
        "col_predicted_revenue": "Predicted monthly revenue",
        "col_predicted_orders": "Predicted monthly orders",
        "data_header": "Data mining table and cleaning summary",
        "quality_dataset": "Dataset",
        "quality_rows": "Rows",
        "quality_columns": "Columns",
        "quality_missing": "Missing cells after cleaning",
        "filtered_order_data": "Filtered order-level data",
        "download_csv": "Download filtered data as CSV",
        "log_header": "AI collaboration debug log / Prompt & Debug Log",
        "log_note": "The final report should include this style of log to prove the team did not blindly copy code.",
        "col_stage": "Stage",
        "col_problem": "Problem",
        "col_fix": "Fix",
        "stage_task_decomposition": "Task decomposition",
        "problem_task_decomposition": "Raw requirement was too broad: build a website + analyze data + decision simulation.",
        "fix_task_decomposition": "Split into data cleaning, KPI dashboard, product/customer risk diagnosis, and simulator.",
        "stage_red_error_1": "Red Error 1",
        "problem_red_error_1": "customer_rating contained many missing values; charts and model summaries could misread blank reviews as zero satisfaction.",
        "fix_red_error_1": "Created rating_missing flag and filled display/model value with median only after preserving missingness.",
        "stage_red_error_2": "Red Error 2",
        "problem_red_error_2": "Discount slider can push values outside historical range, producing external-push prediction risk.",
        "fix_red_error_2": "Added st.warning when simulated discount is outside the observed historical range.",
        "stage_table_ui_fix": "Watchlist table UX",
        "problem_table_ui_fix": "The churn-risk watchlist used a progress column for risk score, so high scores looked like a full 100% bar and pushed row details into horizontal scrolling.",
        "fix_table_ui_fix": "Replaced that watchlist with a compact custom table: the risk score now shows a visible number plus a small bar, with membership, days, and newsletter values formatted for scanning.",
        "stage_streamlit_api_fix": "Streamlit API update",
        "problem_streamlit_api_fix": "Streamlit warned that use_container_width will be removed, which could break chart rendering after the deprecation deadline.",
        "fix_streamlit_api_fix": "Updated Plotly charts to use width='stretch' and synced the embedded stlite version.",
        "stage_business_guard": "Business foolproof guard",
        "problem_business_guard": "Decision sliders could create unrealistic scenarios without a C-level risk warning, especially marketing budget above historical monthly revenue scale.",
        "fix_business_guard": "Loaded monthly_revenue.csv, calculated safe historical boundaries, and added st.error/st.warning/st.success messages plus a reference expander for executives.",
        "stage_simulator_roi_fix": "Decision simulator ROI fix",
        "problem_simulator_roi_fix": "Marketing elasticity was collected but not used in either profit calculation. The simulator also subtracted marketing budget even when the campaign produced modeled customer uplift, and the guard checked discount against the wrong baseline before filtered historical discount was available.",
        "fix_simulator_roi_fix": "Calculated marketing_net from monthly new-customer baseline, marketing budget, elasticity, and filtered average order value. Applied it to both snapshot and simulator profit deltas, skipped the cost when budget is zero, and moved extrapolation checks after filtered historical_avg_discount is calculated.",
        "stage_margin_guard_fix": "Gross margin assumption fix",
        "problem_margin_guard_fix": "The app originally tried to infer gross margin from subtotal, discount, and shipping even though the dataset has no COGS/cost column, producing a misleading historical floor.",
        "fix_margin_guard_fix": "Removed historical margin bounds entirely and treated gross margin as a user assumption with business sanity checks for negative, low, or overly optimistic margins.",
        "stage_bilingual_guard": "Bilingual risk briefing",
        "problem_bilingual_guard": "The new business guardrail messages were initially hardcoded in Traditional Chinese, so English users could not read the executive risk briefings.",
        "fix_bilingual_guard": "Moved all guardrail messages, success text, expander labels, and captions into the existing language dictionary for English and Traditional Chinese.",
        "stage_business_diagnosis": "Business diagnosis",
        "problem_business_diagnosis": "A low R² model can look mathematical but still be weak for strategy.",
        "fix_business_diagnosis": "Show R² visibly and translate the result into high-level business language with warnings.",
        "demo_script": """
**Recommended 30-second demo script**  
1. Start from Executive Dashboard and identify the highest-revenue category.  
2. Go to Risk & Product Diagnosis and show whether top revenue products also have high return risk.  
3. Go to Decision Simulator, move the discount slider, and explain R², slope, profit change, and warnings.  
4. Conclude: data does not make the decision; it makes risks visible before the decision.
""",
    },
    "繁體中文": {
        "all": "全部",
        "sidebar_title": "⚙️ 決策控制",
        "sidebar_caption": "先設定篩選條件，再測試決策模擬滑桿。",
        "category_filter": "1) 商品類別篩選",
        "country_filter": "2) 國家篩選",
        "tier_filter": "3) 會員等級篩選",
        "start_date_filter": "4) 開始日期",
        "end_date_filter": "5) 結束日期",
        "date_range_swapped": "開始日期晚於結束日期，系統已用較早日期作為開始日期。",
        "extra_discount": "決策模擬：額外行銷折扣 (%)",
        "gross_margin": "毛利率假設 (%)",
        "marketing_budget": "額外行銷預算 (USD)",
        "marketing_elasticity": "行銷彈性假設 (%)",
        "return_threshold": "商品退貨警示門檻 (%)",
        "guard_discount_error": "⚠️ 折扣率 {discount:.1f}% 已超出歷史最高紀錄 ({discount_max:.1f}%)。此情境從未在實際營運中發生，預測結果不具參考價值，建議高階主管謹慎評估。",
        "guard_margin_negative_error": "⚠️ 毛利率為負數，每筆訂單將直接虧損，請重新設定。",
        "guard_margin_low_warning": "📋 毛利率低於 10%，屬於極低利潤情境，建議確認此假設是否符合實際營運狀況。",
        "guard_margin_high_warning": "📋 毛利率高於 80%，此假設明顯偏樂觀，建議確認是否已納入所有成本項目。",
        "guard_return_threshold_warning": "📋 退貨警示門檻 {return_threshold:.1f}% 高於歷史95百分位 ({return_max:.1f}%)。此門檻過寬，將導致高退貨商品無法被識別，建議回調至合理範圍。",
        "guard_elasticity_warning": "📋 行銷彈性假設 {elasticity:.1f}% 超出合理情境上限 ({elasticity_safe_max:.1f}%)。此假設缺乏歷史數據支撐，ROI 計算結果屬於樂觀推算，請勿直接用於預算申請。",
        "guard_budget_error": "⚠️ 行銷預算 ${budget:,.0f} 已超過歷史月均營收的15%(安全上限 ${budget_safe_max:,.0f})。此規模的行銷投入在歷史數據中無對應案例，預測結果具有高度不確定性，建議提交風險委員會審核。",
        "guard_success": "✅ 所有參數均通過歷史邊界與商業假設檢查，預測結果可作為決策參考。",
        "guard_bounds_expander": "📊 歷史數據安全邊界參考",
        "guard_bounds_col_param": "參數",
        "guard_bounds_col_lower": "歷史安全下限",
        "guard_bounds_col_upper": "歷史安全上限",
        "guard_param_discount": "折扣率",
        "guard_param_return_threshold": "退貨率門檻",
        "guard_param_marketing_elasticity": "行銷彈性",
        "guard_param_marketing_budget": "行銷預算",
        "guard_bounds_caption": "邊界值依歷史數據5th–95th百分位計算。超出範圍之預測屬外推，信賴度降低。",
        "guard_margin_caption": "毛利率為使用者自行假設，資料集不含實際成本數據，故無歷史邊界可供比對。",
        "empty_filter": "篩選後沒有資料。請放寬篩選條件。",
        "app_title": "零售 AI 決策支援系統",
        "app_subtitle": "目標：把原始電商 CSV 資料轉成互動式決策儀表板：資料清理 → 商業指標 → 風險警示 → 情境模擬。",
        "kpi_revenue": "營收",
        "kpi_orders": "訂單數",
        "kpi_active_customers": "活躍客戶",
        "kpi_avg_order_value": "平均訂單金額",
        "kpi_return_rate": "退貨率",
        "kpi_churn_rate": "流失率",
        "snapshot_title": "一目了然的決策訊號",
        "snapshot_top_category": "營收焦點",
        "snapshot_top_category_note": "目前篩選條件中最大的商品類別。",
        "snapshot_return_risk": "退貨風險",
        "snapshot_return_risk_note": "目前門檻下有 {count} 個商品需要檢查。",
        "snapshot_return_clear": "目前沒有商品超過退貨門檻。",
        "snapshot_profit_signal": "情境利潤",
        "snapshot_profit_positive": "在目前假設下為正向。",
        "snapshot_profit_negative": "納入預算與毛利假設後為負向。",
        "snapshot_model_signal": "模型信心",
        "snapshot_model_strong": "訊號可參考",
        "snapshot_model_medium": "需搭配情境判斷",
        "snapshot_model_low": "訊號偏弱",
        "not_available": "無法取得",
        "tab_overview": "高階儀表板",
        "tab_product": "風險與商品診斷",
        "tab_sim": "決策模擬器",
        "tab_data": "資料探勘表",
        "tab_log": "AI 除錯紀錄",
        "overview_header": "高階儀表板",
        "monthly_revenue_trend": "每月營收趨勢",
        "top_categories_revenue": "營收最高商品類別",
        "business_interpretation": "商業解讀",
        "no_chart_data": "目前篩選條件沒有可用圖表資料。",
        "chart_tooltip_revenue": "營收",
        "chart_tooltip_orders": "訂單",
        "overview_info": "在目前篩選資料中，營收最強的商品類別是 **{top_category}**（{top_category_rev}）。平均折扣為 **{avg_discount:.2f}%**，退貨率為 **{return_rate:.1%}**，回購客戶占比為 **{repeat_share:.1%}**。此儀表板應用來決定促銷資源配置，而不只是展示圖表。",
        "product_header": "風險與商品診斷",
        "high_return_products": "高退貨商品",
        "no_high_return": "沒有商品超過目前設定的退貨風險門檻。",
        "high_return_warning": "共有 {count} 個商品超過退貨門檻。這些商品需要檢查品管、物流或商品頁內容。",
        "best_revenue_products": "最佳營收商品",
        "customer_churn_watchlist": "客戶流失風險觀察名單",
        "churn_top_n": "顯示筆數",
        "churn_risk_threshold": "風險分數 ≥",
        "sim_header": "決策模擬器：折扣 → 營收 / 流量 / 利潤",
        "sim_caption": "這是一個謹慎的多因子線性迴歸情境估算器，不是保證準確的預測。它使用折扣以外的商業因素，讓使用者同時判斷預測與風險。",
        "sim_not_enough": "篩選後的每月資料不足，無法建立模擬器。請選擇更長期間或更大的商品類別範圍。",
        "current_avg_discount": "目前平均折扣",
        "simulated_avg_discount": "模擬平均折扣",
        "predicted_revenue_delta": "預測每月營收變化",
        "predicted_orders_delta": "預測每月訂單變化",
        "model_transparency": "模型透明度",
        "revenue_model_r2": "營收模型 R²",
        "revenue_slope": "營收斜率",
        "estimated_profit_delta": "預估每月利潤變化",
        "sim_focus_label": "最重要數字",
        "sim_focus_positive": "此情境會提升利潤。",
        "sim_focus_negative": "此情境會降低利潤。",
        "sim_focus_neutral": "此情境接近損益兩平。",
        "sim_key_changes": "需要注意的關鍵變化",
        "actual_vs_predicted_revenue": "實際 vs 預測營收",
        "actual_predicted_by_month": "每月實際與預測營收",
        "perfect_prediction": "完美預測線",
        "actual_revenue": "實際營收",
        "predicted_revenue": "預測營收",
        "model_fit_warning": "單靠折扣的解釋力偏弱，因此模擬器改用多因子模型，讓決策支援更穩健。",
        "multi_model_explanation": "主要模擬器使用每月訂單量、平均單價、平均數量、退貨率、配送天數、折扣、月份與年份。這比只用折扣更安全，因為營收變化通常同時受到多個商業因素影響。",
        "discount_model_limitation_header": "模型限制：單折扣迴歸",
        "discount_model_limitation_body": "單折扣模型的 R² 為 **{r2:.3f}**。它的預測會集中在平均每月營收附近，代表單靠折扣無法學到有意義的營收變化。此模型應保留在除錯/限制說明中，不作為主要決策模型。",
        "sim_detail_table": "顯示情境明細表",
        "simulated_discount_line": "目前模擬折扣：**{simulated_discount:.2f}%**",
        "historical_max_discount_line": "歷史最高平均折扣：**{historical_max_discount:.2f}%**",
        "discount_safe_success": "目前折扣仍在歷史資料範圍內，模擬結果相對較可信。",
        "discount_external_warning": "注意：目前模擬折扣已超過歷史資料範圍。這代表模型正在外推，預測結果只能作為參考，不能視為保證。",
        "discount_danger_error": "高風險：目前模擬折扣已明顯超過歷史範圍，模型預測可信度下降，且可能造成利潤快速惡化。",
        "profit_loss_dynamic_warning": "此情境會降低利潤，預估利潤變化為 {profit_change}。建議降低折扣或重新設定行銷預算。",
        "sim_support_revenue": "營收變化",
        "sim_support_orders": "訂單變化",
        "sim_support_discount": "折扣變化",
        "sim_support_marketing": "行銷 ROI",
        "sim_support_confidence": "信心程度",
        "delta_points": "點",
        "discount_point_unit": "USD / 折扣百分點",
        "boss_language": "用主管聽得懂的話說：在目前篩選的歷史資料中，平均折扣每增加 1 個百分點，約對應 **{slope_money}** 的每月營收變化。R² 為 **{r2:.3f}**，因此此工具應視為決策支援訊號，而不是自動答案。",
        "external_push_warning": "外推風險：模擬折扣 {new_discount:.2f}% 超出歷史範圍（{x_min:.2f}% 到 {x_max:.2f}%）。請不要過度信任此預測。",
        "low_explainability_warning": "低解釋力警示：單靠折扣無法很好地解釋營收。請結合商品類別、客戶區隔、商品退貨率與庫存策略一起判斷。",
        "profit_warning": "利潤警示：納入行銷預算與毛利率假設後，此情境可能降低利潤。",
        "scenario_success": "在目前假設下，此情境的財務結果看起來可接受，但仍需確認庫存與商品退貨風險。",
        "scenario_current": "目前",
        "scenario_simulated": "模擬",
        "col_scenario": "情境",
        "col_avg_discount": "平均折扣 %",
        "col_predicted_revenue": "預測每月營收",
        "col_predicted_orders": "預測每月訂單",
        "data_header": "資料探勘表與清理摘要",
        "quality_dataset": "資料集",
        "quality_rows": "列數",
        "quality_columns": "欄數",
        "quality_missing": "清理後缺失儲存格",
        "filtered_order_data": "篩選後訂單明細",
        "download_csv": "下載篩選資料 CSV",
        "log_header": "AI 協作除錯紀錄 / Prompt 與 Debug Log",
        "log_note": "最終報告可包含這種紀錄，以證明團隊不是盲目複製程式碼。",
        "col_stage": "階段",
        "col_problem": "問題",
        "col_fix": "修正",
        "stage_task_decomposition": "任務拆解",
        "problem_task_decomposition": "原始需求太廣：建立網站、分析資料、做決策模擬。",
        "fix_task_decomposition": "拆成資料清理、KPI 儀表板、商品/客戶風險診斷與模擬器。",
        "stage_red_error_1": "紅色錯誤 1",
        "problem_red_error_1": "customer_rating 有許多缺失值；圖表與模型摘要可能把空白評論誤解成低滿意度。",
        "fix_red_error_1": "先保留 rating_missing 旗標，再用中位數填補顯示與模型所需數值。",
        "stage_red_error_2": "紅色錯誤 2",
        "problem_red_error_2": "折扣滑桿可能推到歷史範圍之外，產生外推預測風險。",
        "fix_red_error_2": "當模擬折扣超出觀察到的歷史範圍時，加入 st.warning。",
        "stage_table_ui_fix": "觀察名單表格體驗",
        "problem_table_ui_fix": "客戶流失風險表使用進度條顯示風險分數，高分看起來像滿版 100%，也讓細節需要水平捲動才看得到。",
        "fix_table_ui_fix": "改成精簡自訂表格：風險分數同時顯示數字與短條，會員、天數與電子報欄位也調整成更容易掃讀的格式。",
        "stage_streamlit_api_fix": "Streamlit API 更新",
        "problem_streamlit_api_fix": "Streamlit 提醒 use_container_width 即將移除，未修正可能導致未來圖表顯示相容性問題。",
        "fix_streamlit_api_fix": "將 Plotly 圖表改為 width='stretch'，並同步更新嵌入式 stlite 版本。",
        "stage_business_guard": "商業防呆機制",
        "problem_business_guard": "決策滑桿可產生不合理情境卻沒有高階主管語境的風險提示，尤其行銷預算可能超過歷史月營收規模。",
        "fix_business_guard": "載入 monthly_revenue.csv，計算歷史安全邊界，加入 st.error/st.warning/st.success，並提供高階主管可查核的邊界參考表。",
        "stage_simulator_roi_fix": "決策模擬器 ROI 修正",
        "problem_simulator_roi_fix": "行銷彈性滑桿有收集但沒有進入兩個利潤公式；模擬器仍把行銷預算當成純成本扣除，且防呆檢查在篩選後歷史平均折扣尚未計算前就使用錯誤基準。",
        "fix_simulator_roi_fix": "用每月新客基準、行銷預算、行銷彈性與篩選後平均訂單金額計算 marketing_net，並套用到總覽快照與模擬器兩個利潤變化；預算為 0 時不扣成本，防呆檢查也改到 historical_avg_discount 計算後執行。",
        "stage_margin_guard_fix": "毛利率假設修正",
        "problem_margin_guard_fix": "資料集沒有 COGS/成本欄位，但原本用 subtotal、discount、shipping 推估毛利率，造成錯誤且偏高的歷史下限。",
        "fix_margin_guard_fix": "完全移除毛利率歷史邊界，改將毛利率視為使用者假設，針對負毛利、低毛利與過度樂觀毛利做商業合理性檢查。",
        "stage_bilingual_guard": "雙語風險簡報",
        "problem_bilingual_guard": "新增商業防呆訊息一開始只以繁體中文顯示，英文使用者無法閱讀高階風險提示。",
        "fix_bilingual_guard": "將防呆訊息、成功訊息、展開區標題、表格欄位與說明文字全部接入既有中英文語系字典。",
        "stage_business_diagnosis": "商業診斷",
        "problem_business_diagnosis": "低 R² 的模型看起來很數學，但策略參考價值可能很弱。",
        "fix_business_diagnosis": "明確顯示 R²，並用高階商業語言與警示解釋結果。",
        "demo_script": """
**建議 30 秒展示講稿**  
1. 從高階儀表板開始，指出營收最高的商品類別。  
2. 進入風險與商品診斷，說明高營收商品是否同時有高退貨風險。  
3. 進入決策模擬器，移動折扣滑桿，解釋 R²、斜率、利潤變化與警示。  
4. 結論：資料不會替你做決策；資料會在決策前讓風險變得可見。
""",
    },
}

language = st.sidebar.selectbox("Language / 語言", list(TEXT.keys()), index=0)

def t(key):
    return TEXT[language].get(key, TEXT["English"].get(key, key))

def option_label(value):
    return t("all") if value == "All" else value

def table_labels():
    if language == "繁體中文":
        return {
            "order_id": "訂單 ID",
            "rank": "排名",
            "customer_id": "客戶 ID",
            "order_date": "訂單日期",
            "country": "國家",
            "membership_tier": "會員等級",
            "category": "商品類別",
            "product_name": "商品名稱",
            "quantity": "數量",
            "discount_pct": "折扣 %",
            "total_amount_usd": "訂單金額 USD",
            "returned": "是否退貨",
            "delivery_days": "配送天數",
            "customer_rating": "客戶評分",
            "total_orders": "訂單數",
            "total_revenue_usd": "營收 USD",
            "return_rate": "退貨率",
            "avg_rating": "平均評分",
            "avg_delivery_days": "平均配送天數",
            "total_spend_usd": "總消費 USD",
            "days_since_last_purchase": "距上次購買",
            "avg_review_score": "平均評論分數",
            "returns_made": "退貨次數",
            "newsletter_subscribed": "訂閱電子報",
            "churned": "已流失",
            "risk_score": "風險分數",
        }
    return {
        "order_id": "Order ID",
        "rank": "Rank",
        "customer_id": "Customer ID",
        "order_date": "Order date",
        "country": "Country",
        "membership_tier": "Membership",
        "category": "Product category",
        "product_name": "Product name",
        "quantity": "Quantity",
        "discount_pct": "Discount %",
        "total_amount_usd": "Order amount USD",
        "returned": "Returned",
        "delivery_days": "Delivery days",
        "customer_rating": "Customer rating",
        "total_orders": "Orders",
        "total_revenue_usd": "Revenue USD",
        "return_rate": "Return rate",
        "avg_rating": "Average rating",
        "avg_delivery_days": "Average delivery days",
        "total_spend_usd": "Total spend USD",
        "days_since_last_purchase": "Days since last purchase",
        "avg_review_score": "Average review score",
        "returns_made": "Returns made",
        "newsletter_subscribed": "Newsletter subscribed",
        "churned": "Churned",
        "risk_score": "Risk score",
    }

def human_table(df):
    return df.rename(columns=table_labels())

def short_category_name(value):
    raw = "" if pd.isna(value) else str(value)
    short_names = {
        "Beauty & Personal Care": "Beauty",
        "Clothing & Apparel": "Clothing",
        "Food & Grocery": "Grocery",
        "Health & Wellness": "Health",
        "Home & Kitchen": "Home",
        "Jewelry & Accessories": "Jewelry",
        "Office Supplies": "Office",
        "Pet Supplies": "Pet",
        "Sports & Outdoors": "Sports",
        "Toys & Games": "Toys",
        "Travel & Luggage": "Travel",
    }
    return short_names.get(raw, raw.split("&")[0].strip())

def category_badge(value):
    raw = "" if pd.isna(value) else str(value)
    label = short_category_name(raw)
    return f'<span class="badge badge-cat" title="{escape(raw)}">{escape(label)}</span>'

def tier_badge(value):
    raw = "" if pd.isna(value) else str(value)
    tier_class = raw.lower().replace(" ", "-")
    return f'<span class="badge badge-tier-{escape(tier_class)}">{escape(raw)}</span>'

def money_cell(value):
    return f'<span class="money">{escape(money(float(value)))}</span>'

def return_bar(value):
    val = 0.0 if pd.isna(value) else float(value)
    display = val * 100 if val <= 1 else val
    width = max(3, min(100, display / 30 * 100))
    tone = "danger" if display >= 15 else "warn" if display >= 10 else ""
    return (
        '<div class="return-cell">'
        f'<span>{display:.1f}%</span>'
        '<span class="return-track">'
        f'<span class="return-fill {tone}" style="width: {width:.1f}%"></span>'
        '</span>'
        '</div>'
    )

def risk_score_cell(value):
    val = 0 if pd.isna(value) else int(value)
    tone = "danger" if val >= 65 else "warn" if val >= 35 else ""
    width = max(3, min(100, val))
    return (
        '<div class="risk-score">'
        f'<span class="num">{val}</span>'
        '<span class="risk-track">'
        f'<span class="risk-fill {tone}" style="width: {width}%"></span>'
        '</span>'
        '</div>'
    )

def yes_no(value):
    if pd.isna(value):
        return ""
    if language == "English":
        return "Yes" if int(value) else "No"
    return "是" if int(value) else "否"

def day_cell(value):
    if pd.isna(value):
        return ""
    unit = "天" if language == "繁體中文" else "d"
    return f"{int(value):,} {unit}"

def rank_cell(value):
    return f'<span class="dm-rank">{int(value)}</span>'

def plain_cell(value):
    if pd.isna(value):
        return ""
    if isinstance(value, pd.Timestamp):
        return value.strftime("%Y-%m-%d")
    return escape(str(value))

def section_label(title, count):
    return (
        '<div class="section-divider">'
        f'<div class="section-label">{escape(title)}</div>'
        f'<div class="count-badge">{int(count):,}</div>'
        '</div>'
    )

def render_dm_table(title, df, columns, empty_text=None, min_width="980px"):
    if df.empty:
        title_html = f'<div class="dm-title">{escape(title)}</div>' if title else ""
        return f'<div class="dm-card">{title_html}<div class="ok-box">{escape(empty_text or t("no_chart_data"))}</div></div>'

    labels = table_labels()
    widths = []
    headers = []
    for col in columns:
        widths.append(f'<col style="width: {escape(col.get("width", "auto"))}">')
        headers.append(f'<th class="{escape(col.get("class", ""))}">{escape(col.get("label", labels.get(col["key"], col["key"])))}</th>')

    rows = []
    for _, row in df.iterrows():
        cells = []
        for col in columns:
            key = col["key"]
            renderer = col.get("render", plain_cell)
            cls = escape(col.get("class", ""))
            cells.append(f'<td class="{cls}">{renderer(row.get(key, ""))}</td>')
        rows.append("<tr>" + "".join(cells) + "</tr>")

    return (
        '<div class="dm-card">'
        + (f'<div class="dm-title">{escape(title)}</div>' if title else "")
        + f'<div class="dm-scroll"><table class="dm-table" style="min-width: {escape(min_width)}">'
        + '<colgroup>' + "".join(widths) + '</colgroup>'
        + '<thead><tr>' + "".join(headers) + '</tr></thead>'
        + '<tbody>' + "".join(rows) + '</tbody>'
        + '</table></div></div>'
    )

# ---------- Sidebar controls ----------
st.sidebar.title(t("sidebar_title"))
st.sidebar.caption(t("sidebar_caption"))

category_options = ["All"] + sorted(orders["category"].dropna().unique().tolist())
country_options = ["All"] + sorted(customers["country"].dropna().unique().tolist())
tier_options = ["All"] + sorted(customers["membership_tier"].dropna().unique().tolist())

category_filter = st.sidebar.selectbox(t("category_filter"), category_options, index=0, format_func=option_label)
country_filter = st.sidebar.selectbox(t("country_filter"), country_options, index=0, format_func=option_label)
tier_filter = st.sidebar.selectbox(t("tier_filter"), tier_options, index=0, format_func=option_label)

min_date = orders["order_date"].min().date()
max_date = orders["order_date"].max().date()
start_date_input = st.sidebar.date_input(t("start_date_filter"), value=min_date, min_value=min_date, max_value=max_date)
end_date_input = st.sidebar.date_input(t("end_date_filter"), value=max_date, min_value=min_date, max_value=max_date)

start_date = pd.to_datetime(start_date_input)
end_date = pd.to_datetime(end_date_input)
if start_date > end_date:
    st.sidebar.warning(t("date_range_swapped"))
    start_date, end_date = end_date, start_date

extra_discount = st.sidebar.slider(t("extra_discount"), 0, 15, 0, 1)
gross_margin = st.sidebar.slider(t("gross_margin"), -20, 100, 38, 1)
marketing_budget = st.sidebar.number_input(t("marketing_budget"), min_value=0, max_value=1000000, value=5000, step=1000)
marketing_elasticity = st.sidebar.slider(t("marketing_elasticity"), 0, 20, 5, 1)
return_threshold = st.sidebar.slider(t("return_threshold"), 0, 30, 10, 1)

# ---------- Filtering ----------
work = merged.copy()
work = work[(work["order_date"] >= start_date) & (work["order_date"] <= end_date)]
if category_filter != "All":
    work = work[work["category"] == category_filter]
if country_filter != "All":
    work = work[work["country"] == country_filter]
if tier_filter != "All":
    work = work[work["membership_tier"] == tier_filter]

if work.empty:
    st.error(t("empty_filter"))
    st.stop()

# ---------- Helper functions ----------
def money(x):
    return f"${x:,.0f}"

def pct(x):
    return f"{x:.1%}"

def render_revenue_trend(df, no_data_text, revenue_label, orders_label):
    chart_cols = ["order_date", "revenue_usd"] + (["order_count"] if "order_count" in df.columns else [])
    clean = df[chart_cols].dropna().sort_values("order_date").copy()
    if clean.empty:
        return f'<div class="chart-shell small-note">{escape(no_data_text)}</div>'

    width, height = 640, 260
    left, right, top, bottom = 48, 18, 18, 38
    plot_w = width - left - right
    plot_h = height - top - bottom
    values = clean["revenue_usd"].astype(float).to_numpy()
    order_values = clean["order_count"].astype(int).to_numpy() if "order_count" in clean.columns else np.zeros(len(clean), dtype=int)
    dates = clean["order_date"].to_list()
    v_min, v_max = float(values.min()), float(values.max())
    if v_min == v_max:
        v_min = max(0.0, v_min * 0.9)
        v_max = v_max * 1.1 if v_max else 1.0

    points = []
    for i, value in enumerate(values):
        x = left + (plot_w * i / max(len(values) - 1, 1))
        y = top + plot_h - ((value - v_min) / (v_max - v_min) * plot_h)
        points.append((x, y, value, order_values[i], pd.to_datetime(dates[i]).strftime("%Y-%m")))

    point_attr = " ".join(f"{x:.1f},{y:.1f}" for x, y, _, _, _ in points)
    point_groups = []
    for x, y, value, order_value, date_label in points:
        box_x = min(max(x - 74, left), width - right - 148)
        box_y = y - 48 if y > top + 54 else y + 16
        point_groups.append(
            f'<g class="chart-point">'
            f'<circle class="chart-hit" cx="{x:.1f}" cy="{y:.1f}" r="13" />'
            f'<circle class="chart-dot" cx="{x:.1f}" cy="{y:.1f}" r="4" />'
            f'<title>{escape(date_label)} · {escape(revenue_label)} {escape(money(value))} · {escape(orders_label)} {order_value:,}</title>'
            f'<g class="chart-tooltip">'
            f'<rect class="tooltip-box" x="{box_x:.1f}" y="{box_y:.1f}" width="148" height="38" />'
            f'<text class="tooltip-text" x="{box_x + 8:.1f}" y="{box_y + 15:.1f}">{escape(date_label)}</text>'
            f'<text class="tooltip-text" x="{box_x + 8:.1f}" y="{box_y + 30:.1f}">{escape(money(value))} · {order_value:,}</text>'
            f'</g>'
            f'</g>'
        )
    circles = "\n".join(point_groups)
    first_label = pd.to_datetime(dates[0]).strftime("%Y-%m")
    last_label = pd.to_datetime(dates[-1]).strftime("%Y-%m")

    return f"""
<div class="chart-shell">
<svg class="line-chart-svg" viewBox="0 0 {width} {height}" role="img" aria-label="Monthly revenue trend">
    <line class="chart-axis" x1="{left}" y1="{top + plot_h}" x2="{width - right}" y2="{top + plot_h}" />
    <line class="chart-axis" x1="{left}" y1="{top}" x2="{left}" y2="{top + plot_h}" />
    <line class="chart-grid" x1="{left}" y1="{top}" x2="{width - right}" y2="{top}" />
    <line class="chart-grid" x1="{left}" y1="{top + plot_h / 2}" x2="{width - right}" y2="{top + plot_h / 2}" />
    <polyline class="chart-line" points="{point_attr}" />
    {circles}
    <text class="chart-label" x="{left}" y="{height - 12}">{escape(first_label)}</text>
    <text class="chart-label" text-anchor="end" x="{width - right}" y="{height - 12}">{escape(last_label)}</text>
    <text class="chart-label" x="4" y="{top + 5}">{escape(money(v_max))}</text>
    <text class="chart-label" x="4" y="{top + plot_h + 4}">{escape(money(v_min))}</text>
</svg>
</div>
"""

def render_category_bars(series, no_data_text):
    clean = series.dropna()
    clean = clean[clean > 0]
    if clean.empty:
        return f'<div class="chart-shell small-note">{escape(no_data_text)}</div>'

    max_value = float(clean.max())
    rows = []
    for label, value in clean.items():
        pct_width = max(2.0, float(value) / max_value * 100)
        rows.append(
            '<div class="bar-row">'
            f'<div class="bar-label" title="{escape(str(label))}">{escape(short_category_name(label))}</div>'
            '<div class="bar-track">'
            f'<div class="bar-fill" style="width: {pct_width:.1f}%"></div>'
            '</div>'
            f'<div class="bar-value">{escape(money(float(value)))}</div>'
            '</div>'
        )

    return '<div class="chart-shell"><div class="bar-list">' + "".join(rows) + "</div></div>"

def render_kpi_grid(items, tier="primary"):
    grid_class = "kpi-primary-grid" if tier == "primary" else "kpi-secondary-grid"
    tiles = []
    for item in items:
        tone = escape(item.get("tone", ""))
        tier_class = f"primary {tone}" if tier == "primary" else f"secondary {tone}"
        tiles.append(
            f'<div class="kpi-tile {tier_class}">'
            f'<div class="kpi-label">{escape(item["label"])}</div>'
            f'<div class="kpi-value">{escape(item["value"])}</div>'
            '</div>'
        )
    return f'<div class="{grid_class}">' + "".join(tiles) + "</div>"

def render_signal_grid(title, items):
    cards = [f'<div class="snapshot-title">{escape(title)}</div>', '<div class="signal-grid">']
    for item in items:
        tone = escape(item.get("tone", ""))
        cards.append(
            f'<div class="signal-card {tone}">'
            f'<div class="signal-label"><span class="signal-dot"></span>{escape(item["label"])}</div>'
            f'<div class="signal-value">{escape(item["value"])}</div>'
            f'<div class="signal-note">{escape(item["note"])}</div>'
            '</div>'
        )
    cards.append("</div>")
    return "".join(cards)

def render_model_diagnostics(model):
    if model is None:
        return
    try:
        import plotly.express as px
        import plotly.graph_objects as go
    except ModuleNotFoundError:
        st.warning("Plotly is not installed, so the Actual vs Predicted Revenue chart cannot be rendered.")
        return

    actual = pd.Series(model["actual"], dtype=float)
    predicted = pd.Series(model["predicted"], dtype=float)
    r2 = model["r2"]

    fig = px.scatter(
        x=actual,
        y=predicted,
        labels={"x": t("actual_revenue"), "y": t("predicted_revenue")},
        title=f"{t('actual_vs_predicted_revenue')} | R² = {r2:.3f}",
    )
    min_val = min(float(actual.min()), float(predicted.min()))
    max_val = max(float(actual.max()), float(predicted.max()))
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name=t("perfect_prediction"),
            line={"color": "#dc2626", "dash": "dash"},
        )
    )
    fig.update_layout(
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
        legend={"orientation": "h", "y": -0.2},
    )
    st.plotly_chart(fig, width="stretch")

    monthly_fit = pd.DataFrame({
        "Month": model["dates"],
        t("actual_revenue"): actual,
        t("predicted_revenue"): predicted,
    }).sort_values("Month")
    line_fig = px.line(
        monthly_fit,
        x="Month",
        y=[t("actual_revenue"), t("predicted_revenue")],
        title=f"{t('actual_predicted_by_month')} | R² = {r2:.3f}",
    )
    line_fig.update_layout(
        margin={"l": 10, "r": 10, "t": 60, "b": 10},
        legend_title_text="",
    )
    st.plotly_chart(line_fig, width="stretch")

def fit_simple_linear(df, x_col, y_col):
    clean_cols = [x_col, y_col] + (["order_date"] if "order_date" in df.columns else [])
    clean = df[clean_cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) < 3 or clean[x_col].nunique() < 2 or clean[y_col].nunique() < 2:
        return None
    x = clean[x_col].astype(float).to_numpy()
    y = clean[y_col].astype(float).to_numpy()
    slope, intercept = np.polyfit(x, y, 1)
    pred = slope * x + intercept
    denom = ((y - y.mean()) ** 2).sum()
    r2 = 0.0 if denom == 0 else 1 - ((y - pred) ** 2).sum() / denom
    return {
        "slope": float(slope),
        "intercept": float(intercept),
        "r2": float(r2),
        "x_min": float(x.min()),
        "x_max": float(x.max()),
        "x_mean": float(x.mean()),
        "n": int(len(clean)),
        "actual": y,
        "predicted": pred,
        "dates": clean["order_date"].to_list() if "order_date" in clean.columns else list(range(len(clean))),
    }

MULTI_FEATURES = [
    "order_count",
    "avg_unit_price",
    "avg_quantity",
    "return_rate",
    "avg_delivery_days",
    "avg_discount_pct",
    "month",
    "year",
]

def fit_multi_linear(df, features, target_col):
    clean_cols = ["order_date", target_col] + features
    clean = df[clean_cols].replace([np.inf, -np.inf], np.nan).dropna()
    if len(clean) <= len(features) + 1 or clean[target_col].nunique() < 2:
        return None

    x_raw = clean[features].astype(float)
    y = clean[target_col].astype(float).to_numpy()
    means = x_raw.mean()
    stds = x_raw.std(ddof=0).replace(0, 1)
    x_scaled = ((x_raw - means) / stds).to_numpy()
    design = np.column_stack([np.ones(len(x_scaled)), x_scaled])
    coef, *_ = np.linalg.lstsq(design, y, rcond=None)
    pred = design @ coef
    denom = ((y - y.mean()) ** 2).sum()
    r2 = 0.0 if denom == 0 else 1 - ((y - pred) ** 2).sum() / denom
    return {
        "features": features,
        "coef": coef,
        "means": means,
        "stds": stds,
        "r2": float(r2),
        "n": int(len(clean)),
        "actual": y,
        "predicted": pred,
        "dates": clean["order_date"].to_list(),
    }

def predict_multi(model, values):
    row = pd.Series(values, dtype=float).reindex(model["features"])
    scaled = ((row - model["means"]) / model["stds"]).to_numpy()
    design = np.concatenate([[1.0], scaled])
    return float(design @ model["coef"])

def build_monthly(df):
    monthly = (
        df.groupby(pd.Grouper(key="order_date", freq="ME"))
        .agg(
            revenue_usd=("total_amount_usd", "sum"),
            order_count=("order_id", "count"),
            avg_unit_price=("unit_price_usd", "mean"),
            avg_quantity=("quantity", "mean"),
            avg_discount_pct=("discount_pct", "mean"),
            return_rate=("returned", "mean"),
            avg_delivery_days=("delivery_days", "mean"),
        )
        .dropna()
        .reset_index()
    )
    monthly["month"] = monthly["order_date"].dt.month
    monthly["year"] = monthly["order_date"].dt.year
    return monthly

monthly = build_monthly(work)
historical_avg_discount = monthly["avg_discount_pct"].mean() if not monthly.empty else work["discount_pct"].mean()
historical_max_discount = monthly["avg_discount_pct"].max() if not monthly.empty else work["discount_pct"].max()
discount_revenue_model = fit_simple_linear(monthly, "avg_discount_pct", "revenue_usd")
multi_revenue_model = fit_multi_linear(monthly, MULTI_FEATURES, "revenue_usd")
traffic_model = fit_simple_linear(monthly, "avg_discount_pct", "order_count")

scenario_discount_guard = historical_avg_discount + extra_discount
warnings_list, errors_list = check_extrapolation(
    scenario_discount_guard,
    gross_margin,
    return_threshold,
    marketing_elasticity,
    marketing_budget,
)

with st.sidebar:
    if errors_list:
        for msg in errors_list:
            st.error(msg)

    if warnings_list:
        for msg in warnings_list:
            st.warning(msg)

    if not errors_list and not warnings_list:
        st.success(t("guard_success"))

    with st.expander(t("guard_bounds_expander")):
        st.markdown(
            f"""
| {t("guard_bounds_col_param")} | {t("guard_bounds_col_lower")} | {t("guard_bounds_col_upper")} |
|------|------------|------------|
| {t("guard_param_discount")} | {DISCOUNT_MIN:.1f}% | {DISCOUNT_MAX:.1f}% |
| {t("guard_param_return_threshold")} | {RETURN_MIN:.1f}% | {RETURN_MAX:.1f}% |
| {t("guard_param_marketing_elasticity")} | 0% | {ELASTICITY_SAFE_MAX:.1f}% |
| {t("guard_param_marketing_budget")} | $0 | ${BUDGET_SAFE_MAX:,.0f} |
"""
        )
        st.caption(t("guard_bounds_caption"))
        st.caption(t("guard_margin_caption"))

# ---------- Header ----------
st.markdown(
    '<div class="sticky-title">'
    '<div class="app-header"><span class="app-icon">📊</span>'
    f'<div class="big-title">{t("app_title")}</div></div>'
    f'<div class="subtitle">{t("app_subtitle")}</div>'
    '</div>',
    unsafe_allow_html=True,
)

# ---------- KPI row ----------
revenue = work["total_amount_usd"].sum()
order_count = work["order_id"].nunique()
active_customers = work["customer_id"].nunique()
avg_order_value = revenue / order_count if order_count else 0
return_rate = work["returned"].mean()
avg_discount_now = work["discount_pct"].mean()
mr_filtered = monthly_revenue.copy()
mr_filtered = mr_filtered[
    (mr_filtered["order_date"] >= start_date)
    & (mr_filtered["order_date"] <= end_date)
]
baseline_new_customers = pd.to_numeric(mr_filtered["new_customers"], errors="coerce").mean()
if pd.isna(baseline_new_customers):
    baseline_new_customers = pd.to_numeric(monthly_revenue["new_customers"], errors="coerce").mean()
baseline_new_customers = 0.0 if pd.isna(baseline_new_customers) else float(baseline_new_customers)
avg_order_val = work["total_amount_usd"].mean()
avg_order_val = 0.0 if pd.isna(avg_order_val) else float(avg_order_val)
if marketing_budget > 0:
    extra_customers = baseline_new_customers * (marketing_budget / 1000) * (marketing_elasticity / 100)
    marketing_extra_revenue = extra_customers * avg_order_val
    marketing_net = marketing_extra_revenue - marketing_budget
else:
    extra_customers = 0.0
    marketing_extra_revenue = 0.0
    marketing_net = 0.0
customer_scope = customers.copy()
if country_filter != "All":
    customer_scope = customer_scope[customer_scope["country"] == country_filter]
if tier_filter != "All":
    customer_scope = customer_scope[customer_scope["membership_tier"] == tier_filter]
churn_rate = customer_scope["churned"].mean() if not customer_scope.empty else 0

category_revenue = work.groupby("category")["total_amount_usd"].sum().sort_values(ascending=False)
top_category = category_revenue.idxmax()
top_category_rev = category_revenue.max()

summary_products = products.copy()
if category_filter != "All":
    summary_products = summary_products[summary_products["category"] == category_filter]
high_return_count = int((summary_products["return_rate"] >= return_threshold).sum())

if not monthly.empty:
    base_feature_values = monthly[MULTI_FEATURES].mean()
else:
    base_feature_values = pd.Series({
        "order_count": order_count,
        "avg_unit_price": work["unit_price_usd"].mean(),
        "avg_quantity": work["quantity"].mean(),
        "return_rate": return_rate,
        "avg_delivery_days": work["delivery_days"].mean(),
        "avg_discount_pct": avg_discount_now,
        "month": work["order_date"].dt.month.mean(),
        "year": work["order_date"].dt.year.mean(),
    })

snapshot_profit_delta = None
if multi_revenue_model is not None:
    snapshot_discount = historical_avg_discount + extra_discount
    snapshot_now_features = base_feature_values.copy()
    snapshot_new_features = base_feature_values.copy()
    snapshot_now_features["avg_discount_pct"] = historical_avg_discount
    snapshot_new_features["avg_discount_pct"] = snapshot_discount
    snapshot_rev_now = predict_multi(multi_revenue_model, snapshot_now_features)
    snapshot_rev_new = predict_multi(multi_revenue_model, snapshot_new_features)
    snapshot_profit_delta = (snapshot_rev_new - snapshot_rev_now) * (gross_margin / 100) + marketing_net

model_r2 = multi_revenue_model["r2"] if multi_revenue_model is not None else None
if model_r2 is None:
    model_tone, model_value, model_note = "warn", t("not_available"), t("sim_not_enough")
elif model_r2 >= 0.3:
    model_tone, model_value, model_note = "ok", f"R² {model_r2:.3f}", t("snapshot_model_strong")
elif model_r2 >= 0.15:
    model_tone, model_value, model_note = "warn", f"R² {model_r2:.3f}", t("snapshot_model_medium")
else:
    model_tone, model_value, model_note = "danger", f"R² {model_r2:.3f}", t("snapshot_model_low")

if snapshot_profit_delta is None:
    profit_tone, profit_value, profit_note = "warn", t("not_available"), t("sim_not_enough")
elif snapshot_profit_delta >= 0:
    profit_tone, profit_value, profit_note = "ok", money(snapshot_profit_delta), t("snapshot_profit_positive")
else:
    profit_tone, profit_value, profit_note = "danger", money(snapshot_profit_delta), t("snapshot_profit_negative")

# Primary KPIs (larger, more prominent)
st.markdown(
    render_kpi_grid([
        {"label": f"💰 {t('kpi_revenue')}", "value": money(revenue), "tone": "ok"},
        {"label": f"👥 {t('kpi_active_customers')}", "value": f"{active_customers:,}", "tone": "ok"},
        {"label": f"⚠️ {t('kpi_churn_rate')}", "value": pct(churn_rate), "tone": "danger" if churn_rate >= 0.25 else "warn" if churn_rate >= 0.12 else "ok"},
    ], tier="primary"),
    unsafe_allow_html=True,
)

# Secondary KPIs (smaller supporting metrics)
st.markdown(
    render_kpi_grid([
        {"label": f"🧾 {t('kpi_orders')}", "value": f"{order_count:,}", "tone": ""},
        {"label": f"🛒 {t('kpi_avg_order_value')}", "value": money(avg_order_value), "tone": ""},
        {"label": f"↩️ {t('kpi_return_rate')}", "value": pct(return_rate), "tone": "danger" if return_rate >= 0.10 else "ok"},
    ], tier="secondary"),
    unsafe_allow_html=True,
)

# Decision signals (3 key insights instead of 4)
st.markdown(
    render_signal_grid(
        "🎯 " + t("snapshot_title"),
        [
            {
                "label": t("snapshot_top_category"),
                "value": f"{short_category_name(top_category)}",
                "note": f"{money(top_category_rev)} · " + t("snapshot_top_category_note"),
                "tone": "ok",
            },
            {
                "label": t("snapshot_return_risk"),
                "value": f"{high_return_count}",
                "note": t("snapshot_return_risk_note").format(count=high_return_count) if high_return_count else t("snapshot_return_clear"),
                "tone": "danger" if high_return_count else "ok",
            },
            {
                "label": t("snapshot_profit_signal"),
                "value": profit_value,
                "note": profit_note,
                "tone": profit_tone,
            },
        ],
    ),
    unsafe_allow_html=True,
)

# ---------- Tabs ----------
tab_overview, tab_product, tab_sim, tab_data, tab_log = st.tabs([
    f"1. {t('tab_overview')}",
    f"2. {t('tab_product')}",
    f"3. {t('tab_sim')}",
    f"4. {t('tab_data')}",
    f"5. {t('tab_log')}",
])

with tab_overview:
    st.subheader(t("overview_header"))
    left, right = st.columns([1.5, 1])
    with left:
        st.markdown(f"**{t('monthly_revenue_trend')}**")
        st.markdown(
            render_revenue_trend(monthly, t("no_chart_data"), t("chart_tooltip_revenue"), t("chart_tooltip_orders")),
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(f"**{t('top_categories_revenue')}**")
        cat_rev = work.groupby("category")["total_amount_usd"].sum().sort_values(ascending=False).head(10)
        st.markdown(render_category_bars(cat_rev, t("no_chart_data")), unsafe_allow_html=True)

    st.markdown(f"**{t('business_interpretation')}**")
    top_category = work.groupby("category")["total_amount_usd"].sum().idxmax()
    top_category_rev = work.groupby("category")["total_amount_usd"].sum().max()
    repeat_share = work["is_repeat_customer"].mean() if "is_repeat_customer" in work.columns else np.nan
    st.info(
        t("overview_info").format(
            top_category=top_category,
            top_category_rev=money(top_category_rev),
            avg_discount=avg_discount_now,
            return_rate=return_rate,
            repeat_share=repeat_share,
        )
    )

with tab_product:
    st.subheader(t("product_header"))
    p = products.copy()
    if category_filter != "All":
        p = p[p["category"] == category_filter]
    high_return = p[p["return_rate"] >= return_threshold].sort_values("return_rate", ascending=False)

    st.markdown(section_label(t("high_return_products"), len(high_return)), unsafe_allow_html=True)
    product_cols = [
        {"key": "category", "width": "10%", "render": category_badge},
        {"key": "product_name", "width": "34%", "class": "product"},
        {"key": "total_revenue_usd", "width": "14%", "class": "num", "render": money_cell},
        {"key": "return_rate", "width": "18%", "render": return_bar},
        {"key": "avg_rating", "width": "12%", "class": "num", "render": lambda v: f"{float(v):.2f}"},
        {"key": "avg_delivery_days", "width": "12%", "class": "num", "render": lambda v: f"{float(v):.1f}"},
    ]
    high_return_display = high_return[["category", "product_name", "total_revenue_usd", "return_rate", "avg_rating", "avg_delivery_days"]].head(5)
    if high_return.empty:
        st.markdown(
            render_dm_table(
                t("high_return_products"),
                high_return,
                product_cols,
                empty_text=t("no_high_return"),
                min_width="720px",
            ),
            unsafe_allow_html=True,
        )
    else:
        st.warning(t("high_return_warning").format(count=len(high_return)))
        st.dataframe(
            human_table(high_return_display),
            width="stretch",
            hide_index=True,
            column_config={
                table_labels()["total_revenue_usd"]: st.column_config.NumberColumn(format="$%d"),
                table_labels()["return_rate"]: st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=30),
            },
        )

    st.markdown(section_label(t("best_revenue_products"), len(p)), unsafe_allow_html=True)
    best_products = p.sort_values("total_revenue_usd", ascending=False).head(5).copy()
    best_products.insert(0, "rank", range(1, len(best_products) + 1))
    st.dataframe(
        human_table(best_products[["rank", "category", "product_name", "total_orders", "total_revenue_usd", "avg_rating", "return_rate"]]),
        width="stretch",
        hide_index=True,
        column_config={
            table_labels()["total_revenue_usd"]: st.column_config.NumberColumn(format="$%d"),
            table_labels()["return_rate"]: st.column_config.ProgressColumn(format="%.1f%%", min_value=0, max_value=30),
        },
    )

    customer_risk = customers.copy()
    customer_risk["risk_score"] = (
        (customer_risk["days_since_last_purchase"] > 120).astype(int) * 35
        + (customer_risk["avg_review_score"] < 3.2).astype(int) * 25
        + (customer_risk["returns_made"] >= 3).astype(int) * 20
        + (customer_risk["newsletter_subscribed"] == 0).astype(int) * 10
        + (customer_risk["churned"] == 1).astype(int) * 10
    )
    if country_filter != "All":
        customer_risk = customer_risk[customer_risk["country"] == country_filter]
    if tier_filter != "All":
        customer_risk = customer_risk[customer_risk["membership_tier"] == tier_filter]
    churn_risk_threshold = st.slider(t("churn_risk_threshold"), 0, 100, 35, 5)
    customer_risk_filtered = customer_risk[customer_risk["risk_score"] >= churn_risk_threshold]
    st.markdown(section_label(t("customer_churn_watchlist"), len(customer_risk_filtered)), unsafe_allow_html=True)
    customer_risk_display = customer_risk_filtered.sort_values("risk_score", ascending=False)[[
        "customer_id", "country", "membership_tier", "total_spend_usd", "days_since_last_purchase",
        "avg_review_score", "returns_made", "newsletter_subscribed", "risk_score"
    ]].head(5)
    customer_cols = [
        {"key": "customer_id", "width": "9%"},
        {"key": "country", "width": "13%"},
        {"key": "membership_tier", "width": "10%", "render": tier_badge},
        {"key": "total_spend_usd", "width": "11%", "class": "num", "render": money_cell},
        {"key": "days_since_last_purchase", "width": "14%", "class": "num", "render": day_cell},
        {"key": "avg_review_score", "width": "12%", "class": "num", "render": lambda v: f"{float(v):.1f}"},
        {"key": "returns_made", "width": "9%", "class": "num"},
        {"key": "newsletter_subscribed", "width": "10%", "render": yes_no},
        {"key": "risk_score", "width": "12%", "render": risk_score_cell},
    ]
    st.markdown(
        render_dm_table(
            "",
            customer_risk_display,
            customer_cols,
            min_width="900px",
        ),
        unsafe_allow_html=True,
    )

with tab_sim:
    st.subheader(t("sim_header"))
    st.caption(t("sim_caption"))

    if multi_revenue_model is None:
        st.error(t("sim_not_enough"))
    else:
        new_discount = historical_avg_discount + extra_discount
        warning_threshold = historical_max_discount
        danger_threshold = historical_max_discount + 3

        current_features = base_feature_values.copy()
        simulated_features = base_feature_values.copy()
        current_features["avg_discount_pct"] = historical_avg_discount
        simulated_features["avg_discount_pct"] = new_discount

        if traffic_model is not None:
            orders_now = traffic_model["slope"] * historical_avg_discount + traffic_model["intercept"]
            orders_new = traffic_model["slope"] * new_discount + traffic_model["intercept"]
        else:
            orders_now = base_feature_values["order_count"]
            orders_new = base_feature_values["order_count"]
        current_features["order_count"] = max(0, orders_now)
        simulated_features["order_count"] = max(0, orders_new)

        rev_now = predict_multi(multi_revenue_model, current_features)
        rev_new = predict_multi(multi_revenue_model, simulated_features)

        revenue_delta = rev_new - rev_now
        orders_delta = orders_new - orders_now
        estimated_profit_delta = revenue_delta * (gross_margin / 100) + marketing_net
        marketing_card = None
        if marketing_budget > 0:
            marketing_card = {
                "label": t("sim_support_marketing"),
                "value": money(marketing_net),
                "note": f"{extra_customers:.1f} new customers · {money(marketing_extra_revenue)} revenue",
                "tone": "ok" if marketing_net >= 0 else "warn",
            }

        if estimated_profit_delta > 100:
            decision_tone = "ok"
            decision_note = t("sim_focus_positive")
        elif estimated_profit_delta < -100:
            decision_tone = "danger"
            decision_note = t("sim_focus_negative")
        else:
            decision_tone = "warn"
            decision_note = t("sim_focus_neutral")

        st.markdown(
            f"""
<div class="decision-focus {decision_tone}">
    <div class="decision-kicker">{escape(t("sim_focus_label"))}</div>
    <div class="decision-main">{escape(money(estimated_profit_delta))}</div>
    <div class="decision-note">{escape(decision_note)}</div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown(t("simulated_discount_line").format(simulated_discount=new_discount))
        st.markdown(t("historical_max_discount_line").format(historical_max_discount=historical_max_discount))
        if new_discount > danger_threshold:
            st.error(t("discount_danger_error"), icon="🚨")
        elif new_discount > warning_threshold:
            st.warning(t("discount_external_warning"), icon="⚠️")
        else:
            st.success(t("discount_safe_success"), icon="✅")

        if estimated_profit_delta < 0:
            st.error(
                t("profit_loss_dynamic_warning").format(profit_change=money(estimated_profit_delta)),
                icon="🚨",
            )
        if discount_revenue_model is not None and discount_revenue_model["r2"] < 0.3:
            st.warning(t("model_fit_warning"))

        confidence_tone = "ok" if multi_revenue_model["r2"] >= 0.3 else "warn" if multi_revenue_model["r2"] >= 0.15 else "danger"
        confidence_note = (
            t("snapshot_model_strong")
            if multi_revenue_model["r2"] >= 0.3
            else t("snapshot_model_medium")
            if multi_revenue_model["r2"] >= 0.15
            else t("snapshot_model_low")
        )
        sim_signal_cards = [
            {
                "label": t("sim_support_revenue"),
                "value": money(revenue_delta),
                "note": t("predicted_revenue_delta"),
                "tone": "ok" if revenue_delta >= 0 else "danger",
            },
            {
                "label": t("sim_support_orders"),
                "value": f"{orders_delta:,.1f}",
                "note": t("predicted_orders_delta"),
                "tone": "ok" if orders_delta >= 0 else "danger",
            },
            {
                "label": t("sim_support_discount"),
                "value": f"{historical_avg_discount:.2f}% → {new_discount:.2f}%",
                "note": f"{extra_discount:+.0f} {t('delta_points')}",
                "tone": "warn" if extra_discount > 0 else "ok",
            },
            {
                "label": t("sim_support_confidence"),
                "value": f"R² {multi_revenue_model['r2']:.3f}",
                "note": confidence_note,
                "tone": confidence_tone,
            },
        ]
        if marketing_card is not None:
            sim_signal_cards.insert(2, marketing_card)

        st.markdown(
            render_signal_grid(t("sim_key_changes"), sim_signal_cards),
            unsafe_allow_html=True,
        )

        render_model_diagnostics(multi_revenue_model)

        st.markdown(
            f'<div class="detail-muted">{t("multi_model_explanation")}</div>',
            unsafe_allow_html=True,
        )

        sim_df = pd.DataFrame({
            t("col_scenario"): [t("scenario_current"), t("scenario_simulated")],
            t("col_avg_discount"): [historical_avg_discount, new_discount],
            t("col_predicted_revenue"): [rev_now, rev_new],
            t("col_predicted_orders"): [orders_now, orders_new],
        })
        with st.expander(t("sim_detail_table")):
            st.dataframe(sim_df, width="stretch", hide_index=True)

with tab_data:
    st.subheader(t("data_header"))
    quality = pd.DataFrame({
        t("quality_dataset"): ["customers", "orders", "monthly_revenue", "product_summary"],
        t("quality_rows"): [len(customers), len(orders), len(monthly_revenue), len(products)],
        t("quality_columns"): [customers.shape[1], orders.shape[1], monthly_revenue.shape[1], products.shape[1]],
        t("quality_missing"): [
            int(customers.isna().sum().sum()),
            int(orders.isna().sum().sum()),
            int(monthly_revenue.isna().sum().sum()),
            int(products.isna().sum().sum()),
        ],
    })
    st.dataframe(quality, width="stretch", hide_index=True)
    show_cols = [
        "order_id", "customer_id", "order_date", "country", "membership_tier", "category", "product_name",
        "quantity", "discount_pct", "total_amount_usd", "returned", "delivery_days", "customer_rating"
    ]
    st.markdown(f"**{t('filtered_order_data')}**")
    st.dataframe(
        human_table(work[show_cols].sort_values("order_date", ascending=False).head(500)),
        width="stretch",
        hide_index=True,
    )

    csv = work[show_cols].to_csv(index=False).encode("utf-8")
    st.download_button(t("download_csv"), data=csv, file_name="filtered_retail_orders.csv", mime="text/csv")

with tab_log:
    st.subheader(t("log_header"))
    st.write(t("log_note"))
    debug_log = pd.DataFrame([
        {
            t("col_stage"): t("stage_task_decomposition"),
            t("col_problem"): t("problem_task_decomposition"),
            t("col_fix"): t("fix_task_decomposition"),
        },
        {
            t("col_stage"): t("stage_red_error_1"),
            t("col_problem"): t("problem_red_error_1"),
            t("col_fix"): t("fix_red_error_1"),
        },
        {
            t("col_stage"): t("stage_red_error_2"),
            t("col_problem"): t("problem_red_error_2"),
            t("col_fix"): t("fix_red_error_2"),
        },
        {
            t("col_stage"): t("stage_table_ui_fix"),
            t("col_problem"): t("problem_table_ui_fix"),
            t("col_fix"): t("fix_table_ui_fix"),
        },
        {
            t("col_stage"): t("stage_streamlit_api_fix"),
            t("col_problem"): t("problem_streamlit_api_fix"),
            t("col_fix"): t("fix_streamlit_api_fix"),
        },
        {
            t("col_stage"): t("stage_business_guard"),
            t("col_problem"): t("problem_business_guard"),
            t("col_fix"): t("fix_business_guard"),
        },
        {
            t("col_stage"): t("stage_simulator_roi_fix"),
            t("col_problem"): t("problem_simulator_roi_fix"),
            t("col_fix"): t("fix_simulator_roi_fix"),
        },
        {
            t("col_stage"): t("stage_margin_guard_fix"),
            t("col_problem"): t("problem_margin_guard_fix"),
            t("col_fix"): t("fix_margin_guard_fix"),
        },
        {
            t("col_stage"): t("stage_bilingual_guard"),
            t("col_problem"): t("problem_bilingual_guard"),
            t("col_fix"): t("fix_bilingual_guard"),
        },
        {
            t("col_stage"): t("stage_business_diagnosis"),
            t("col_problem"): t("problem_business_diagnosis"),
            t("col_fix"): t("fix_business_diagnosis"),
        },
    ])
    st.dataframe(debug_log, width="stretch", hide_index=True)
    if discount_revenue_model is not None:
        st.markdown(f"**{t('discount_model_limitation_header')}**")
        if discount_revenue_model["r2"] < 0.3:
            st.warning(t("model_fit_warning"))
        st.markdown(t("discount_model_limitation_body").format(r2=discount_revenue_model["r2"]))
    st.markdown(t("demo_script"))
