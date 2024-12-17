from flask import Flask, request, jsonify, render_template, redirect, url_for, session, flash
from pymongo import MongoClient
import joblib
from flask_cors import CORS
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'
CORS(app)

# MongoDB Configuration
client = MongoClient('mongodb://localhost:27017')  # Update if MongoDB is on a different host
db = client['aluminium_project']
users_collection = db['users']

# Load ML Models
best_model_uts = joblib.load('models/best_model_uts.pkl')
best_model_elongation = joblib.load('models/best_model_elongation.pkl')
best_model_conductivity = joblib.load('models/best_model_conductivity.pkl')

# Routes
@app.route('/')
def signup_page():
    return render_template('wt-SignUp.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('wt-SignUp.html')

    data = request.form
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        flash("All fields are required.", "error")
        return render_template('wt-SignUp.html')

    # Check if user already exists
    if users_collection.find_one({'email': email}):
        flash("Email already exists. Please log in.", "error")
        return render_template('wt-LogIn.html')

    # Insert new user into MongoDB
    users_collection.insert_one({
        'username': username,
        'email': email,
        'password': password
    })

    flash("Signup successful! Please log in.", "success")
    return render_template('wt-LogIn.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('wt-LogIn.html')

    data = request.form
    email = data.get('email')
    password = data.get('password')

    user = users_collection.find_one({'email': email, 'password': password})
    if user:
        session['user'] = str(user['_id'])
        flash("Login successful!", "success")
        return redirect(url_for('alu'))
    else:
        flash("Invalid email or password.", "error")
        return redirect(url_for('login'))

@app.route('/alu', methods=['GET', 'POST'])
def alu():
    # Check if the user is logged in
    if 'user' not in session:
        flash("Please log in to access this page.", "error")
        return redirect(url_for('login'))

    # Initialize default predictions as None
    uts_prediction = None
    elongation_prediction = None
    conductivity_prediction = None

    if request.method == 'POST':
        try:
            # Fetch input data from the form
            input_data = {
                "casting_temp": float(request.form['casting_temp']),
                "cooling_temp": float(request.form['cooling_temp']),
                "casting_speed": float(request.form['casting_speed']),
                "bar_entry_temp": float(request.form['bar_entry_temp']),
                "emulsion_temp": float(request.form['emulsion_temp']),
                "emulsion_pressure": float(request.form['emulsion_pressure']),
                "emulsion_concentration": float(request.form['emulsion_concentration']),
                "quench_pressure": float(request.form['quench_pressure'])
            }

            # Map form input keys to match model's training column names
            feature_mapping = {
                "casting_temp": "Casting_Temp_C",
                "cooling_temp": "Cooling_Water_Temp_C",
                "casting_speed": "Casting_Speed_m_per_min",
                "bar_entry_temp": "Cast_Bar_Entry_Temp_C",
                "emulsion_temp": "Emulsion_Temp_C",
                "emulsion_pressure": "Emulsion_Pressure_bar",
                "emulsion_concentration": "Emulsion_Concentration_percent",
                "quench_pressure": "Rod_Quench_Water_Pressure_bar"
            }

            # Standardize input features to match the trained model
            standardized_features = {
                feature_mapping[key]: value for key, value in input_data.items()
            }

            # Convert the standardized features to a DataFrame
            features_df = pd.DataFrame([standardized_features])

            # Ensure DataFrame columns match model's training columns
            required_columns = [
                "Casting_Temp_C", "Cooling_Water_Temp_C", "Casting_Speed_m_per_min", 
                "Cast_Bar_Entry_Temp_C", "Emulsion_Temp_C", "Emulsion_Pressure_bar", 
                "Emulsion_Concentration_percent", "Rod_Quench_Water_Pressure_bar"
            ]
            features_df = features_df.reindex(columns=required_columns)

            # Make predictions
            uts_prediction = best_model_uts.predict(features_df)[0]
            elongation_prediction = best_model_elongation.predict(features_df)[0]
            conductivity_prediction = best_model_conductivity.predict(features_df)[0]

            # Debugging predictions
            print("Predictions:", uts_prediction, elongation_prediction, conductivity_prediction)

        except KeyError as ke:
            flash(f"Missing form input: {str(ke)}", "error")
            print("KeyError:", str(ke))
        except ValueError as ve:
            flash(f"Invalid input type: {str(ve)}", "error")
            print("ValueError:", str(ve))
        except Exception as e:
            flash(f"Prediction failed: {str(e)}", "error")
            print("Prediction Error:", str(e))

    # Render the template with predictions (None if no POST or failure)
    return render_template('alu.html',
                           uts=uts_prediction,
                           elongation=elongation_prediction,
                           conductivity=conductivity_prediction)




@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("Logged out successfully.", "success")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
