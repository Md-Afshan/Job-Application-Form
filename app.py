from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Mail Configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('job_application.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Form Inputs
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

        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            file_data = resume.read()

            msg = Message(
                subject=f"New Job Application from {first_name} {last_name}",
                sender=email,
                recipients=[app.config['MAIL_USERNAME']]
            )

            msg.body = f"""
Job Application Submitted:

Name       : {first_name} {last_name}
DOB        : {dob}
Gender     : {gender}
Phone      : {phone}
Email      : {email}
Location   : {location}
Area Code  : {area_code}

Cover Letter:
{cover_letter}
"""

            msg.attach(filename, "application/pdf", file_data)

            mail.send(msg)
            return redirect(url_for('thank_you'))

        return "Invalid file type. Upload only PDF/DOC/DOCX."

    except Exception as e:
        return f"❌ Error occurred: {str(e)}"

@app.route('/thank-you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    app.run(debug=True)
