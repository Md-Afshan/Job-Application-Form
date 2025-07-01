from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
import os
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = Flask(__name__)

# Mail configuration from environment
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')  # Your email
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')  # App password
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Upload folder & allowed extensions
UPLOAD_FOLDER = 'uploads/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

# Ensure uploads folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('job_application.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        dob = request.form['dob']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        area_code = request.form['area-code']
        cover_letter = request.form['cover-letter']
        resume = request.files['resume']

        # Save uploaded resume
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            # Ensure uploads folder exists (again here just in case)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])

            resume.save(filepath)

            # Prepare email
            msg = Message(
                subject=f'New Job Application from {first_name} {last_name}',
                sender=email,  # From the applicant
                recipients=[os.environ.get('MAIL_USERNAME')]  # To the owner
            )

            msg.body = f'''
New Job Application Received:

First Name: {first_name}
Last Name: {last_name}
Date of Birth: {dob}
Gender: {gender}
Phone: {phone}
Email: {email}
Location: {location}
Area Code: {area_code}

Cover Letter:
{cover_letter}
            '''

            with app.open_resource(filepath) as f:
                msg.attach(filename, "application/octet-stream", f.read())

            mail.send(msg)

            # Optionally delete file after sending
            os.remove(filepath)

            return redirect(url_for('thank_you'))

        return 'File upload failed or invalid file type.'

    except Exception as e:
        return f"An error occurred: {str(e)}"

@app.route('/thank-you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
