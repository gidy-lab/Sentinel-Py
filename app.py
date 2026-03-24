import os
import subprocess
import csv
from io import StringIO
from flask import Flask, render_template, request, redirect, url_for, make_response
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'instance', 'siem.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())
    event_type = db.Column(db.String(50))
    source_ip = db.Column(db.String(50))
    message = db.Column(db.Text)
    severity = db.Column(db.String(20))

def get_service_status():
    # Checks if your collector is running
    return True # Simplified for testing, usually uses subprocess check

@app.route('/')
def index():
    alerts = Alert.query.order_by(Alert.timestamp.desc()).all()
    stats = {
        'total': len(alerts),
        'high': len([a for a in alerts if a.severity == 'High']),
        'medium': len([a for a in alerts if a.severity == 'Medium'])
    }
    return render_template('index.html', alerts=alerts, online=get_service_status(), stats=stats)

# NEW: Export to CSV for Reports
@app.route('/export')
def export_csv():
    alerts = Alert.query.all()
    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['ID', 'Timestamp', 'Threat Type', 'Source IP', 'Severity'])
    for a in alerts:
        cw.writerow([a.id, a.timestamp, a.event_type, a.source_ip, a.severity])
    
    response = make_response(si.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=sentinel_report.csv"
    response.headers["Content-type"] = "text/csv"
    return response

# NEW: Delete specific logs
@app.route('/delete', methods=['POST'])
def delete_logs():
    log_ids = request.form.getlist('log_ids')
    if log_ids:
        Alert.query.filter(Alert.id.in_(log_ids)).delete(synchronize_session=False)
        db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    os.makedirs(os.path.join(basedir, 'instance'), exist_ok=True)
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)