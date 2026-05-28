# Pandas Analysis Notes

## Data tables

1. `customers.csv`: customer-level profile, membership, behavior, churn label.
2. `orders.csv`: order-level transaction data, discount, revenue, delivery, return, rating.
3. `product_summary.csv`: product-level total orders, revenue, rating, return rate, discount, delivery days.

## Cleaning logic

```python
customers = pd.read_csv("customers.csv")
orders = pd.read_csv("orders.csv")
products = pd.read_csv("product_summary.csv")

customers["registration_date"] = pd.to_datetime(customers["registration_date"])
orders["order_date"] = pd.to_datetime(orders["order_date"])
orders["delivery_date"] = pd.to_datetime(orders["delivery_date"])

customers = customers.drop_duplicates(subset=["customer_id"])
orders = orders.drop_duplicates(subset=["order_id"])
orders["rating_missing"] = orders["customer_rating"].isna().astype(int)
orders["customer_rating"] = orders["customer_rating"].fillna(orders["customer_rating"].median())
merged = orders.merge(customers, on="customer_id", how="left")
```

## Important findings from the uploaded data

- Total revenue: $3,136,404.66
- Orders: 25,000
- Customers: 8,000
- Product rows: 140
- Average order value: $125.46
- Return rate: 8.08%
- Date range: 2020-01-01 to 2026-03-30
- Missing order ratings: 15,749. This should be explained as missing reviews, not bad reviews.
- Highest-revenue category: Electronics ($1,148,937.00)

## Model explanation

The app uses simple linear regression because the PPT asks for slope and R². The main model is:

```text
monthly_revenue = slope × average_discount_percentage + intercept
```

This model is intentionally transparent. A low R² is not hidden. If R² is low, the app displays a warning and tells the presenter to explain that discount alone cannot fully explain revenue.

## Business interpretation

Good management language:

> The simulator is not a magic answer machine. It is a risk-control tool. If the discount slider creates negative profit, low R², or out-of-range predictions, the system warns the manager before money is spent.
