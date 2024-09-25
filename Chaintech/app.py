import requests
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///submissions.db'
db = SQLAlchemy(app)

# Model to store submission data
class Submission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)

# Sample quotes
quotes = [
    "Life is what happens when you're busy making other plans.",
    "The greatest glory in living lies not in never falling, but in rising every time we fall.",
    "The purpose of our lives is to be happy."
]

# Function to fetch weather information using OpenWeatherMap API
def get_weather():
    api_key = "Weather_map_api_key"
    city = "New York"  # Change the city to your preferred one
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()
        weather = {
            "city": city,
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"].capitalize(),
            "icon": data["weather"][0]["icon"]
        }
    except Exception as e:
        weather = None

    return weather

# Home route to display form and dynamic content
@app.route('/')
def home():
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    random_quote = random.choice(quotes)
    weather = get_weather()
    return render_template('index.html', time=now, quote=random_quote, weather=weather)

# Route to handle form submission
@app.route('/submit', methods=['POST'])
def submit():
    name = request.form.get('name')
    email = request.form.get('email')

    # Save submission to the database
    new_submission = Submission(name=name, email=email)
    db.session.add(new_submission)
    db.session.commit()

    # Redirect to the submissions page
    return redirect('/submissions')

# Route to display all stored submissions
@app.route('/submissions')
def submissions():
    all_submissions = Submission.query.all()
    return render_template('submissions.html', submissions=all_submissions)

# Run the application
if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables
    app.run(debug=True)
