from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    goal = db.Column(db.String(120), nullable=False)
    timing = db.Column(db.String(120), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    emoji = db.Column(db.String(10), nullable=False)
    why_reason = db.Column(db.String(200), nullable=False)


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date =  db.Column(db.Date, nullable=False)
    completion = db.Column(db.Boolean, nullable=False)

@app.route('/')
def home():
    return "Welcome to the Habit Tracker API!"

if __name__ == '__main__':
    app.run(debug=True)     