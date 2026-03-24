from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    event_type = db.Column(db.String(100))  # e.g., "Failed Login"
    source_ip = db.Column(db.String(50))
    message = db.Column(db.Text)
    severity = db.Column(db.String(20))     # Low, Medium, High