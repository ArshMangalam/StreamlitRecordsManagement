#!/usr/bin/env python3
from app import create_app
from app.services.jobs import start_scheduler
import os
from dotenv import load_dotenv

load_dotenv()

if __name__ == '__main__':
    app = create_app()

    start_scheduler()

    debug = os.getenv('FLASK_ENV', 'production') == 'development'
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=debug
    )
