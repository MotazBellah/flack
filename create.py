import os
from flask import Flask
from models import *

app = Flask(__name__)

# app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://syoilhbljjrvyv:35d64a02935af3684ac54adac250d21422a8e5c35b2d2d68bbfe87c9f79c097c@ec2-52-200-119-0.compute-1.amazonaws.com:5432/deevouk6kecicj"
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
