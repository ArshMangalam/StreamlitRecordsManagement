# Flask CRUD Web Application

A production-ready Flask web application with authentication, CRUD operations, dynamic dashboards, report generation, and background job scheduling.

## Features

- **Authentication**: Email/password login with bcrypt hashing, or optional guest mode
- **CRUD Operations**: RESTful API for creating, reading, updating, and deleting records
- **Dashboard**: Real-time KPI metrics and analytics with filtering
- **Report Generation**: Export data as CSV, Excel, and PDF with summary statistics
- **Background Jobs**: APScheduler-based background data fetching from external APIs
- **Supabase Backend**: Secure, scalable PostgreSQL database with Row Level Security

## Project Structure

```
.
├── app/
│   ├── __init__.py                 # Flask app factory
│   ├── models/
│   │   └── __init__.py            # Database client
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth.py                # Authentication endpoints
│   │   ├── records.py             # Records CRUD endpoints
│   │   ├── reports.py             # Report export endpoints
│   │   └── jobs.py                # Background job endpoints
│   ├── services/
│   │   ├── auth.py                # Authentication logic
│   │   ├── records.py             # Records business logic
│   │   ├── reports.py             # Report generation
│   │   └── jobs.py                # Background job logic
│   ├── templates/
│   │   └── index.html             # Single-page app HTML
│   └── static/
│       ├── css/style.css          # Styling
│       └── js/app.js              # Frontend application
├── tests/
│   └── test_api.py                # API tests
├── run.py                         # Application entry point
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
SECRET_KEY=your-secret-key-here
FLASK_ENV=development
```

### 3. Database Setup

The database schema is already created in your Supabase instance with the following tables:

- `users` - User accounts with bcrypt-hashed passwords
- `records` - User records with title, category, value, timestamp, and metadata
- `background_data` - Logs of background job executions

All tables have Row Level Security (RLS) enabled for data protection.

### 4. Run the Application

```bash
python run.py
```

The app will be available at `http://localhost:5000`

## Usage

### First Time Setup

1. **Register or Use Guest Mode**: Create an account or use guest access
2. **Create Records**: Navigate to "Records" and add your first record
3. **View Dashboard**: Check the "Dashboard" to see KPIs and analytics
4. **Generate Reports**: Go to "Reports" to export data
5. **Background Jobs**: Visit "Jobs" to manage data fetching

### API Endpoints

#### Authentication
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login with email/password
- `POST /api/auth/guest` - Create guest account
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

#### Records
- `POST /api/records/create` - Create record
- `GET /api/records/list` - List user records (supports filters)
- `GET /api/records/<id>` - Get single record
- `PUT /api/records/<id>` - Update record
- `DELETE /api/records/<id>` - Delete record
- `GET /api/records/statistics` - Get KPI statistics

#### Reports
- `GET /api/reports/csv` - Export as CSV
- `GET /api/reports/excel` - Export as Excel
- `GET /api/reports/pdf` - Export as PDF
- `GET /api/reports/summary` - Get summary statistics

#### Background Jobs
- `POST /api/jobs/run` - Manually trigger job
- `GET /api/jobs/last-run` - Get last job execution
- `GET /api/jobs/history` - Get job history
- `GET /api/jobs/config` - Get job configuration
- `POST /api/jobs/start-scheduler` - Start background scheduler

### Record Fields

- **Title**: Descriptive name
- **Category**: Classification/type
- **Value**: Numeric value
- **Timestamp**: Date and time
- **Metadata**: JSON object for flexible data

### Filters Available

- **Category**: Filter by specific category
- **Date Range**: Filter by start and end dates
- All filters are applied across records, statistics, and reports

## Running Tests

```bash
pytest tests/ -v
```

Tests cover:
- Authentication endpoints
- CRUD operations
- Report generation
- Statistics calculation
- Unauthorized access

## Key Technologies

- **Flask**: Lightweight web framework
- **Supabase**: PostgreSQL database with RLS
- **Pandas**: Data manipulation and export
- **WeasyPrint**: HTML-to-PDF conversion
- **APScheduler**: Background job scheduling
- **bcrypt**: Secure password hashing
- **pytest**: Testing framework
- **Flask-CORS**: Cross-origin resource sharing

## Architecture

### Frontend
- Single-page application (SPA) built with vanilla JavaScript
- Responsive design with CSS Grid and Flexbox
- Real-time UI updates

### Backend
- RESTful API with Flask blueprints
- Session-based authentication with server-side storage
- Service layer for business logic separation

### Database
- Supabase PostgreSQL with RLS policies
- User isolation through RLS
- Indexed queries for performance

## Security Features

- **Password Security**: Bcrypt hashing with salt
- **Row Level Security**: Users only access their own data
- **Session Management**: Server-side session storage
- **CORS**: Protected cross-origin requests
- **Input Validation**: Server-side validation on all endpoints

## Environment Variables

| Variable | Description |
|----------|-------------|
| SUPABASE_URL | Supabase project URL |
| SUPABASE_KEY | Supabase anonymous key |
| EXTERNAL_API_URL | External API endpoint for jobs |
| JOB_INTERVAL_MIN | Background job interval in minutes |
| SECRET_KEY | Flask secret key (must be set in production) |
| FLASK_ENV | development or production |

## Production Deployment

For production:

1. **Set strong SECRET_KEY** in environment
2. **Disable debug mode**: Set `FLASK_ENV=production`
3. **Use production WSGI server**: Gunicorn or uWSGI
4. **Enable HTTPS**: Use reverse proxy like Nginx
5. **Database backups**: Enable Supabase automated backups
6. **Monitoring**: Add logging and error tracking
7. **Rate limiting**: Implement API rate limits

Example with Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

## Troubleshooting

### "SUPABASE_URL not set" Error

Ensure `.env` file exists in project root with valid credentials.

### Database Connection Issues

Check that:
- SUPABASE_URL and SUPABASE_KEY are correct
- Network has access to Supabase
- Database tables exist (run migrations)

### PDF Generation Fails

Install system dependencies:

**Ubuntu/Debian:**
```bash
sudo apt-get install libpango-1.0-0 libpangoft2-1.0-0
```

**macOS:**
```bash
brew install pango
```

### Background Jobs Not Starting

Jobs start automatically with the app. Check:
- APScheduler is installed
- No scheduler already running
- Check application logs

## API Response Format

All endpoints return JSON responses:

**Success Response:**
```json
{
    "message": "Operation successful",
    "data": {...}
}
```

**Error Response:**
```json
{
    "error": "Error message describing the issue"
}
```

## Performance Optimization

- Database queries use indexes on user_id, category, timestamp
- Records are paginated in list views
- Export operations stream data to avoid memory issues
- Background jobs run in separate thread

## Contributing

Guidelines for extending the application:

1. Create new endpoints in appropriate api/*.py file
2. Add business logic to services/*.py
3. Add tests for new functionality
4. Update documentation

## License

MIT License - Use freely for personal and commercial projects

## Support

For issues or questions:
1. Check troubleshooting section
2. Review inline code comments
3. Check test files for usage examples
