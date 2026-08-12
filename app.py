from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'habit_tracker_secret_key'
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
    emoji = db.Column(db.String(10), nullable=True)
    why_reason = db.Column(db.String(200), nullable=False)


class Logs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    completion = db.Column(db.Boolean, nullable=False)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        hashed_password = generate_password_hash(password)
        new_user = User(email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return "Signup successful!"
    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(email=email).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            return "Login successful!"
        else:
            return "Invalid email or password"

    return render_template('login.html')

@app.route('/add_habit', methods=['GET', 'POST'])
def add_habit():
    if 'user_id'  not in session:
        return "please  log in first"

    if request.method == 'POST':
        new_habit = Habit(
            user_id=session['user_id'],
            name=request.form['name'],
            goal=request.form['goal'],
            timing=request.form['timing'],
            duration=request.form['duration'],
            emoji=request.form['emoji'],
            why_reason=request.form['why_reason']
        )
        db.session.add(new_habit)
        db.session.commit()

        return "Habit added successfully!"
    return render_template('add_habit.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return f"Welcome back, {user.email}!"
    else:
        return "Please log in first"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return "Logged out successfully!"       


@app.route('/')
def home():
    return "Welcome to the Habit Tracker API!"


if __name__ == '__main__':
    app.run(debug=True)