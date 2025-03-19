
from flask import Flask, render_template, request, redirect, url_for, session
from encryptor import encrypt_file
import os
import smtplib
from email.message import EmailMessage

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Dummy Login Details
users = {"admin": "password123"}

# Email Configuration
SENDER_EMAIL = "bharanikumar018@gmail.com"
APP_PASSWORD = "jnmy akir ugoy shee" # Your Gmail App Password

# Function to send email with encrypted file
def send_email(receiver_email, subject, description, attachment_path):
    try:
        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = SENDER_EMAIL
        msg['To'] = receiver_email
        msg.set_content(description)

        # Attach encrypted file
        with open(attachment_path, 'rb') as attachment:
            msg.add_attachment(attachment.read(), maintype='application', subtype='octet-stream', filename=os.path.basename(attachment_path))

        # Send Email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(SENDER_EMAIL, APP_PASSWORD)
            smtp.send_message(msg)

        print("✅ Email sent successfully!")
    
    except Exception as e:
        print(f"❌ Failed to send email: {e}")

# Index Route (File Upload)
@app.route('/', methods=['GET', 'POST'])
def index():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        file = request.files['file']
        receiver_email = request.form['receiver_email']
        subject = request.form['subject']
        description = request.form['description']

        file_path = os.path.join('uploads', file.filename)
        file.save(file_path)

        # Encrypt File
        encrypted_file = encrypt_file(file_path, 'key/public_key.pem')

        # Send Email with Encrypted File
        send_email(receiver_email, subject, description, encrypted_file)

        return render_template('success.html', encrypted_file=encrypted_file)

    return render_template('index.html')

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username] == password:
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return "❌ Invalid username or password."
    
    return render_template('login.html')

# Register Route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            return "❌ Passwords do not match. Please try again."

        users[username] = password
        return render_template('register_success.html')  # Display Success Page
    
    return render_template('register.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    if not os.path.exists('uploads'):
        os.makedirs('uploads')
    app.run(debug=True)
