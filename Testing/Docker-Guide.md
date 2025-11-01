
This guide explains the purpose of the Docker setup and provides clear, step-by-step instructions for any developer who wants to get the project running. It assumes you are using the improved `docker-compose.yml` that manages both the frontend and backend services.

---

# Docker Guide for Fin-Sight

This guide provides instructions on how to build, run, and manage the Fin-Sight application using Docker and Docker Compose. Using Docker ensures a consistent and isolated development environment for all team members, regardless of their local machine setup.

## Overview

Our Docker setup consists of two main services defined in `docker-compose.yml`:

1.  **`backend`**: A Python Flask server that handles file uploads, text extraction, financial parsing, and analysis. It runs on port `5001`.
2.  **`frontend`**: A React web application that provides the user interface for uploading documents and viewing the analysis. It runs on port `3000`.

The key benefit of this setup is **live-reloading**. Any changes you make to the Python code in the `./backend` directory or the React code in the `./frontend/src` directory will be automatically reflected in the running containers, speeding up development significantly.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

*   [Docker Desktop](https://www.docker.com/products/docker-desktop/) (which includes Docker Engine and Docker Compose).

## One-Time Setup

For the full frontend and backend setup to work, you need to have a `Dockerfile` inside the `frontend` directory.

1.  **Create `frontend/Dockerfile`**:
    Create a new file at `Testing/frontend/Dockerfile` and add the following content:

    ```dockerfile
    # Testing/frontend/Dockerfile

    # Use an official Node.js runtime as a parent image
    FROM node:18-alpine

    # Set the working directory in the container
    WORKDIR /app

    # Copy package.json and package-lock.json
    # This leverages Docker's layer caching
    COPY package*.json ./

    # Install app dependencies
    RUN npm install

    # Copy the rest of the application code
    COPY . .

    # Make port 3000 available to the world outside this container
    EXPOSE 3000

    # Command to run the app in development mode
    CMD ["npm", "start"]
    ```

## Step-by-Step Instructions

All commands should be run from the `Fin-Sight/Testing/` directory in your terminal.

### Step 1: Build the Docker Images

This command reads the `docker-compose.yml` file, finds the `build` instructions for both the `backend` and `frontend` services, and creates the necessary Docker images. This might take a few minutes the first time as it downloads base images and installs dependencies.

```bash
docker-compose build
```

### Step 2: Start the Services

This command starts the containers for both services in "detached" mode (`-d`), meaning they will run in the background.

```bash
docker-compose up -d
```

### Step 3: Verify the Containers are Running

Check the status of your running containers.

```bash
docker-compose ps
```

You should see an output similar to this, indicating that both services are `Up`:

```
      Name                     Command               State           Ports
------------------------------------------------------------------------------------
finsight-backend    python app.py                    Up      0.0.0.0:5001->5001/tcp
finsight-frontend   npm start                        Up      0.0.0.0:3000->3000/tcp
```

### Step 4: Access the Application

Your full application is now running!

*   **Frontend UI**: Open your web browser and navigate to **`http://localhost:3000`**
*   **Backend Health Check**: To verify the backend is running independently, navigate to **`http://localhost:5001/health`**. You should see a JSON response: `{"status": "ok", "message": "Backend is running!"}`.

You can now use the web interface to upload a document and get the analysis.

## Development Workflow

The primary advantage of this setup is the seamless development experience.

*   **Backend Changes**: Edit any `.py` file inside the `backend/` directory on your local machine. Save the file. The volume mount will sync this change into the container, and the Flask development server will automatically reload.
*   **Frontend Changes**: Edit any file inside the `frontend/src/` directory. Save the file. The React development server will automatically hot-re-render the changes in your browser.

## Useful Docker Commands

Here are some common commands you will use during development.

#### View Logs

To see the real-time logs (output) from a service, which is essential for debugging:

```bash
# View logs for the backend
docker-compose logs -f backend

# View logs for the frontend
docker-compose logs -f frontend
```
Press `Ctrl + C` to stop viewing the logs.

#### Stop the Application

To stop and remove the running containers, networks, and volumes created by `up`:

```bash
docker-compose down
```

#### Rebuild an Image

If you change a dependency (e.g., add a new package to `requirements.txt` or `package.json`), you need to rebuild the image for that service.

```bash
# Rebuild all services
docker-compose build

# Rebuild only the backend service
docker-compose build backend
```

After rebuilding, bring the services up again with `docker-compose up -d`.

#### Access a Container's Shell

For advanced debugging, you can get an interactive shell (`bash` or `sh`) inside a running container.

```bash
# Get a shell inside the backend container
docker-compose exec backend bash

# Get a shell inside the frontend container (uses sh)
docker-compose exec frontend sh
```

## Troubleshooting

*   **Port Conflict**: If you see an error like `Error starting userland proxy: listen tcp 0.0.0.0:5001: bind: address already in use`, it means another process on your machine is already using that port. Stop the other process or change the port mapping in `docker-compose.yml` (e.g., change `"5001:5001"` to `"5002:5001"`).
*   **Frontend Can't Connect to Backend**:
    1.  Ensure the backend container is running (`docker-compose ps`).
    2.  Check the backend logs (`docker-compose logs backend`) for any errors on startup.
    3.  Confirm that the API URL in your React code is `http://localhost:5001/api/process-document`. The React app runs in your browser, which accesses the backend via the port mapped to your `localhost`.