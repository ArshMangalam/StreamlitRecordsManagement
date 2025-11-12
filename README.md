# Streamlit CRUD Web App

A minimal, production-ready Streamlit web application with authentication, CRUD operations, dynamic dashboards, report generation, and background job scheduling.

## Features

- **Authentication**: Email/password login with bcrypt hashing, or optional guest mode
- **CRUD Operations**: Create, read, update, and delete records with flexible metadata
- **Dynamic Dashboard**: KPI cards, interactive time series charts, and category breakdowns with filters
- **Report Generation**: Export data as CSV, Excel, and PDF with summary statistics
- **Background Jobs**: APScheduler-based background data fetching from external APIs
- **Supabase Backend**: Secure, scalable database with Row Level Security (RLS)

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   ├── main.py                 # Main Streamlit application
│   ├── pages/
│   │   ├── auth.py            # Login/register/guest pages
│   │   ├── dashboard.py       # Dashboard with charts and KPIs
│   │   ├── records_page.py    # CRUD interface for records
│   │   ├── reports_page.py    # Report generation and downloads
│   │   └── jobs_page.py       # Background job management
│   ├── services/
│   │   ├── records.py         # Record CRUD operations
│   │   ├── reports.py         # Report generation logic
│   │   └── background_jobs.py # Background job functions
│   └── utils/
│       ├── database.py        # Supabase client
│       └── auth.py            # Authentication utilities
├── tests/
│   ├── test_records.py        # CRUD tests
│   └── test_reports.py        # Report export tests
├── requirements.txt
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your Supabase credentials:

```bash
cp .env.example .env
```

Edit `.env`:

```
SUPABASE_URL=your_supabase_url_here
SUPABASE_KEY=your_supabase_anon_key_here
EXTERNAL_API_URL=https://jsonplaceholder.typicode.com/posts
JOB_INTERVAL_MIN=5
```

### 3. Database Setup

The database schema is already created in your Supabase instance with the following tables:

- `users` - User accounts with bcrypt-hashed passwords
- `records` - User records with title, category, value, timestamp, and metadata
- `background_data` - Logs of background job executions

All tables have Row Level Security (RLS) enabled for data protection.

### 4. Run the Application

```bash
streamlit run app/main.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

### First Time Setup

1. **Register or Use Guest Mode**: Create an account with email/password or click "Continue as Guest"
2. **Create Records**: Navigate to "Records" and add your first record
3. **View Dashboard**: Check the "Dashboard" to see KPIs and charts
4. **Generate Reports**: Go to "Reports" to export data as CSV, Excel, or PDF
5. **Background Jobs**: Visit "Background Jobs" to manually trigger data fetching

### Dashboard Filters

- **Category**: Filter by specific category or view all
- **Date Range**: Set start and end dates to focus on specific time periods

### Record Fields

- **Title**: Descriptive name for the record
- **Category**: Classification (e.g., Sales, Marketing, Operations)
- **Value**: Numeric value
- **Timestamp**: Date and time of the record
- **Metadata**: JSON object for additional flexible data

### Report Types

- **CSV**: Simple comma-separated values for spreadsheet import
- **Excel**: Formatted workbook with all record data
- **PDF**: Summary report with statistics and top records

### Background Jobs

- Jobs run automatically at the configured interval
- Manual trigger available in the "Background Jobs" page
- View job history and success/error status
- Fetched data is stored in the `background_data` table

## Running Tests

```bash
pytest tests/ -v
```

Tests cover:
- CRUD operations for records
- Report generation (CSV, Excel, PDF)
- Error handling and edge cases

## Key Technologies

- **Streamlit**: Web UI framework
- **Supabase**: PostgreSQL database with real-time capabilities
- **Plotly**: Interactive charts and visualizations
- **Pandas**: Data manipulation and CSV/Excel export
- **WeasyPrint**: HTML-to-PDF conversion
- **APScheduler**: Background job scheduling
- **bcrypt**: Secure password hashing
- **pytest**: Testing framework

## Security Notes

- All passwords are hashed using bcrypt
- Row Level Security (RLS) ensures users only access their own data
- Supabase connection uses environment variables (never hardcoded)
- Guest accounts are isolated and temporary

## Production Considerations

For production deployment:

1. **Environment Variables**: Use secure secret management (AWS Secrets Manager, etc.)
2. **Background Jobs**: Replace in-memory APScheduler with persistent queue (Celery, AWS Lambda)
3. **Hosting**: Deploy on Streamlit Cloud, AWS, or Docker containers
4. **Monitoring**: Add logging and error tracking (Sentry, CloudWatch)
5. **Rate Limiting**: Implement API rate limits for external data fetching
6. **Database Backups**: Enable automated Supabase backups

## Troubleshooting

### "SUPABASE_URL not set" Error

Make sure you have a `.env` file in the project root with valid credentials.

### Charts Not Displaying

Ensure you have records in the database. The dashboard needs data to visualize.

### PDF Generation Fails

WeasyPrint requires system libraries. On Ubuntu/Debian:

```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

On macOS:

```bash
brew install pango
```

### Background Jobs Not Running

Jobs run in-memory and reset on app restart. Check the "Background Jobs" page to manually trigger.

## License

MIT License - Feel free to use this as a template for your own projects.

## Support

For issues or questions, please check the troubleshooting section or review the inline code comments.
