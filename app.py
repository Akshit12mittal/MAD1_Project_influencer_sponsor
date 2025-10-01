from flask import Flask, render_template

app= Flask(__name__)

import config

import models

import routes
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

if __name__ == '__main__':
    app.run(debug=True)

from models import User_entry, Influencer, Sponsor,Campaign