# app.py
import os
import json
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# --- Import your custom modules ---
# These imports assume the files are in the same directory as app.py
from text_extractor import TextExtractor
from financial_parser import FinancialStatementParser
from financial_analyzer import analyze_profitability, analyze_yoy_growth

# --- Basic Setup ---
app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing for web frontends

# --- Configuration ---
# Define a folder to temporarily store uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- The Core API Endpoint ---
@app.route('/api/process-document', methods=['POST'])
def upload_and_process_file():
    """
    Handles file upload and orchestrates the full pipeline:
    1. Extracts text from the document.
    2. Parses the text to find financial data.
    3. Analyzes the data to generate insights.
    4. Returns the final analysis as a JSON response.
    """
    # --- Step 1: Handle the File Upload ---
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No file selected for upload"}), 400

    if not file:
        return jsonify({"error": "Invalid file provided"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    
    try:
        file.save(filepath)

        # --- Step 2: Extract Text from the Document ---
        print(f"INFO: Starting text extraction for '{filename}'...")
        extractor = TextExtractor()
        extracted_text = extractor.extract_text(filepath)
        
        if extracted_text.startswith("[Error:"):
            print(f"ERROR: Text extraction failed. Reason: {extracted_text}")
            return jsonify({"error": f"Failed to extract text: {extracted_text}"}), 500
        
        print("SUCCESS: Text extraction complete.")

        # --- Step 3: Parse the Extracted Text ---
        print("INFO: Starting financial data parsing...")
        parser = FinancialStatementParser(extracted_text)
        parsed_data = parser.parse()

        if not parsed_data:
            print("ERROR: Parsing failed. No financial data could be structured.")
            return jsonify({"error": "Could not parse financial statements from the document."}), 404
            
        print("SUCCESS: Financial data parsed.")

        # --- Step 4: Analyze the Parsed Data ---
        print("INFO: Running financial analysis...")
        profitability_insights = analyze_profitability(parsed_data)
        growth_insights = analyze_yoy_growth(parsed_data)
        
        final_analysis = {
            "filename": filename,
            "profitability_ratios": profitability_insights,
            "year_over_year_growth": growth_insights,
            "raw_parsed_data": parsed_data # Optionally include the raw data
        }
        print("SUCCESS: Analysis complete.")

        # --- Step 5: Return the Final Result ---
        return jsonify(final_analysis)

    except Exception as e:
        # Catch-all for any unexpected errors during the process
        print(f"CRITICAL: An unexpected error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected server error occurred: {str(e)}"}), 500
    finally:
        # --- Cleanup: Remove the temporary file ---
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"INFO: Cleaned up temporary file '{filename}'.")

# A simple health check endpoint to verify the server is running
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "message": "Backend is running!"}), 200

# --- Run the App ---
if __name__ == '__main__':
    # Runs on 0.0.0.0 to be accessible on your local network
    # Debug mode is on for development, turn off for production
    app.run(host='0.0.0.0', port=5001, debug=True)