# This-or-That Decision Helper

An AI-powered decision-making tool to help you choose between two options.

## Features

- AI-powered decision making using OpenAI
- Random coin flip mode
- Docker containerization for easy setup

## Prerequisites

- Docker and Docker Compose installed on your machine (only needed for Docker option)
- OpenAI API key (only needed for AI-powered decisions)

## Security Note

For security reasons, **NEVER commit your OpenAI API key to version control**. The `.env` file is already in `.gitignore`, so you can safely store your API key there.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/SGupta101/This-or-That.git
   cd This-or-That
   ```

2. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   ```
   Edit `backend/.env` and add your OpenAI API key if you want to use AI-powered decisions.

## Running the App

### Option 1: Using Docker (Recommended)

1. Build and start the containers:

   ```bash
   docker compose up --build
   ```

2. Access the app:
   - Open your browser and go to http://localhost:5173
   - The backend API will be available at http://localhost:8000

### Option 2: Without Docker

1. Install dependencies:

   ```bash
   # Backend (Python)
   cd backend
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt

   # Frontend (Node.js)
   cd ../frontend
   npm install
   ```

2. Set up environment variables:

   ```bash
   # Backend
   cp backend/.env.example backend/.env
   # Edit backend/.env and add your OpenAI API key if you want to use AI-powered decisions

   # Frontend
   cp frontend/.env.example frontend/.env
   # Edit frontend/.env and set VITE_API_URL=http://localhost:8000
   ```

3. Start the backend:

   ```bash
   cd backend
   source .venv/bin/activate
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

4. In a new terminal, start the frontend:

   ```bash
   cd frontend
   npm run dev
   ```

5. Access the app:
   - Open your browser and go to http://localhost:5173
   - The backend API will be available at http://localhost:8000

## Usage

1. Enter two options you're deciding between
2. Choose your decision mode:
   - **Random**: Quick random choice (no API key needed)
   - **Reasoned**: AI-powered decision with explanation (requires OpenAI API key)
3. Click "Get Decision" to see your result

## Development

The app uses:

- Frontend: React + TypeScript + Vite + TailwindCSS
- Backend: Python + FastAPI
- Containerization: Docker + Docker Compose
- Windsurf AI
