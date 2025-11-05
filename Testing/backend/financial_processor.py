# backend/financial_processor.py

from typing import List, Dict, Any

# --- Import your custom modules ---
from text_extractor import TextExtractor
from financial_parser import FinancialStatementParser
from financial_analyzer import analyze_profitability, analyze_yoy_growth

# ==============================================================================
# CONFIGURATION & CONSTANTS
# ==============================================================================

# Centralize thresholds for easy tuning. Structure: (threshold, insight_label)
METRIC_THRESHOLDS = {
    "Net Profit Margin": [
        (20, "Excellent"),
        (10, "Healthy"),
        (5, "Average"),
        (0, "Weak")
    ],
    "Gross Margin": [
        (50, "Very Strong"),
        (35, "Strong"),
        (20, "Average"),
        (0, "Weak")
    ],
    "Operating Margin": [
        (25, "Excellent"),
        (15, "Healthy"),
        (10, "Average"),
        (0, "Weak")
    ]
}

CATEGORY_PROFITABILITY = "Profitability"

# ==============================================================================
# RESPONSE STRUCTURE DEFINITION
# ==============================================================================

def _get_response_template() -> Dict[str, Any]:
    """
    Returns a predefined, empty structure for the API response.
    This ensures a consistent format is always sent to the frontend.
    """
    return {
        "filename": "",
        "error": None,
        "ai_analysis": {
            "recommendations": [],
            "strengths": [],
            "weaknesses": []
        },
        "profitability_ratios": [],
        "raw_parsed_data": [],
        "year_over_year_growth": []
    }

# ==============================================================================
# INTERNAL HELPER FUNCTIONS
# ==============================================================================

def _get_qualitative_insight(metric: str, value_str: str) -> str:
    """
    Converts a metric's value into a qualitative insight using the centralized
    METRIC_THRESHOLDS configuration.
    """
    try:
        value = float(value_str.strip('%'))
    except (ValueError, AttributeError):
        return "N/A"

    thresholds = METRIC_THRESHOLDS.get(metric)
    if not thresholds:
        return "Stable"  # Default for metrics without defined thresholds

    for threshold, label in thresholds:
        if value >= threshold:
            return label
            
    # If value is below the lowest threshold (e.g., negative)
    return thresholds[-1][1] if thresholds else "Weak"


