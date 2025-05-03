from flask import Flask, json, jsonify, render_template, request, redirect, url_for, flash, session
import csv
import pandas as pd
import pickle
import json
import google.generativeai as genai
import os
from dotenv import load_dotenv
 
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
 
load_dotenv()
 
app = Flask(__name__)
app.secret_key = "your_secret_key"
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")
chat_session = None
 
CSV_FILE = 'users.csv'
DATA_FOLDER = os.path.join(os.getcwd(), 'data')
os.makedirs(DATA_FOLDER, exist_ok=True)
 
 # ==================== AUTHENTICATION ====================
def email_exists(email):
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
             if row and row[0] == email:
                 return True
    return False
 
def add_user(email, password):
    with open(CSV_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([email, password])
 
def check_user(email, password):
    if not os.path.exists(CSV_FILE):
        return False
    with open(CSV_FILE, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row and row[0] == email and row[1] == password:
                return True
    return False
 
 # ==================== ROUTES ====================
@app.route('/')
def login_page():
    return render_template('login.html')
 
@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['password']
 
    if check_user(email, password):
        session['user'] = email
        return redirect(url_for('index'))
    else:
        flash("Invalid email or password. Please try again.", "error")
        return redirect(url_for('login_page'))
 
@app.route('/signup')
def signup_page():
    return render_template('signup.html')
 
@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    password = request.form['password']
    confirm_password = request.form['confirm_password']
 
    if email_exists(email):
        flash("User already exists. Please log in.", "error")
        return redirect(url_for('signup_page'))
 
    if password != confirm_password:
        flash("Passwords do not match. Please try again.", "error")
        return redirect(url_for('signup_page'))
 
    add_user(email, password)
    flash("Account created successfully! Please log in.", "success")
    return redirect(url_for('login_page'))
 
@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        flash("You must log in first.", "error")
        return redirect(url_for('login_page'))
 
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("You have been logged out.", "info")
    return redirect(url_for('login_page'))
 
@app.route('/about')
def about():
    return render_template('aboutus.html')
 
@app.route('/AiCounseller')
def AiCounseller():
    return render_template('aiAdvisor.html')
 
@app.route('/save_data', methods=['POST'])
def save_data():
    try:
        form_data = request.form.to_dict()
        if not form_data:
            return jsonify({"error": "No data received. Ensure all form fields have 'name' attributes."}), 400
 
        user_email = session.get('user', 'default')
        filename = f"career_data_{user_email.replace('@', '_at_')}.json"
        file_path = os.path.join(DATA_FOLDER, filename)
        with open(file_path, 'w') as json_file:
            json.dump(form_data, json_file, indent=4)
 
        return jsonify({"message": "Data saved successfully!", "file_path": file_path})
    except Exception as e:
         return jsonify({"error": str(e)}), 500
 
 
@app.errorhandler(404)
def page_not_found(e):
     return render_template("404.html"),404
 
 # ==================== AI ====================
def get_student_profile_from_json():
    user_email = session.get('user', 'default')
    filename = f"career_data_{user_email.replace('@', '_at_')}.json"
    file_path = os.path.join(DATA_FOLDER, filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return "\n".join([f"{key}: {value}" for key, value in data.items()])
 
 
def initialize_yosker_chat():
    profile = get_student_profile_from_json()
    if not profile:
        profile = "No student data available."
 
    initial_prompt = f"""
You are MentorMind, a friendly and knowledgeable AI career counselor.
 
Start by analyzing the following student profile and predict the most suitable stream:
 {profile}
 
 Explain why this stream is suitable based on their marks, interests, and preferences in as short as possible.
 Then continue with this structured flow:
 1. Confirm the student's details and ask any missing ones.
 2. Ask if they agree with the suggested stream.
 3. List 7 top career options in that stream (short bullets).
 4. Ask which career they are interested in.
 5. Provide step-by-step guidance for that career.
 6. End with helpful suggestions and offer to connect with institutions if they wish.
 NOTE : make sure the response is not big and user friendly and a pragraph 
 """
 
    return model.start_chat(history=[{"role": "user", "parts": [initial_prompt]}])
 
def get_user_response(user_input):
    global chat_session
    if chat_session is None:
        chat_session = initialize_yosker_chat()
    response = chat_session.send_message(user_input)
    return response.text.strip()
 
@app.route("/talk", methods=["GET", "POST"])
def talk():
     if 'user' not in session:
         flash("Please log in to talk with AI.", "error")
         return redirect(url_for('login_page'))
 
     global chat_session
     if "chat" not in session:
         session["chat"] = []
         chat_session = initialize_yosker_chat()
 
     if request.method == "POST":
         user_input = request.form["user_input"]
         bot_response = get_user_response(user_input)
         session["chat"].append({"user": user_input, "bot": bot_response})
         session.modified = True
 
     return render_template("chat.html", chat_history=session["chat"])
 
@app.route("/reset")
def reset_chat():
     session.pop("chat", None)
     global chat_session
     chat_session = initialize_yosker_chat()
     return redirect(url_for('talk'))
 
 # ==================== Email ====================
 
 
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
 
def generate_email_content(student_data):
     profile = "\n".join([f"{key}: {value}" for key, value in student_data.items()])
     prompt = f"""
 Hi {student_data.get('name', 'Student')},
 
 Warm greetings from MentorMind! This is MentorMind, your personalized AI career guidance assistant.
 
 Your aspiration is inspiring! Based on your profile, here's a recommended path:
 {profile}
 Please explore the suggested path and feel free to reach out if you'd like to connect with experts in this field.
 
 Best wishes,  
MentorMind | AI Career Assistant
 """
     try:
         response = model.generate_content(prompt)
         return response.text.strip() if response.text else "Explore your future with us!"
     except Exception as e:
         print(f"AI Error: {e}")
         return "Explore your future with us!"
 
 
def send_email(to_email, subject, body):
     try:
         msg = MIMEMultipart()
         msg["From"] = EMAIL_SENDER
         msg["To"] = to_email
         msg["Subject"] = subject
         msg.attach(MIMEText(body, "plain"))
 
         server = smtplib.SMTP("smtp.gmail.com", 587)
         server.starttls()
         server.login(EMAIL_SENDER, EMAIL_PASSWORD)
         server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
         server.quit()
         print(f"✅ Email sent to {to_email}")
     except Exception as e:
         print(f"❌ Error sending email: {e}")
 
@app.route('/send_email', methods=['POST'])
def send_email_route():
     try:
         if 'user' not in session:
             return jsonify({"error": "User not logged in"}), 401
 
         data = request.get_json()
         to_email = data.get("email")
 
         if not to_email:
             return jsonify({"error": "Email is required"}), 400
 
         # Use logged-in user's personalized data file
         user_email = session['user']
         filename = f"career_data_{user_email.replace('@', '_at_')}.json"
         file_path = os.path.join(DATA_FOLDER, filename)
 
         if not os.path.exists(file_path):
             return jsonify({"error": "No career data found for this user. Please submit your form first."}), 400
 
         with open(file_path, 'r') as json_file:
             student_data = json.load(json_file)
 
         subject = "Your Personalized Career Guidance"
         body = generate_email_content(student_data)
         send_email(to_email, subject, body)
 
         return jsonify({"message": f"Email sent to {to_email}"})
     except Exception as e:
         return jsonify({"error": str(e)}), 500
 
 
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9082)