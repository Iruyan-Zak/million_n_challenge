from flask import Flask, render_template, redirect, request, url_for, abort
from flask_sqlalchemy import SQLAlchemy

app = Flask('million_per_n')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/codename.db'
db = SQLAlchemy(app)


class Post(db.Model):
    twitter = db.Column(db.String(32), primary_key=True)
    n = db.Column(db.Integer, nullable=False)

    def __init__(self, twitter: str, n: int):
        self.twitter = twitter
        self.n = n

    def __repr__(self):
        return f'{self.twitter}\t{self.n}'


@app.route('/', methods=['GET'])
def index():
    return 'get method'  # render_template('index.html')


@app.route('/', methods=['POST'])
def post():
    return 'post method'


db.create_all()
app.run(port=80)
