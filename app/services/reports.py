import pandas as pd
from io import BytesIO
from typing import List, Dict
from datetime import datetime

def generate_csv(records: List[Dict]) -> bytes:
    if not records:
        df = pd.DataFrame(columns=['id', 'title', 'category', 'value', 'timestamp', 'metadata'])
    else:
        df = pd.DataFrame(records)
        df = df[['id', 'title', 'category', 'value', 'timestamp', 'metadata']]

    return df.to_csv(index=False).encode('utf-8')

def generate_excel(records: List[Dict]) -> bytes:
    if not records:
        df = pd.DataFrame(columns=['id', 'title', 'category', 'value', 'timestamp', 'metadata'])
    else:
        df = pd.DataFrame(records)
        df = df[['id', 'title', 'category', 'value', 'timestamp', 'metadata']]

    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Records')
    output.seek(0)
    return output.getvalue()

def generate_pdf_summary(records: List[Dict], statistics: Dict) -> bytes:
    from weasyprint import HTML

    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {{
                font-family: Arial, sans-serif;
                margin: 40px;
                color: #333;
            }}
            h1 {{
                color: #2c3e50;
                border-bottom: 3px solid #3498db;
                padding-bottom: 10px;
            }}
            h2 {{
                color: #34495e;
                margin-top: 30px;
            }}
            .summary {{
                background-color: #ecf0f1;
                padding: 20px;
                border-radius: 5px;
                margin: 20px 0;
            }}
            .stat {{
                display: inline-block;
                margin: 10px 20px 10px 0;
            }}
            .stat-label {{
                font-weight: bold;
                color: #7f8c8d;
            }}
            .stat-value {{
                font-size: 1.3em;
                color: #2c3e50;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }}
            th {{
                background-color: #3498db;
                color: white;
                padding: 12px;
                text-align: left;
            }}
            td {{
                padding: 10px;
                border-bottom: 1px solid #ddd;
            }}
            tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .footer {{
                margin-top: 40px;
                text-align: center;
                color: #7f8c8d;
                font-size: 0.9em;
            }}
        </style>
    </head>
    <body>
        <h1>Records Summary Report</h1>
        <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>

        <div class="summary">
            <h2>Statistics</h2>
            <div class="stat">
                <div class="stat-label">Total Records</div>
                <div class="stat-value">{statistics['count']}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Total Value</div>
                <div class="stat-value">${statistics['sum']:.2f}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Average Value</div>
                <div class="stat-value">${statistics['average']:.2f}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Min Value</div>
                <div class="stat-value">${statistics['min']:.2f}</div>
            </div>
            <div class="stat">
                <div class="stat-label">Max Value</div>
                <div class="stat-value">${statistics['max']:.2f}</div>
            </div>
        </div>

        <h2>Recent Records</h2>
        <table>
            <thead>
                <tr>
                    <th>Title</th>
                    <th>Category</th>
                    <th>Value</th>
                    <th>Timestamp</th>
                </tr>
            </thead>
            <tbody>
    """

    for record in records[:50]:
        timestamp = record.get('timestamp', '')
        if timestamp:
            try:
                dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                timestamp = dt.strftime('%Y-%m-%d %H:%M')
            except:
                pass

        html_content += f"""
                <tr>
                    <td>{record.get('title', 'N/A')}</td>
                    <td>{record.get('category', 'N/A')}</td>
                    <td>${record.get('value', 0):.2f}</td>
                    <td>{timestamp}</td>
                </tr>
        """

    html_content += """
            </tbody>
        </table>

        <div class="footer">
            <p>This report contains a summary of your records data.</p>
        </div>
    </body>
    </html>
    """

    pdf_bytes = HTML(string=html_content).write_pdf()
    return pdf_bytes
