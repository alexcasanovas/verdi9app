from . import db
from sqlalchemy.sql import func 

class Commands(db.Model):
    
    print_sess = db.Column(db.String(100), primary_key=True)
    filename = db.Column(db.String(150), primary_key=True)
    data = db.Column(db.LargeBinary)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    email = db.Column(db.String(100))