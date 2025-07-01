
# 📝 Job Application Form – Flask Web App

A secure and user-friendly job application form built using **Flask**. Applicants can fill out their details, upload their resume, and automatically send the application to the employer via email.

---

## 📌 Key Features

* 🔐 Secure form submission using Flask
* 📄 Resume upload with allowed file types (PDF, DOC, DOCX)
* ✉️ Automatically sends form data and attached resume to the employer's email
* 🌐 Ready for deployment using GitHub + Render
* ⚙️ Email credentials managed securely through `.env` file (not exposed in public)

---

## 🗂️ Folder Structure

```
Job-Application-Form/
├── app.py               # Main Flask app
├── templates/           # HTML templates (form + thank you page)
│   ├── job_application.html
│   └── thanks.html
├── uploads/             # Stores uploaded resumes temporarily
├── static/              # Optional: For images, CSS, or JS
├── requirements.txt     # Python dependencies
├── .env                 # Contains Gmail credentials (excluded from GitHub)
├── .gitignore           # Prevents sensitive files from being pushed
```

---

## 🚀 Getting Started (Local Setup)

### ✅ 1. Clone the Repository

```bash
git clone https://github.com/Md-Afshan/Job-Application-Form.git
cd Job-Application-Form
```

### ✅ 2. Install Required Libraries

```bash
pip install -r requirements.txt
```

### ✅ 3. Create `.env` File (For Email Settings)

Inside your project folder, create a file named `.env` and add:

```env
MAIL_USERNAME=your_gmail_address@gmail.com
MAIL_PASSWORD=your_gmail_app_password
```

> 🔐 Use a [Gmail App Password](https://myaccount.google.com/apppasswords).
> Don’t use your actual Gmail login password.

### ✅ 4. Run the App

```bash
python app.py
```

Go to [http://localhost:5000](http://localhost:5000) to view the job application form.

---

## 🌐 Deploying to Render (Free Hosting)

1. Create a [Render.com](https://render.com/) account
2. Click "New Web Service" → Connect your GitHub repo
3. Set:

   * **Build command:**
     `pip install -r requirements.txt`
   * **Start command:**
     `gunicorn app:app`
4. Add these environment variables in Render’s dashboard:

   * `MAIL_USERNAME` → your Gmail address
   * `MAIL_PASSWORD` → your Gmail App Password

Your Flask job form will be live and accessible on the internet!

---

## 🔒 Security Best Practices

* Do **not** hardcode your email or password in `app.py`
* Use `.env` file locally and add it to `.gitignore`
* Never upload `.env` to GitHub
* Limit resume file size (e.g., 2MB) and type (PDF/DOC/DOCX only)

---

## Technical Output:
1)Applicant Opens the Form Page and fills the Form.
![jobapplication-1](https://github.com/user-attachments/assets/10e16019-395c-4c15-b618-233ae82bca48)

2)Backend Validates and Processes the Form.
![jobapplication-2](https://github.com/user-attachments/assets/865434ab-c291-408f-ab18-226891244fe7)

3)Redirects to ThankYou Page.
![jobapplication-3](https://github.com/user-attachments/assets/c5b43bfc-2e22-461d-9886-5b854d46a00d)

4)The Owner side recieves the email in form structure with attached pdf.
![jobapplication-4](https://github.com/user-attachments/assets/3324294c-eb7c-4cda-bbff-cbf52ee396c7)

## Live:
https://job-application-form-jlh0.onrender.com



