import pandas as pd

def analyze_trend(values):
    """Return a simple trend: improving, declining, or stable."""
    if values[0] is None or len(values) < 2:
        return "Insufficient data"
    if values[-1] > values[0] * 1.02:
        return "improving"
    elif values[-1] < values[0] * 0.98:
        return "declining"
    else:
        return "stable"

# Load the ratio data
df = pd.read_excel("financial_ratios.xlsx")

# Convert all columns except 'Ratio' to numeric
for col in df.columns[1:]:
    df[col] = pd.to_numeric(df[col], errors='coerce')

years = df.columns[1:]

analysis = []

for _, row in df.iterrows():
    ratio_name = row["Ratio"]
    values = [row[year] for year in years if not pd.isna(row[year])]

    if not values:
        continue

    trend = analyze_trend(values)
    avg_val = sum(values) / len(values)

    comment = ""
    if "Gross Profit Margin" in ratio_name:
        comment = f"Gross margin averages {avg_val:.2f}%, indicating {'strong' if avg_val > 60 else 'moderate'} profitability and {trend} trend."
    elif "Operating Profit Margin" in ratio_name:
        comment = f"Operating margin averages {avg_val:.2f}%, showing {'efficient' if avg_val > 40 else 'average'} cost control and {trend} performance."
    elif "Net Profit Margin" in ratio_name:
        comment = f"Net profit margin averages {avg_val:.2f}%, which is {'excellent' if avg_val > 30 else 'average'}; trend is {trend}."
    elif "Return on Sales" in ratio_name:
        comment = f"Return on Sales at an average of {avg_val:.2f}% reflects {'strong' if avg_val > 35 else 'moderate'} profitability."
    elif "COGS Ratio" in ratio_name:
        comment = f"COGS ratio averages {avg_val:.2f}%, suggesting {'efficient production' if avg_val < 40 else 'high costs'}. Trend: {trend}."
    elif "Operating Expense Ratio" in ratio_name:
        comment = f"Operating expense ratio averages {avg_val:.2f}%. Lower values indicate good control over overheads ({trend})."
    elif "Interest Coverage" in ratio_name:
        comment = f"Interest coverage is {'very healthy' if avg_val and avg_val > 10 else 'weak or missing'}. Trend: {trend}."
    elif "Debt Service" in ratio_name:
        comment = f"Debt service ratio averages {avg_val:.2f}, showing the company’s ability to pay interest from profits."

    analysis.append((ratio_name, avg_val, trend, comment))

# Convert to DataFrame
analysis_df = pd.DataFrame(analysis, columns=["Ratio", "Average Value", "Trend", "Comment"])
print("\n📈 FINANCIAL PERFORMANCE ANALYSIS\n")
print(analysis_df[["Ratio", "Comment"]])

# Save to Excel
analysis_df.to_excel("ratio_analysis.xlsx", index=False)
#print("\n✅ Analysis saved as 'ratio_analysis.xlsx'")

# Overall summary
profitability = analysis_df[analysis_df["Ratio"].str.contains("Profit|Sales")]
avg_profitability = profitability["Average Value"].mean()

if avg_profitability > 30:
    print("\n💹 Overall: The company shows **strong profitability** and efficient operations.")
elif avg_profitability > 20:
    print("\n💹 Overall: The company maintains **moderate profitability** with room for margin improvement.")
else:
    print("\n💹 Overall: The company’s profitability appears **weak**, cost control or pricing strategy may need attention.")
import matplotlib.pyplot as plt

# Re-load ratio data (or keep df if already in memory)
ratio_df = pd.read_excel("financial_ratios.xlsx")

# Convert numeric columns
for col in ratio_df.columns[1:]:
    ratio_df[col] = pd.to_numeric(ratio_df[col], errors='coerce')

# Create a bar chart for each ratio
for _, row in ratio_df.iterrows():
    ratio_name = row["Ratio"]
    values = row[1:].values
    years = ratio_df.columns[1:]

    plt.figure()
    plt.bar(years, values)
    plt.title(f"{ratio_name} Across Years")
    plt.xlabel("Year")
    plt.ylabel(ratio_name)
    plt.tight_layout()
    plt.savefig(f"{ratio_name.replace(' ', '_')}.png")  # save each graph
    # plt.show()  # uncomment if you want to see on screen