def _generate_ai_summary(ratios: List[Dict], growth_metrics: List[Dict]) -> Dict[str, List]:
    """
    Generates the AI analysis object with more contextual defaults.
    """
    strengths, weaknesses, recommendations = [], [], []

    # Handle the edge case where no data is available for analysis
    if not ratios and not growth_metrics:
        return {
            "strengths": [{"title": "Insufficient Data", "description": "Could not generate analysis as no financial metrics were found."}],
            "weaknesses": [{"title": "Insufficient Data", "description": "Could not identify weaknesses without key financial data."}],
            "recommendations": [{"title": "Review Document", "description": "Please ensure the uploaded document is a valid financial statement and try again."}]
        }

    # --- Analyze Year-over-Year Growth ---
    for metric in growth_metrics:
        try:
            growth_value = float(metric['value'].strip('%'))
            metric_name = metric['metric'].replace(' YoY Growth', '')
            if growth_value > 5:
                strengths.append({
                    "title": f"Strong {metric_name} Growth",
                    "description": f"The company shows a healthy {metric['value']} growth in {metric_name}, indicating strong market demand or operational efficiency."
                })
            elif growth_value < 0:
                weaknesses.append({
                    "title": f"Decline in {metric_name}",
                    "description": f"A decline of {metric['value']} in {metric_name} is a key concern that may signal market challenges or internal issues."
                })
                recommendations.append({
                    "title": f"Investigate {metric_name} Decline",
                    "description": f"Analyze the root causes for the drop in {metric_name.lower()} (e.g., competition, pricing, market saturation) and develop a targeted strategy to reverse the trend."
                })
        except (ValueError, KeyError):
            continue

    # --- Analyze Profitability Ratios (using the latest year's data) ---
    latest_year = max([r['year'] for r in ratios], default=0)
    latest_ratios = [r for r in ratios if r['year'] == latest_year]

    for ratio in latest_ratios:
        if ratio['insight'] in ["Excellent", "Very Strong", "Strong"]:
            strengths.append({
                "title": f"High {ratio['metric']}",
                "description": f"A {ratio['metric']} of {ratio['value']} is considered {ratio['insight'].lower()}, pointing to efficient cost management and strong pricing power."
            })
        elif ratio['insight'] == "Weak":
            weaknesses.append({
                "title": f"Low {ratio['metric']}",
                "description": f"The {ratio['metric']} of {ratio['value']} is weak. This could suggest high operating costs, intense price competition, or inefficient operations."
            })
            recommendations.append({
                "title": f"Improve {ratio['metric']}",
                "description": f"Conduct a detailed review of the cost of goods sold (for Gross Margin) or operating expenses (for Operating/Net Margin) to identify areas for cost reduction."
            })

    # --- Add smarter, more helpful default messages if lists are empty ---
    if not strengths:
        strengths.append({
            "title": "No Standout Strengths Identified",
            "description": "Based on the available data, no metrics met the criteria for a significant strength. The company's performance appears stable but lacks strong growth or high profitability indicators."
        })
    if not weaknesses:
        weaknesses.append({
            "title": "No Significant Weaknesses Detected",
            "description": "The analysis did not flag any key metrics as significant weaknesses from the provided data, suggesting a solid and stable financial footing."
        })
    if not recommendations:
        recommendations.append({
            "title": "General Financial Best Practices",
            "description": "Continuously monitor key financial ratios, manage cash flow effectively, and explore opportunities for strategic cost optimization and sustainable revenue growth."
        })

    return {"strengths": strengths, "weaknesses": weaknesses, "recommendations": recommendations}

# ==============================================================================
# PUBLIC PROCESSING FUNCTION (THE ORCHESTRATOR)
# ==============================================================================

def process_financial_document(filepath: str, filename: str) -> Dict[str, Any]:
    """
    Orchestrates the full analysis pipeline from file to final JSON.
    This function acts as the core business logic controller.
    """
    # Step 1: Initialize the response using the template for consistency
    response = _get_response_template()
    response["filename"] = filename

    try:
        # Step 2: Extract text from the document
        print("INFO: Starting text extraction...")
        extractor = TextExtractor()
        extracted_text = extractor.extract_text(filepath)
        if extracted_text.startswith("[Error:"):
            response["error"] = f"Failed to extract text: {extracted_text}"
            return response

        # Step 3: Parse the extracted text into structured financial data
        print("INFO: Starting financial parsing...")
        parser = FinancialStatementParser(extracted_text)
        parsed_data = parser.parse()
        if not parsed_data:
            response["error"] = "Could not parse financial statements from the document."
            return response
        
        response["raw_parsed_data"] = parsed_data
        print("SUCCESS: Extraction and parsing complete.")

        # Step 4: Perform financial analysis on the structured data
        print("INFO: Running financial analysis...")
        profitability_insights = analyze_profitability(parsed_data)
        growth_insights = analyze_yoy_growth(parsed_data)
        response["year_over_year_growth"] = growth_insights
        
        # Step 5: Transform raw analysis into the frontend-specific format
        print("INFO: Transforming data for frontend...")
        transformed_ratios = [
            {
                "category": CATEGORY_PROFITABILITY,
                "metric": ratio["metric"],
                "value": ratio["value"],
                "year": ratio.get("year"),
                "insight": _get_qualitative_insight(ratio["metric"], ratio["value"])
            } for ratio in profitability_insights
        ]
        response["profitability_ratios"] = transformed_ratios

        # Step 6: Generate the final AI-powered summary
        ai_summary = _generate_ai_summary(transformed_ratios, growth_insights)
        response["ai_analysis"] = ai_summary
        
        print("SUCCESS: Analysis and transformation complete.")

    except Exception as e:
        print(f"CRITICAL: An unexpected error occurred during processing: {str(e)}")
        response["error"] = f"An internal server error occurred: {str(e)}"

    return response