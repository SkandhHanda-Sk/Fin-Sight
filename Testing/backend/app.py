# backend/app.py
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# --- Import your custom modules ---
from text_extractor import TextExtractor
from financial_parser import FinancialStatementParser
from financial_analyzer import analyze_profitability, analyze_yoy_growth

# --- Basic Setup ---
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# ==============================================================================
# NEW HELPER FUNCTIONS TO GENERATE FRONTEND-COMPATIBLE DATA
# ==============================================================================

def get_qualitative_insight(metric, value_str):
    """
    Converts a metric's value into a simple qualitative insight.
    This replaces the long definitions with short, UI-friendly statuses.
    """
    try:
        # Convert percentage string to float
        value = float(value_str.strip('%'))
    except ValueError:
        return "N/A" # Handle non-percentage values if any

    if metric == "Net Profit Margin":
        if value > 20: return "Excellent"
        if value > 10: return "Healthy"
        if value > 5: return "Average"
        return "Weak"
    elif metric == "Gross Margin":
        if value > 50: return "Very Strong"
        if value > 35: return "Strong"
        if value > 20: return "Average"
        return "Weak"
    elif metric == "Operating Margin":
        if value > 25: return "Excellent"
        if value > 15: return "Healthy"
        if value > 10: return "Average"
        return "Weak"
    # Add more rules for other metrics as needed
    return "Stable"

def generate_ai_summary(ratios, growth_metrics):
    """
    Generates the AI analysis object (strengths, weaknesses, recommendations)
    based on the processed financial data.
    """
    strengths = []
    weaknesses = []
    recommendations = []

    # Analyze Year-over-Year Growth
    for metric in growth_metrics:
        try:
            growth_value = float(metric['value'].strip('%'))
            if growth_value > 5:
                strengths.append({
                    "title": f"Strong {metric['metric']}",
                    "description": f"The company shows a healthy {metric['value']} growth in {metric['metric'].replace(' YoY Growth', '')}, indicating strong performance."
                })
            elif growth_value < 0:
                weaknesses.append({
                    "title": f"Decline in {metric['metric']}",
                    "description": f"There was a decline of {metric['value']} in {metric['metric'].replace(' YoY Growth', '')}, which needs investigation."
                })
                recommendations.append({
                    "title": f"Address {metric['metric'].replace(' YoY Growth', '')} Decline",
                    "description": "Investigate the root causes for the drop in sales/income and develop strategies to reverse the trend."
                })
        except (ValueError, KeyError):
            continue # Skip if value is not a valid percentage

    # Analyze Profitability Ratios (using the latest year's data)
    latest_year = max([r['year'] for r in ratios]) if ratios else 0
    latest_ratios = [r for r in ratios if r['year'] == latest_year]

    for ratio in latest_ratios:
        if ratio['insight'] in ["Excellent", "Very Strong", "Strong"]:
            strengths.append({
                "title": f"High {ratio['metric']}",
                "description": f"A {ratio['metric']} of {ratio['value']} is considered {ratio['insight'].lower()}, pointing to efficient operations and strong pricing power."
            })
        elif ratio['insight'] == "Weak":
            weaknesses.append({
                "title": f"Low {ratio['metric']}",
                "description": f"The {ratio['metric']} of {ratio['value']} is weak, suggesting potential issues with cost control or pricing strategy."
            })
            recommendations.append({
                "title": f"Improve {ratio['metric']}",
                "description": f"Analyze cost structures and pricing to improve the {ratio['metric']} and boost overall profitability."
            })

    # Default messages if no specific insights are found
    if not strengths:
        strengths.append({"title": "Stable Operations", "description": "The company maintains a stable operational profile."})
    if not weaknesses:
        weaknesses.append({"title": "No Major Weaknesses Detected", "description": "No significant financial weaknesses were identified from the available data."})
    if not recommendations:
        recommendations.append({"title": "Continue Monitoring", "description": "Continue to monitor key performance indicators and market trends."})

    return {
        "strengths": strengths,
        "weaknesses": weaknesses,
        "recommendations": recommendations
    }


# --- The Core API Endpoint ---
@app.route('/api/process-document', methods=['POST'])
def upload_and_process_file():
    """
    Handles file upload and orchestrates the full pipeline.
    """
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for upload"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)

        # --- Step 1 & 2: Extract and Parse ---
        print("INFO: Starting text extraction and parsing...")
        extractor = TextExtractor()
        extracted_text = extractor.extract_text(filepath)
        if extracted_text.startswith("[Error:"):
            return jsonify({"error": f"Failed to extract text: {extracted_text}"}), 500
        
        parser = FinancialStatementParser(extracted_text)
        parsed_data = parser.parse()
        if not parsed_data:
            return jsonify({"error": "Could not parse financial statements."}), 404
        print("SUCCESS: Extraction and parsing complete.")

        # --- Step 3: Analyze the Parsed Data ---
        print("INFO: Running financial analysis...")
        profitability_insights = analyze_profitability(parsed_data)
        growth_insights = analyze_yoy_growth(parsed_data)
        
        # --- Step 4: Transform Data and Generate AI Summary for Frontend ---
        print("INFO: Transforming data for frontend...")
        
        # 4a. Transform profitability ratios to match frontend expectations
        transformed_ratios = []
        for ratio in profitability_insights:
            transformed_ratios.append({
                "category": "Profitability",  # Add the missing 'category' field
                "metric": ratio["metric"],
                "value": ratio["value"],
                "year": ratio.get("year"), # Use .get for safety
                # Replace definition with a qualitative insight
                "insight": get_qualitative_insight(ratio["metric"], ratio["value"])
            })

        # 4b. Generate the missing ai_analysis object
        ai_summary = generate_ai_summary(transformed_ratios, growth_insights)

        # --- Step 5: Assemble the Final JSON Response ---
        final_analysis = {
            "filename": filename,
            "profitability_ratios": transformed_ratios, # Use the transformed data
            "year_over_year_growth": growth_insights,
            "ai_analysis": ai_summary, # Add the newly generated AI summary
            "raw_parsed_data": parsed_data
        }
        print("SUCCESS: Analysis and transformation complete.")

        return jsonify(final_analysis)

    except Exception as e:
        print(f"CRITICAL: An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500
    finally:
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"INFO: Cleaned up temporary file '{filename}'.")

# Health check endpoint
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend is running!"}), 200

# --- Run the App ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)