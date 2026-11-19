# CareerConnect – Django Job Portal

## Project Overview

CareerConnect is a web-based job portal developed using Python and Django. It connects students looking for jobs with companies that want to recruit candidates.

Students can create profiles, upload resumes, search for jobs, and track their applications. Companies can post jobs, manage applications, and monitor recruitment performance.

## Features

### Student Features
- Student registration and login
- Create and update student profiles
- Upload resumes and profile pictures
- Browse and search job opportunities
- Apply for jobs
- Track application status
- Receive notifications

### Company Features
- Company profile management
- Post new job vacancies
- Edit and delete job postings
- View student applications
- Update application status
- Company dashboard and analytics
- Performance reports

### Admin Features
- Admin analytics dashboard
- Monitor students, companies, jobs, and applications
- Export reports in PDF and Excel formats

## Technologies Used

- **Frontend:** HTML, CSS, JavaScript, Bootstrap (if used)
- **Backend:** Python, Django
- **Database:** SQLite
- **Charts:** Chart.js
- **Development Tools:** Visual Studio Code, Git, GitHub

## Project Structure

```text
CareerConnect/
│
├── accounts/
├── config/
├── jobs/
├── profiles/
├── templates/
├── media/
├── manage.py
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/subhashjiddu3-jpg/carrerconnect.git
```

### 2. Open the project folder

```bash
cd carrerconnect
```

### 3. Create a virtual environment

```bash
python -m venv .venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 5. Install dependencies

Install the packages required by the project.

```bash
pip install django pillow openpyxl reportlab
```

Install any additional packages used by your project.

### 6. Apply database migrations

```bash
python manage.py migrate
```

### 7. Create an administrator account

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

Open the application:

http://127.0.0.1:8000/

## Testing

The project was manually tested for:

- Student registration and login
- Student profile management
- Job posting and applications
- Application status updates
- Student notifications
- Company dashboard
- Admin analytics
- PDF and Excel exports
- Mobile responsive layouts

## Learning Outcomes

Through this project, I practised:

- Python and Django development
- Django models, views, URLs, and templates
- CRUD operations
- Authentication and authorization
- File uploads
- Database relationships
- Dashboard development
- Git and GitHub version control
- Manual application testing

## Future Enhancements

- Online interview scheduling
- Advanced job recommendations
- Email verification
- Resume parsing
- Cloud deployment

## Author

**Subhash**

GitHub: https://github.com/subhashjiddu3-jpg

---

**CareerConnect – Connecting Students with Opportunities.**