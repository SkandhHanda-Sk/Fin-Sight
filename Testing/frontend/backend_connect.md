Here is a complete, step-by-step guide on how to connect a React website to your `app.py` server.

### The Core Concept

1.  **Backend Server:** Your Flask `app.py` runs on a specific address and port (e.g., `http://localhost:5001`). It listens for incoming HTTP requests at defined routes (`/api/process-document`).
2.  **Frontend Client:** Your React app runs in the user's web browser (usually on a different port during development, like `http://localhost:3000`).
3.  **The Connection:** The React app will use a browser API (like `fetch` or a library like `axios`) to send an HTTP `POST` request to the Flask server's URL. This request will include the file the user selected.
4.  **Data Flow:**
    *   User selects a file in the React UI.
    *   React packages this file into a `FormData` object.
    *   React sends a `POST` request with the `FormData` to `http://localhost:5001/api/process-document`.
    *   Flask receives the request, processes the file, and generates the analysis.
    *   Flask sends back a JSON response (either the analysis data or an error message).
    *   React receives the JSON response, updates its state, and displays the results or the error to the user.

Your Flask server is already perfectly set up for this because it includes `flask_cors`, which handles the security policy (Cross-Origin Resource Sharing) that allows a web page from one origin (`localhost:3000`) to request data from another (`localhost:5001`).

---

### Step 1: Run Your Flask Backend

First, make sure your backend server is running. Open a terminal, navigate to the directory containing `app.py` and your other Python modules, and run it:

```bash
# Make sure you have Flask and other dependencies installed
# pip install Flask Flask-Cors werkzeug PyPDF2 python-docx

python app.py
```

You should see output indicating the server is running, something like:

```
 * Running on http://0.0.0.0:5001/
 * Debug mode: on
```

This means your API is now live and listening for requests at `http://localhost:5001`.

---

### Step 2: Create and Set Up the React Frontend

If you don't have a React app yet, create one using Create React App.

1.  **Create the App:** Open a *new* terminal window (leave the Flask server running in the other one).

    ```bash
    npx create-react-app financial-analyzer-ui
    cd financial-analyzer-ui
    ```

2.  **Replace the Code in `src/App.js`:** This is where we'll write the code to interact with your Flask API. Replace the entire content of `src/App.js` with the following:

    ```javascript
    // src/App.js
    import React, { useState } from 'react';
    import './App.css';

    function App() {
      // State variables to manage the UI
      const [selectedFile, setSelectedFile] = useState(null);
      const [analysisResult, setAnalysisResult] = useState(null);
      const [error, setError] = useState('');
      const [isLoading, setIsLoading] = useState(false);

      // Function to handle file selection from the input
      const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
        // Reset previous results when a new file is selected
        setAnalysisResult(null);
        setError('');
      };

      // Function to handle the form submission
      const handleSubmit = async (event) => {
        event.preventDefault(); // Prevent the default form submission

        if (!selectedFile) {
          setError('Please select a file first.');
          return;
        }

        // Set loading state and clear previous errors/results
        setIsLoading(true);
        setError('');
        setAnalysisResult(null);

        // Use FormData to send the file
        const formData = new FormData();
        formData.append('file', selectedFile); // The key 'file' must match the key in your Flask app

        try {
          // The API call to your Flask server
          const response = await fetch('http://localhost:5001/api/process-document', {
            method: 'POST',
            body: formData,
            // IMPORTANT: Do not set 'Content-Type' header yourself.
            // The browser will automatically set it to 'multipart/form-data'
            // with the correct boundary when you use FormData.
          });

          if (!response.ok) {
            // If the server response is not OK, parse the error
            const errorData = await response.json();
            throw new Error(errorData.error || `Server responded with status: ${response.status}`);
          }

          // If the response is OK, parse the JSON data
          const data = await response.json();
          setAnalysisResult(data);

        } catch (err) {
          // Handle network errors or errors from the server
          console.error("Error during API call:", err);
          setError(err.message);
        } finally {
          // Always stop loading, whether it succeeded or failed
          setIsLoading(false);
        }
      };

      return (
        <div className="App">
          <header className="App-header">
            <h1>Financial Document Analyzer</h1>
            <p>Upload a PDF or DOCX file to analyze its financial statements.</p>
          </header>
          <main>
            <form onSubmit={handleSubmit} className="upload-form">
              <input type="file" onChange={handleFileChange} accept=".pdf,.docx" />
              <button type="submit" disabled={isLoading || !selectedFile}>
                {isLoading ? 'Analyzing...' : 'Analyze Document'}
              </button>
            </form>

            {/* Display loading spinner */}
            {isLoading && <div className="loader"></div>}

            {/* Display error messages */}
            {error && <div className="error-message">Error: {error}</div>}

            {/* Display the analysis result */}
            {analysisResult && (
              <div className="results">
                <h2>Analysis for: {analysisResult.filename}</h2>
                <div className="result-section">
                  <h3>Profitability Ratios</h3>
                  <pre>{JSON.stringify(analysisResult.profitability_ratios, null, 2)}</pre>
                </div>
                <div className="result-section">
                  <h3>Year-over-Year Growth</h3>
                  <pre>{JSON.stringify(analysisResult.year_over_year_growth, null, 2)}</pre>
                </div>
                <div className="result-section">
                  <h3>Raw Parsed Data</h3>
                  <pre>{JSON.stringify(analysisResult.raw_parsed_data, null, 2)}</pre>
                </div>
              </div>
            )}
          </main>
        </div>
      );
    }

    export default App;
    ```

