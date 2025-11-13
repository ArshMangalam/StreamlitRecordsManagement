from flask import Flask
from flask_cors import CORS
import os
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['JSON_SORT_KEYS'] = False

    from app.api import auth_bp, records_bp, reports_bp, jobs_bp
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(records_bp, url_prefix='/api/records')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    app.register_blueprint(jobs_bp, url_prefix='/api/jobs')

    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    return app
