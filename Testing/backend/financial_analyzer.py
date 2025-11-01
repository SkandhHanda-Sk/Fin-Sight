import json

def load_financial_data(filepath):
    """Loads the parsed financial data from a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: The file was not found at '{filepath}'")
        return None
    except json.JSONDecodeError:
        print(f"Error: Could not decode the JSON file at '{filepath}'")
        return None

def analyze_profitability(data):
    """Calculates key profitability ratios for annual periods."""
    
    insights = []
    
    # Filter for only annual data to perform YoY analysis
    annual_data = sorted([d for d in data if d['period_type'] == 'annual'], key=lambda x: x['year'])

    for period_data in annual_data:
        year = period_data['year']
        total_sales = period_data.get('total_net_sales', 0)
        gross_margin_value = period_data.get('gross_margin', 0)
        operating_income = period_data.get('operating_income', 0)
        net_income = period_data.get('net_income', 0)

        # Avoid division by zero
        if total_sales == 0:
            continue

        # Calculate Ratios
        gross_margin_percent = (gross_margin_value / total_sales) * 100
        operating_margin_percent = (operating_income / total_sales) * 100
        net_profit_margin_percent = (net_income / total_sales) * 100

        insights.append({
            'year': year,
            'metric': 'Gross Margin',
            'value': f"{gross_margin_percent:.2f}%",
            'insight': 'Percentage of revenue left after accounting for the cost of goods sold.'
        })
        insights.append({
            'year': year,
            'metric': 'Operating Margin',
            'value': f"{operating_margin_percent:.2f}%",
            'insight': 'Measures how much profit a company makes on a dollar of sales, after paying for variable costs of production but before paying interest or tax.'
        })
        insights.append({
            'year': year,
            'metric': 'Net Profit Margin',
            'value': f"{net_profit_margin_percent:.2f}%",
            'insight': 'The ultimate measure of profitability, showing how much of each dollar in revenue is translated into profit.'
        })
        
    return insights

def analyze_yoy_growth(data):
    """Calculates Year-over-Year growth for key metrics."""
    insights = []
    
    annual_data = sorted([d for d in data if d['period_type'] == 'annual'], key=lambda x: x['year'])
    
    # Need at least two years to calculate growth
    if len(annual_data) < 2:
        return []

    # Compare the last two years
    previous_year_data = annual_data[-2]
    current_year_data = annual_data[-1]

    metrics_to_compare = ['total_net_sales', 'operating_income', 'net_income']

    for metric in metrics_to_compare:
        prev_value = previous_year_data.get(metric)
        curr_value = current_year_data.get(metric)

        if prev_value and curr_value and prev_value != 0:
            growth_percent = ((curr_value - prev_value) / prev_value) * 100
            insights.append({
                'metric': f"{metric.replace('_', ' ').title()} YoY Growth",
                'value': f"{growth_percent:.2f}%",
                'period': f"{previous_year_data['year']} vs {current_year_data['year']}"
            })
            
    return insights


if __name__ == '__main__':
    # 1. Load the clean data
    financial_data = load_financial_data('output/parsed_financials.json')

    if financial_data:
        # 2. Run different analyses
        profitability_insights = analyze_profitability(financial_data)
        growth_insights = analyze_yoy_growth(financial_data)
        
        # 3. Combine and present the results
        final_results = {
            "profitability_ratios": profitability_insights,
            "year_over_year_growth": growth_insights
        }

        print("--- Financial Analysis Results ---")
        print(json.dumps(final_results, indent=4))
        
        # In your real application, this `final_results` dictionary is what you would
        # send to the front-end UI for display.