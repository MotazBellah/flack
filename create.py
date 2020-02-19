import os
from flask import Flask
from models import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://empawzdedkzmzu:ec111b26dda56b50cd61a648b60eebda842e2189b782ff308a8d56d3c1a512c6@ec2-184-72-236-3.compute-1.amazonaws.com:5432/d8s47squ17rp4l"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

def main():
    db.create_all()

if __name__ == "__main__":
    with app.app_context():
        main()
