# Retail AI Decision Support System — Stlite Project

This package contains a browser-based Streamlit/stlite website for the uploaded e-commerce CSV data.

## How to run

### Option A — easiest
Open `index.html` in a modern desktop browser with internet access. It loads stlite from CDN and runs Python in the browser.

### Option B — safer local preview
From this folder, run:

```bash
python3 -m http.server 8000
```

Then open:

```text
http://localhost:8000/index.html
```

## Files

- `index.html`: self-contained stlite web app launcher with embedded CSV data.
- `streamlit_app.py`: readable Streamlit app source code.
- `data/customers.csv`: customer profile data.
- `data/orders.csv`: order transaction data.
- `data/product_summary.csv`: product-level summary data.
- `PROJECT_PLAN.md`: project schedule and PPT-aligned task plan.
- `analysis_notes.md`: pandas analysis strategy and important findings.
- `debug_log.md`: prompt/debug log sample for the final report.

## Data summary

- Customers: 8,000 rows
- Orders: 25,000 rows
- Product summary: 140 rows
- Order date range: 2020-01-01 to 2026-03-30
- Total revenue: $3,136,404.66
- Average order value: $125.46
- Return rate: 8.08%
- Missing customer ratings in orders: 15,749 cells. These are treated as missing reviews, not low ratings.
- Highest-revenue category: Electronics ($1,148,937.00)
