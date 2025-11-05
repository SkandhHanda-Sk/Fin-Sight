import pandas as pd

# Load the cleaned financial data
df = pd.read_excel("financial_summary.xlsx")

# Convert numeric columns to float
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Helper to get metric values
def get(metric):
    row = df[df["Metric"] == metric]
    return row.iloc[0, 1:].values if not row.empty else [None] * (len(df.columns) - 1)

years = df.columns[1:]
revenue = get("Net Sales (Revenue)")
gross_profit = get("Gross Profit")
operating_income = get("Operating Income (EBIT)")
net_income = get("Net Income")
cogs = get("Cost of Goods Sold (COGS)")
ebt = get("Earnings Before Tax (EBT)")
interest = get("Interest Expense")

# 💰 Profitability Ratios
profitability = {
    "Gross Profit Margin (%)": [gp / rev * 100 if rev else None for gp, rev in zip(gross_profit, revenue)],
    "Operating Profit Margin (%)": [op / rev * 100 if rev else None for op, rev in zip(operating_income, revenue)],
    "Net Profit Margin (%)": [ni / rev * 100 if rev else None for ni, rev in zip(net_income, revenue)],
    "Return on Sales (EBT/Revenue) (%)": [e / rev * 100 if rev else None for e, rev in zip(ebt, revenue)],
}

# 🧭 Stability Ratios (Operational efficiency / cost structure)
stability = {
    "COGS Ratio (%)": [c / rev * 100 if rev else None for c, rev in zip(cogs, revenue)],
    "Operating Expense Ratio (%)": [
        (rev - gp - op) / rev * 100 if rev and gp and op else None
        for rev, gp, op in zip(revenue, gross_profit, operating_income)
    ],
}

# 💸 Debt Ratios (based on Interest coverage etc.)
debt = {
    "Interest Coverage Ratio (EBIT/Interest)": [
        op / abs(i) if i and i != 0 else None for op, i in zip(operating_income, interest)
    ],
    "Debt Service Ratio (EBT/Interest)": [
        e / abs(i) if i and i != 0 else None for e, i in zip(ebt, interest)
    ],
}

# Combine results
all_ratios = {**profitability, **stability, **debt}
ratio_df = pd.DataFrame(all_ratios, index=years).T.reset_index()
ratio_df.rename(columns={"index": "Ratio"}, inplace=True)

print("\n📊 FINANCIAL RATIOS\n")
print(ratio_df)

# Save to Excel
#ratio_df.to_excel("financial_ratios.xlsx", index=False)
print("\n✅ Saved as 'financial_ratios.xlsx'")
