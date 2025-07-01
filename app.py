from flask import Flask, request, render_template, redirect, url_for
from flask_mail import Mail, Message
import os
import mimetypes
from werkzeug.utils import secure_filename
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

app = Flask(__name__)

# Mail configuration from environment variables
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

# Upload configuration
UPLOAD_FOLDER = 'uploads/'
ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB max

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('job_application.html')

@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Form fields
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        dob = request.form['dob']
        gender = request.form['gender']
        phone = request.form['phone']
        email = request.form['email']
        location = request.form['location']
        area_code = request.form['area-code']
        cover_letter = request.form['cover-letter']
        
        # Handle file
        resume = request.files['resume']
        if resume and allowed_file(resume.filename):
            filename = secure_filename(resume.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            resume.save(filepath)

            # Compose email
            msg = Message(
                subject=f'New Job Application from {first_name} {last_name}',
                sender=app.config['MAIL_USERNAME'],
                recipients=[app.config['MAIL_USERNAME']],
                reply_to=email
            )
            msg.body = f'''
New job application received:

Name: {first_name} {last_name}
Date of Birth: {dob}
Gender: {gender}
Phone: {phone}
Email: {email}
Location: {location}
Area Code: {area_code}
Cover Letter:
{cover_letter}

Reply to this email to contact the applicant.
            '''

            mimetype = mimetypes.guess_type(filename)[0] or 'application/octet-stream'
            with app.open_resource(filepath) as f:
                msg.attach(filename, mimetype, f.read())

            mail.send(msg)
            os.remove(filepath)
            return redirect(url_for('thank_you'))

        return 'Invalid file or upload failed.'

    except Exception as e:
        return f'An error occurred: {str(e)}'

@app.route('/thank-you')
def thank_you():
    return render_template('thanks.html')

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)
