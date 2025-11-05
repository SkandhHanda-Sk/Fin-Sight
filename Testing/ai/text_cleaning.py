import pandas as pd
import re
from extract import *

# 🧾 Paste your OCR-extracted text here
# text = """
# Year Ended June 30, 2024 2023 2022
# Revenue:
# Product $ 64,773 $ 64,699 $ 72,732
# Service and other 180,349 147,216 125,538
# Total revenue 245,122 211,915 198,270
# Cost of revenue:
# Product 15,272 17,804 19,064
# Service and other 58,842 48,059 43,586
# Total cost of revenue 74,114 65,863 62,650
# Gross margin 171,008 146,052 135,620
# Research and development 29,510 27,195 24,512
# Sales and marketing 24,456 22,759 21,825
# General and administrative 7,609 7,575 5,900
# Operating income 109,433 88,523 83,383
# Interest expense (18,177) (17,050) (15,900)
# Income before income taxes 107,787 89,311 83,716
# Provision for income taxes 19,651 16,950 10,978
# Net income $ 88,136 $ 72,361 $ 72,738
# Earnings per share:
# Basic $ 11.86 $ 9.72 $ 9.70
# """
text=extract_text_from_image("/home/shubhankar/Downloads/Screenshot2024-09-01at2.45.30PM-a3919a880bbc472687252c4e1f4b2e98.png")

# 🎯 1. Define the key metrics and their synonyms
metric_map = {
    "Net Sales (Revenue)": [r"total revenue", r"net sales", r"revenue"],
    "Cost of Goods Sold (COGS)": [r"cost of revenue", r"cost of sales", r"cogs"],
    "Gross Profit": [r"gross profit", r"gross margin"],
    "Operating Expenses": [r"total operating expenses", r"operating expenses"],
    "Operating Income (EBIT)": [r"operating income", r"ebit"],
    "Interest Expense": [r"interest expense"],
    "Earnings Before Tax (EBT)": [r"income before tax", r"earnings before tax", r"income before income taxes"],
    "Income Tax Expense": [r"income tax", r"tax expense", r"provision for income taxes"],
    "Net Income": [r"net income", r"net earnings"],
    "Earnings Per Share (EPS)": [r"earnings per share", r"eps"],
}

# 🎯 2. Extract years
year_line = re.search(r'Year Ended.*?((?:19|20)\d{2}.*)', text)
years = re.findall(r'(?:19|20)\d{2}', year_line.group(1)) if year_line else ["Value"]

# 🎯 3. Extract lines containing numbers
lines = [l.strip() for l in text.splitlines() if re.search(r'\d', l)]

data = []

for line in lines:
    if 'Year Ended' in line:
        continue

    # Clean line and find numbers
    clean_line = line.replace('§', '').replace('$', '').replace(',', '')
    values = re.findall(r'\(?-?[\d\.]+\)?', clean_line)
    if not values:
        continue

    # Extract metric (text before first number)
    metric = re.split(r'\(?-?[\d\.]+\)?', clean_line, maxsplit=1)[0].strip(': ').lower()

    # Convert numbers to floats
    cleaned_vals = []
    for v in values:
        v = v.replace('(', '-').replace(')', '')
        try:
            cleaned_vals.append(float(v))
        except ValueError:
            cleaned_vals.append(None)

    # Pad values if needed
    while len(cleaned_vals) < len(years):
        cleaned_vals.append(None)

    data.append((metric, cleaned_vals))

# 🎯 4. Match extracted metrics to your desired standard list
final_data = []

for std_name, patterns in metric_map.items():
    found = False
    for metric, vals in data:
        for pattern in patterns:
            if re.search(pattern, metric):
                final_data.append([std_name] + vals[:len(years)])
                found = True
                break
        if found:
            break
    if not found:
        final_data.append([std_name] + [None] * len(years))  # placeholder if missing

# 🎯 5. Create final DataFrame
df = pd.DataFrame(final_data, columns=["Metric"] + years)

# 🎯 6. Export to Excel and CSV
df.to_excel("financial_summary.xlsx", index=False)
df.to_csv("financial_summary.csv", index=False)

print(df)
print("\n✅ Saved as 'financial_summary.xlsx' and 'financial_summary.csv'")
