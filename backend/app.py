# backend/app.py
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename

# --- Import the core processing logic ---
from financial_processor import process_financial_document, _get_response_template

# --- Basic Setup ---
app = Flask(__name__)
CORS(app)

# --- Configuration ---
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# --- API Endpoints ---
@app.route('/api/process-document', methods=['POST'])
def upload_and_process_file():
    """
    Handles file upload and calls the core processing pipeline.
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

        # --- Call the core logic from the other file ---
        analysis_result = process_financial_document(filepath, filename)

        # --- Check for processing errors within the structured response ---
        if analysis_result.get("error"):
            # A processing error occurred (e.g., parsing failed)
            # We still return the full structure, but with an error code.
            return jsonify(analysis_result), 422 # Unprocessable Entity
        
        # --- On success, return the full analysis ---
        return jsonify(analysis_result), 200

    except Exception as e:
        # This catches server-level errors (e.g., disk full, unexpected crashes)
        print(f"CRITICAL: An unexpected error occurred in the web layer: {str(e)}")
        # For these critical errors, we can create a structured response on the fly
        error_response = _get_response_template()
        error_response["filename"] = filename
        error_response["error"] = f"An unexpected server error occurred: {str(e)}"
        return jsonify(error_response), 500
    finally:
        # Ensure the temporary file is always cleaned up
        if os.path.exists(filepath):
            os.remove(filepath)
            print(f"INFO: Cleaned up temporary file '{filename}'.")

@app.route('/health', methods=['GET'])
def health_check():
    """A simple health check endpoint."""
    return jsonify({"status": "ok", "message": "Backend is running!"}), 200

# --- Run the App ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)