3.  **Add Some Basic Styling in `src/App.css`:** Replace the content of `src/App.css` with this to make it look decent.

    ```css
    /* src/App.css */
    body {
      background-color: #f0f2f5;
      color: #333;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Oxygen',
        'Ubuntu', 'Cantarell', 'Fira Sans', 'Droid Sans', 'Helvetica Neue',
        sans-serif;
      margin: 0;
      padding: 20px;
    }

    .App {
      max-width: 800px;
      margin: 0 auto;
      background-color: #fff;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      padding: 20px 40px;
    }

    .App-header {
      text-align: center;
      border-bottom: 1px solid #eee;
      padding-bottom: 20px;
      margin-bottom: 20px;
    }

    .App-header h1 {
      color: #1a73e8;
    }

    .upload-form {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 15px;
      margin-bottom: 30px;
    }

    .upload-form input[type="file"] {
      border: 1px solid #ccc;
      padding: 10px;
      border-radius: 5px;
      width: 100%;
      max-width: 400px;
    }

    .upload-form button {
      background-color: #1a73e8;
      color: white;
      border: none;
      padding: 12px 25px;
      border-radius: 5px;
      font-size: 16px;
      cursor: pointer;
      transition: background-color 0.3s;
    }

    .upload-form button:hover {
      background-color: #155ab6;
    }

    .upload-form button:disabled {
      background-color: #9e9e9e;
      cursor: not-allowed;
    }

    .error-message {
      color: #d32f2f;
      background-color: #ffcdd2;
      border: 1px solid #d32f2f;
      padding: 15px;
      border-radius: 5px;
      text-align: center;
      margin-top: 20px;
    }

    .results {
      margin-top: 30px;
      animation: fadeIn 0.5s ease-in-out;
    }

    .result-section {
      background-color: #fafafa;
      border: 1px solid #e0e0e0;
      border-radius: 5px;
      margin-bottom: 20px;
      padding: 15px;
    }

    .result-section h3 {
      margin-top: 0;
      color: #333;
    }

    pre {
      background-color: #e8e8e8;
      padding: 15px;
      border-radius: 4px;
      white-space: pre-wrap; /* Wraps long lines */
      word-wrap: break-word;
      font-family: 'Courier New', Courier, monospace;
      font-size: 14px;
    }

    .loader {
      border: 5px solid #f3f3f3;
      border-top: 5px solid #1a73e8;
      border-radius: 50%;
      width: 40px;
      height: 40px;
      animation: spin 1s linear infinite;
      margin: 20px auto;
    }

    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    @keyframes fadeIn {
      from { opacity: 0; }
      to { opacity: 1; }
    }
    ```

---

### Step 3: Run the React App

Now, in the terminal for your React app, run the start command:

```bash
npm start
```

Your web browser should automatically open to `http://localhost:3000`, and you will see the user interface.

### How It Works: The Final Check

1.  **Backend:** Your Flask server is running on `http://localhost:5001`.
2.  **Frontend:** Your React app is running on `http://localhost:3000`.
3.  **Action:**
    *   Go to `http://localhost:3000` in your browser.
    *   Click the "Choose File" button and select a PDF or DOCX file.
    *   Click the "Analyze Document" button.
4.  **Result:**
    *   You will see the "Analyzing..." text and a loading spinner.
    *   The `fetch` call in `App.js` sends the file to your Flask backend.
    *   The Flask server processes it and sends back the JSON.
    *   The React app receives the JSON, updates its state, and displays the formatted results on the page. If there's an error (e.g., you upload a non-document file or the parsing fails), the red error box will appear with the message from the server.