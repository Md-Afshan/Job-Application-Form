from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Email config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Absolute path for upload folder
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('job_application.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Ensure upload directory exists (absolute path)
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

        # Get form inputs
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        dob = request.form.get('dob')
        gender = request.form.get('gender')
        phone = request.form.get('phone')
        email = request.form.get('email')
        location = request.form.get('location')
        area_code = request.form.get('area-code')
        cover_letter = request.form.get('cover-letter')
        resume = request.files.get('resume')

        # File check
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(filepath)

            # Prepare and send email
            msg = Message(subject=f"New Application from {first_name} {last_name}",
                          sender=email,
                          recipients=[os.environ.get('MAIL_USERNAME')])

            msg.body = f'''
New Job Application Received:

First Name: {first_name}
Last Name: {last_name}
DOB: {dob}
Gender: {gender}
Phone: {phone}
Email: {email}
Location: {location}
Area Code: {area_code}

Cover Letter:
{cover_letter}
            '''

            with open(filepath, 'rb') as f:
                msg.attach(filename, "application/octet-stream", f.read())

            mail.send(msg)

            # Delete file after sending
            os.remove(filepath)

            return redirect(url_for('thank_you'))

        return "Invalid or missing file. Please upload a .pdf, .doc, or .docx file."

    except Exception as e:
        # Log error on screen for now
        return f"An error occurred: {e}"

@app.route('/thank-you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
