# Strata - Enterprise AI Translation Platform

Strata is an AI-automated multi-database migration platform that simplifies the process of migrating databases from one system to another.

## Features

- Four-step migration process: Analyze → Extract → Migrate → Reconcile
- Support for multiple database types: PostgreSQL, MySQL, Snowflake, Databricks, Oracle, SQL Server, Teradata, Google BigQuery
- AI-powered schema translation and validation
- Web-based interface with real-time progress tracking
- Export validation reports in PDF, JSON, and Excel formats

## Prerequisites

- Python 3.8+
- Node.js 16+
- npm 8+

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd strata
   ```

2. Install backend dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:
   ```
   cd frontend
   npm install
   ```

## Usage

### Development Mode

1. Start the backend server:
   ```
   python main.py
   ```

2. Start the frontend development server:
   ```
   cd frontend
   npm run dev
   ```

3. Open your browser and navigate to `http://localhost:3000`

### One-Click Start (Linux/Mac)

```
./start.sh
```

### One-Click Start (Windows)

```
start.bat
```

### Using the CLI Tool

Strata includes a command-line interface for easy management:

```
python strata.py [command] [options]
```

Available commands:
- `setup` - Set up the development environment
- `start [all|backend|frontend]` - Start the application components
- `status` - Check the application status
- `test [all|e2e|backend|frontend]` - Run tests
- `deploy` - Deploy the application
- `reset` - Reset the application (clears database and artifacts)

Example:
```
python strata.py start all
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key for AI-powered features
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)
- `FERNET_KEY`: Encryption key for database credentials (auto-generated if not provided)

## Database Support

Strata supports the following databases:
- PostgreSQL
- MySQL
- Snowflake
- Databricks
- Oracle
- SQL Server
- Teradata
- Google BigQuery

## Architecture

The application follows a client-server architecture:
- Frontend: React + Vite + TypeScript with TailwindCSS
- Backend: Python FastAPI
- Database: SQLite for storing connections and session data
- Background Tasks: FastAPI BackgroundTasks