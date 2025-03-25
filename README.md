# This-or-That Decision Helper

An AI-powered decision-making tool to help you choose between two options.

## Features

- AI-powered decision making using free, open-source models
- Random coin flip mode
- Decision history tracking with Supabase
- Context-aware decisions

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy `.env.example` to `.env` and fill in your Supabase credentials
4. Run the development server:
   ```bash
   uvicorn backend.main:app --reload
   ```

## Project Structure

```
This-or-That/
├── backend/
│   ├── main.py           # FastAPI server
│   ├── models/           # ML models and decision logic
│   ├── database/         # Supabase integration
│   └── utils/           
├── frontend/            # React/Next.js frontend (coming soon)
├── requirements.txt     # Python dependencies
└── .env.example        # Environment variables template
```

## API Endpoints

- POST `/api/decide` - Get a decision between two options
- GET `/api/history` - View recent decisions
