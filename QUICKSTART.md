# Quick Start Guide

## Installation (2 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Copy environment template
cp .env.example .env

# 3. Add your Supabase credentials to .env
# Edit .env and set SUPABASE_URL and SUPABASE_KEY
```

## Running (1 minute)

```bash
python run.py
```

Visit: `http://localhost:5000`

## First Use (2 minutes)

1. **Register or Guest**: Sign up with email or use guest mode
2. **Add Record**: Go to Records tab, create your first entry
3. **View Dashboard**: Check Dashboard to see KPIs
4. **Export Report**: Visit Reports to download as CSV/Excel/PDF
5. **Schedule Job**: Check Jobs tab for background data fetching

## API Testing

### Create Record
```bash
curl -X POST http://localhost:5000/api/records/create \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Sales",
    "category": "Revenue",
    "value": 1000,
    "timestamp": "2024-01-15T10:00:00Z"
  }'
```

### List Records
```bash
curl http://localhost:5000/api/records/list
```

### Export CSV
```bash
curl http://localhost:5000/api/reports/csv > records.csv
```

## Database Tables

Already created in Supabase:
- `users` - User accounts
- `records` - Your data
- `background_data` - Job logs

## Environment Variables

| Variable | Example |
|----------|---------|
| SUPABASE_URL | `https://xxx.supabase.co` |
| SUPABASE_KEY | `eyJhbGciOi...` |
| EXTERNAL_API_URL | `https://api.example.com/data` |
| JOB_INTERVAL_MIN | `5` |
| SECRET_KEY | `your-secret-key` |
| FLASK_ENV | `development` |

## Troubleshooting

**ModuleNotFoundError**: Run `pip install -r requirements.txt`

**SUPABASE_URL not set**: Check your `.env` file

**Port 5000 in use**: Kill process or change port in `run.py`

**Database connection failed**: Verify SUPABASE credentials are correct

## Next Steps

- Read `README.md` for full documentation
- Check `IMPLEMENTATION.md` for architecture details
- Run `pytest tests/` for test coverage
- Deploy with Gunicorn for production

## Performance

- Supports thousands of records
- Instant filtering
- PDF export in <2 seconds
- Background jobs every N minutes

## Support

- Check README.md troubleshooting
- Review test files for API examples
- Check inline code comments
