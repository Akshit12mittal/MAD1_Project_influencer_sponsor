from app import app
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


db = SQLAlchemy(app)
migrate = Migrate(app, db)


# models.py
class User_entry(db.Model):
    __tablename__ = 'user_entry'
    id = db.Column(db.String, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(50), nullable=False)




class Influencer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    niche = db.Column(db.String(120), nullable=False)
    platform = db.Column(db.String(120), nullable=False)
    followers = db.Column(db.Integer, nullable=False)
    password = db.Column(db.String(120), nullable=False)


class Sponsor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(120), nullable=False)
    industry = db.Column(db.String(120), nullable=False)
    budget = db.Column(db.Float, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)




class CampaignRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, nullable=False)
    sponsor_id = db.Column(db.Integer,  nullable=False)
    influencer_id = db.Column(db.Integer, nullable=False)
    status = db.Column(db.Integer, default=0)
    date_of_request = db.Column(db.DateTime, default=datetime.utcnow)
    date_of_modification = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Campaign(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sponsor_id=db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    budget = db.Column(db.Float, nullable=False)
    visibility = db.Column(db.String(20), nullable=False)
    goals = db.Column(db.String(500), nullable=True)
    status=db.Column(db.Boolean,default=True,nullable=False)





