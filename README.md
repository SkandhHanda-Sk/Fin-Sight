# Fin-Sight: AI-Powered Financial Document Analysis

**Fin-Sight** is a web application designed to ingest complex financial documents and transform them into actionable insights. Users can upload reports in various formats, and our AI-powered backend extracts key data, calculates financial ratios, and presents the results in a clean, interactive dashboard.

This project is built to simplify financial analysis for everyone, from individual investors to large enterprises.

## ✨ Key Features

*   **Multi-Format Document Processing:** Accepts `.pdf`, `.docx`, `.xlsx`, `.xls` and other files for analysis.
*   **Intelligent Data Extraction:** Utilizes OCR for scanned PDFs and preserves table structures from all document types.
*   **Automated Financial Ratio Analysis:** The AI core automatically calculates and displays key financial ratios from the extracted data.
*   **Interactive Dashboards:** Visualizes financial data and key metrics using charts for easy interpretation.
*   **Modular & Scalable Architecture:** A robust **Flask (Python)** backend API serves a modern **React + Vite** frontend, with a dedicated AI module for processing.
*   **Fully Containerized:** The entire application stack (backend, AI, and frontend) is containerized with **Docker**, ensuring a simple, one-command setup.

## 💻 Tech Stack

| Area         | Technology                                                                                                                                                                                                                                                        | Description                                                                                                                            |
| :----------- | :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------- |
| **Frontend** | ![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB) ![Vite](https://img.shields.io/badge/vite-%23646CFF.svg?style=for-the-badge&logo=vite&logoColor=white)                                                  | A modern UI built with React and powered by Vite for an incredibly fast development experience with Hot Module Replacement (HMR).      |
| **Backend**  | ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Flask](https://img.shields.io/badge/flask-%23000.svg?style=for-the-badge&logo=flask&logoColor=white)                                                          | A lightweight and powerful Flask API to handle file uploads, manage processing jobs, and serve data to the frontend.                 |
| **DevOps**   | ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)                                                                                                                                                         | The entire application is containerized, ensuring consistent environments and a simple, one-command setup with Docker Compose.       |

## 📂 Project Structure

```text
Fin-Sight/Testing/
├── ai/                     # Core AI and data processing modules
│   └── ...
├── backend/                # Flask API and file handling
│   ├── uploads/            # Temporary storage for user-uploaded files
│   ├── app.py              # Main Flask application entry point
│   ├── financial_parser.py # Parses text into structured financial data
│   └── text_extractor.py   # Extracts raw text and tables from documents
├── frontend/               # React UI application
│   ├── src/
│   │   └── components/     # Reusable React components (charts, sections, etc.)
│   ├── Dockerfile          # Container definition for the frontend service
│   └── package.json
├── .gitignore
├── docker-compose.yml      # Orchestrates all services (frontend, backend)
├── Docker-Guide.md         # In-depth guide for the Docker setup
├── Dockerfile              # Container definition for the backend service
├── requirements.txt        # Python dependencies for backend & AI
└── README.md               # You are here!
```

### A Note on the Frontend

The frontend was bootstrapped with the standard **React + Vite** template. This provides a minimal setup with excellent performance and developer experience features like Fast Refresh.

*   **Vite Plugins:** It uses [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) which leverages Babel for Fast Refresh.
*   **ESLint:** For production applications, we recommend expanding the ESLint configuration with type-aware linting rules. See the official [Vite TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for guidance.

---

## 🚀 Getting Started

This project is fully containerized, making setup incredibly simple.

### Prerequisites

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.
*   [Git](https://git-scm.com/) or [GitHub Desktop](https://desktop.github.com/) for cloning the repository.

### Run with Docker (Recommended)

This single command will build the images for the frontend and backend, start the containers, and run the entire application.

```bash
# 1. Clone the repository
git clone https://github.com/your-username/fin-sight.git
cd fin-sight/Testing/

# 2. Build and start all services
docker-compose up --build
```

That's it!

*   The **Frontend** will be available at `http://localhost:3000`.
*   The **Backend API** will be running at `http://localhost:5001`.

To stop the application, press `Ctrl + C` in the terminal, and then run `docker-compose down`.

### Alternative: Local Development (for Frontend)

If you are actively developing the frontend and want to leverage Vite's Hot Module Replacement (HMR), you can run the backend in Docker and the frontend locally.

#### 1. Run the Backend (Terminal 1)

```bash
# From the Fin-Sight/Testing/ directory
docker-compose up --build backend
```
This command starts only the backend service.

#### 2. Run the Frontend (Terminal 2)

```bash
# Navigate to the frontend directory
cd frontend/

# Install dependencies (only needed once)
npm install

# Start the React development server with HMR
npm run dev
```
The frontend will still be available at `http://localhost:3000` and will connect to the Dockerized backend.

---

## 💡 Roadmap & Future Improvements

While the core functionality is in place, there are many exciting directions for this project:

*   **Advanced NLP Analysis:**
    *   **Sentiment Analysis:** Analyze the "Management Discussion & Analysis" (MD&A) section to gauge tone (optimistic, pessimistic, neutral).
    *   **Summarization:** Use a pre-trained model (like T5 or BART) to generate a concise, executive summary of the entire document.
*   **Enhanced Data Features:**
    *   **Trend Analysis:** Allow users to upload multiple reports for the same company (e.g., 2023 Q3, 2023 Q4) and automatically generate trend charts.
    *   **Comparison View:** Create a UI to place two reports side-by-side and automatically highlight the key differences.
*   **Architecture & Scalability:**
    *   **Asynchronous Processing:** For large documents, use a task queue like **Celery** with **Redis** to process files in the background, improving UI responsiveness.
    *   **Vector Database:** Store document text as vector embeddings in a database like **Pinecone** or **ChromaDB** to enable powerful semantic search (e.g., "What are the main risks related to supply chain issues?").
    *   **User Accounts:** Implement authentication to allow users to save their documents and analysis history.
*   **Deployment:**
    *   **Cloud Deployment:** Create scripts and configurations to easily deploy the application to a cloud provider like AWS Elastic Beanstalk or Google Cloud Run.

## 🤝 Contributing

We welcome contributions! If you have an idea for a new feature or have found a bug, please open an issue in the GitHub repository. Pull requests are also greatly appreciated.

## 👥 The Team

*   Skandh Handa
*   Shubhankar
*   Vedika Srivastava
*   Vanshika Gupta
*   Yash