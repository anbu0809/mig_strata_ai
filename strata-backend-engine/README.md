# Strata Backend Engine

This is the standalone backend engine for the Strata AI-powered multi-database migration platform.

## Features

- RESTful API for database connection management
- Multi-database support (PostgreSQL, MySQL, Snowflake, Databricks, Oracle, SQL Server, Teradata, Google BigQuery)
- AI-powered schema translation and validation
- Secure credential storage with encryption
- Session management for migration workflows

## API Endpoints

### Connections
- `POST /api/connections/test` - Test database connection
- `POST /api/connections/save` - Save database connection
- `GET /api/connections` - List all connections
- `DELETE /api/connections/{id}` - Delete a connection

### Session
- `GET /api/session` - Get current session
- `POST /api/session/set-source-target` - Set source and target databases

### Analysis
- `POST /api/analyze/start` - Start analysis
- `GET /api/analyze/status` - Get analysis status

### Extraction
- `POST /api/extract/start` - Start extraction
- `GET /api/extract/status` - Get extraction status

### Migration
- `POST /api/migrate/start` - Start migration
- `GET /api/migrate/status` - Get migration status

### Validation
- `POST /api/validate/start` - Start validation
- `GET /api/validate/status` - Get validation status

### Export
- `GET /api/export/report/{format}` - Export validation report (pdf, json, xlsx)

### Reset
- `POST /api/reset` - Reset migration session

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Set environment variables:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `OPENAI_MODEL` - OpenAI model to use (default: gpt-4o-mini)

3. Initialize the database:
   ```
   python init_db.py
   ```

4. Start the server:
   ```
   python main.py
   ```

   Or use the start script:
   ```
   start.bat
   ```

## Usage

The backend API will be available at `http://localhost:8000` by default.

You can integrate this backend with any frontend by making HTTP requests to the API endpoints listed above.