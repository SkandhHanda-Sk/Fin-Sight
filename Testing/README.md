
---

# Fin-Sight: AI-Powered Financial Document Analysis

**Fin-Sight** is a web application designed to ingest complex financial documents and transform them into actionable insights. Users can upload reports in various formats (PDF, DOCX, XLSX), and our AI-powered backend extracts key information, performs analysis, and presents the results in a clean, user-friendly interface.

This project is built for the goal of simplifying financial analysis for everyone, from companies to investors.

## ✨ Key Features

*   **Multi-Format Support:** Accepts `.pdf`, `.docx`, `.xlsx`, and `.xls` files.
*   **Advanced Text Extraction:** Intelligently extracts text while preserving table structures from documents.
*   **OCR for Scanned PDFs:** Automatically detects and extracts text from image-based or scanned PDFs.
*   **AI-Powered Analysis:** (In Progress) A modular backend to plug in various analysis engines (e.g., KPI extraction, sentiment analysis, summarization).
*   **Decoupled Architecture:** A robust **Flask (Python)** backend API serves a modern **React** frontend.
*   **Containerized Backend:** The entire Python environment is containerized with **Docker** for consistent, one-command setup.

## 💻 Tech Stack

| Area    | Technology                                                                                              |
| :--- | :--- |
| **Frontend** | ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) |
| **Backend** | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white) |
| **DevOps** | ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) |

## 📂 Project Structure

```
Fin-Sight/Testing/
├── backend/                # All Python code
│   ├── app.py              # The Flask API server
│   └── text_extractor.py   # The core text extraction module
├── frontend/               # The React application
│   ├── src/
│   └── package.json
├── docker-compose.yml      # Defines and runs the backend service
├── Dockerfile              # The blueprint for the backend environment
├── requirements.txt        # Python dependencies
└── README.md               # You are here!
```

---

## 🚀 How to Run the Project

This project uses a two-terminal setup. One for the Dockerized backend and one for the local React frontend.

### Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
*   [Node.js and npm](https://nodejs.org/en/) installed.

### Step-by-Step Instructions

#### 1. Clone the Repository

```bash
git clone <your-repo-url> #to be updated
cd Fin-Sight/Testing/
```

#### 2. Run the Backend (Terminal 1)

This terminal will run the Python/Flask API inside a Docker container.

```bash
# Navigate to the project root
cd /path/to/Fin-Sight/Testing/

# 1. Build the Docker image (only needed the first time or after changes)
docker-compose build

# 2. Start the backend service
docker-compose up
```

Your backend is now running! You should see logs from Flask, and the API is available at `http://localhost:5001`.

#### 3. Run the Frontend (Terminal 2)

This terminal will run the React development server on your local machine.

```bash
# Navigate to the frontend directory
cd /path/to/Fin-Sight/Testing/frontend/

# 1. Install dependencies (only needed the first time)
npm install

# 2. Start the React app
npm start
```

Your browser should automatically open to `http://localhost:3000`, where you can see the application.

---

## 💡 Ideas & Future Improvements

This project has a strong foundation. Here are some ideas for where to take it next:

### Core Analysis Engine

*   **Financial KPI Extraction:** Use Regex and NLP (like spaCy) to automatically find and extract key metrics:
    *   Total Revenue
    *   Net Income / Loss
    *   EBITDA
    *   Gross Margin
    *   Key ratios (P/E, Debt-to-Equity)
*   **Sentiment Analysis:** Analyze the "Management Discussion & Analysis" (MD&A) section to gauge whether the tone is optimistic, pessimistic, or neutral.
*   **Trend Analysis:** Allow users to upload multiple reports for the same company (e.g., 2023 Q3, 2023 Q4) and automatically generate charts showing trends in key metrics.
*   **Summarization:** Use a pre-trained model (like T5 or BART) to generate a concise, executive summary of the entire document.

### User Interface (UI/UX)

*   **Interactive Dashboards:** Use a charting library (like Chart.js or Recharts) to visualize the extracted KPIs and trends.
*   **Insight Highlighting:** In the UI, when displaying the raw text, highlight the specific sentences or numbers where an insight was found. This builds trust and provides context.
*   **User Accounts & History:** Implement user authentication to allow users to save their uploaded documents and view their analysis history.
*   **Comparison View:** Create a UI to place two reports side-by-side and automatically highlight the key differences.

### Backend & Architecture

*   **Asynchronous Processing:** For large documents, analysis can be slow. Use a task queue like **Celery** with **Redis** to process files in the background. The UI can poll for results, providing a much better user experience.
*   **Vector Database for Semantic Search:** Store document text as vector embeddings in a database like **Pinecone** or **ChromaDB**. This would enable powerful semantic search features, allowing users to ask natural language questions like, "What are the main risks related to supply chain issues?"
*   **Cloud Deployment:** Create scripts and configurations to easily deploy the application to a cloud provider like AWS Elastic Beanstalk or Google Cloud Run.

## 👥 The Team

*   [Name]
*   [Name]
*   [Name]