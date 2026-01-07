# Dynamic Observability Platform (DynObs) 🚀
> **🚧 Under Active Development**: A professional orchestration and AI-driven observability platform. Note this project is still in active development and is not ready for production use.

![Java](https://img.shields.io/badge/Java-17%2B-ED8B00?style=for-the-badge&logo=openjdk&logoColor=white)
![Spring Boot](https://img.shields.io/badge/Spring_Boot-3.1-6DB33F?style=for-the-badge&logo=spring-boot&logoColor=white)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Podman](https://img.shields.io/badge/Podman-Container-892CA0?style=for-the-badge&logo=podman&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local_LLM-black?style=for-the-badge&logo=ollama&logoColor=white)

## 📖 Overview

**DynObs** is a modernization of container orchestration, bridging the gap between raw container management and intelligent observability. Unlike standard dashboards that simply *show* logs, DynObs attempts to *understand* them using local Large Language Models (LLMs).

It offers a "Single Pane of Glass" to deploy complex stacks (Orchestration) and monitor their health through AI-powered log analysis (Observability).

---

## 🏗️ Design & Architecture Choices

### 🔄 Migration: Python to Java
The original prototype utilized a split architecture (Python for Podman/AI, Java for API). We migrated to a **Unified Java Backend** for the following reasons:
*   **Architecture Simplicity**: Consolidating to a single Spring Boot application reduces operational overhead and deployment complexity.
*   **Strong Typing**: Leveraging Java's type safety prevents a class of runtime errors present in the dynamic Python scripts.
*   **Concurrency**: Spring Boot's robust thread management is better suited for handling simultaneous log streams and HTTP requests than the previous synchronous Python implementation.
*   **Ecosystem**: The `docker-java` library provides a more mature and stable interface for Podman socket interaction on Windows compared to the Python alternatives tested.

### 🎨 Frontend Modernization
*   **React + Vite**: Chosen for near-instant hot-reloading and component reusability.
*   **Dark Mode & Glassmorphism**: Implemented to provide a premium, "Day-2 Operations" feel suitable for engineering tools.

---

## ✨ Key Features

*   **1-Click Orchestration**: Deploy multi-container setups (e.g., Nginx + Redis) instantly.
*   **Live Monitoring**: Real-time tracking of active containers via Podman socket integration.
*   **🧠 AI Log Analysis**: On-demand inspection of container logs using **Ollama** (Llama 3.2) to detect anomalies and explain errors in plain English.
*   **Responsive Dashboard**: A unified view for command, control, and insights.

---

## 🚀 Getting Started

Follow these steps to spin up the entire platform locally.

### Prerequisites
1.  **Java JDK 17+**
2.  **Node.js 18+**
3.  **Podman Desktop** (or CLI installed and machine running).
4.  **Ollama**: Installed and running.
    *   Pull the model: `ollama pull llama3.2:3b`

### Step-by-Step Installation

#### 1. Backend Setup (Spring Boot)
The backend acts as the orchestrator. It connects to both Podman and Ollama.

```powershell
# 1. Navigate to the app directory
cd app

# 2. Configure Podman Socket (Windows)
# This tells the Java app where to find the Podman machine
$env:DOCKER_HOST="npipe:////./pipe/podman-machine-default"

# 3. Build and Run
mvn clean install -DskipTests
mvn spring-boot:run
```
*Server will start on `http://localhost:8080`*

#### 2. Demo Containers (Optional)
To verify observability, spin up some "noise" containers using the provided helper script.

```powershell
# Open a new terminal in the project root
.\start_demo_containers.ps1
```
*This starts Nginx, Redis, and a "Loop" container that generates logs.*

#### 3. Frontend Setup (React)
The dashboard UI.

```powershell
# 1. Navigate to frontend
cd frontend

# 2. Install Dependencies
npm install

# 3. Start Dev Server
npm run dev
```
*Access the dashboard at `http://localhost:5173`*

---

## ⚙️ How Orchestration Works
When you click **"Deploy"** in the dashboard:
1.  **Frontend** sends a request to the Java Backend (`POST /api/orchestrate/web-stack`).
2.  **Backend** (`OrchestrationService`) receives the command.
3.  **Backend** acts as a controller, using the `docker-java` library to talk directly to your local **Podman Socket**.
4.  It instructs Podman to pull images (`nginx`, `redis`) and start containers from scratch.
    *   *Note: This mimics a real-world orchestrator like Kubernetes, but runs locally on your machine.*

---

## 🎮 Usage Guide

### 1. Launching the Demo Environment
To fully test the **AI Analysis** features, you need a container that generates logs. We provide a script for this:

**Option A: The Full Demo Script (Recommended)**
This spins up `nginx`, `redis`, and a special `dynobs-alpine` container that prints logs for the AI to analyze.
```powershell
# Run from project root
.\start_demo_containers.ps1
```

**Option B: Dashboard Orchestration**
You can also start containers directly from the UI:
1.  Go to the Dashboard.
2.  Click **"Deploy"** on the "Web Stack" card.
3.  Watch the "System Logs" panel as the Backend instructs Podman to start Nginx and Redis.

### 2. Live Monitoring
The "Active Containers" panel polls the backend every 5 seconds to show whatever is currently running on your Podman machine.

### 3. AI Log Analysis
1.  Ensure `dynobs-alpine` is running (use **Option A** above).
2.  Find it in the "Active Containers" list.
3.  Click the **"Analyze AI"** button.
4.  The Backend fetches the last 5 lines of logs, sends them to **Ollama**, and streams the explanation to the "System Logs" panel.

## 🛠️ Tech Stack

### Backend
*   **Framework**: Spring Boot 3
*   **Container API**: `docker-java` (interacting with Podman)
*   **AI Integration**: `RestTemplate` connecting to local Ollama API

### Frontend
*   **Core**: React 18, Vite
*   **Styling**: Tailwind CSS
*   **Animation**: Framer Motion
*   **Icons**: Lucide React

---
*Created by Mahed Javed - 2026 - for any queries & feedback please get in touch: mahed95@gmail.com*