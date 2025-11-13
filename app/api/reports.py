from flask import Blueprint, request, jsonify, session, send_file
from app.services.records import get_records, get_record_statistics
from app.services.reports import generate_csv, generate_excel, generate_pdf_summary
from datetime import datetime
from io import BytesIO

reports_bp = Blueprint('reports', __name__)

def check_auth():
    if 'user_id' not in session:
        return None
    return session['user_id']

@reports_bp.route('/csv', methods=['GET'])
def export_csv():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        start_date = end_date = None

    records = get_records(user_id, category, start_date, end_date)

    try:
        csv_data = generate_csv(records)
        output = BytesIO(csv_data)
        output.seek(0)

        return send_file(
            output,
            mimetype='text/csv',
            as_attachment=True,
            download_name=f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )
    except Exception as e:
        return jsonify({'error': f'Error generating CSV: {str(e)}'}), 500

@reports_bp.route('/excel', methods=['GET'])
def export_excel():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        start_date = end_date = None

    records = get_records(user_id, category, start_date, end_date)

    try:
        excel_data = generate_excel(records)
        output = BytesIO(excel_data)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=f"records_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        )
    except Exception as e:
        return jsonify({'error': f'Error generating Excel: {str(e)}'}), 500

@reports_bp.route('/pdf', methods=['GET'])
def export_pdf():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        start_date = end_date = None

    records = get_records(user_id, category, start_date, end_date)
    stats = get_record_statistics(user_id, category, start_date, end_date)

    try:
        pdf_data = generate_pdf_summary(records, stats)
        output = BytesIO(pdf_data)
        output.seek(0)

        return send_file(
            output,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
    except Exception as e:
        return jsonify({'error': f'Error generating PDF: {str(e)}'}), 500

@reports_bp.route('/summary', methods=['GET'])
def get_summary():
    user_id = check_auth()
    if not user_id:
        return jsonify({'error': 'Not authenticated'}), 401

    category = request.args.get('category')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    try:
        if start_date:
            start_date = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
        if end_date:
            end_date = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
    except ValueError:
        start_date = end_date = None

    records = get_records(user_id, category, start_date, end_date)
    stats = get_record_statistics(user_id, category, start_date, end_date)

    return jsonify({
        'statistics': stats,
        'record_count': len(records)
    }), 200
