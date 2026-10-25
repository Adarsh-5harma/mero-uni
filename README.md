# Mero Uni 🇳🇵 – CS & AI Resources Platform

The ultimate resource hub for Computer Science & Artificial Intelligence students in Nepal.

### Features
- Semester-wise subjects and resources
- Notes, question banks, lab files
- Clean, responsive design
- Built with Django 5.2 + Whitenoise

### Live Site
https://mero-uni.com

### Local Setup
```bash
git clone https://github.com/Adarsh-5harma/mero-uni.git
cd mero-uni
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Fill your DB details
python manage.py migrate
python manage.py runserver

Made with ❤️ by Adarsh Sharma
AKA Mr_Ikigai

### Development and deployment

Every push to `develop` or `main` runs migration checks, Django security checks,
tests, and static-file collection through GitHub Actions.

Production deployment happens only after CI succeeds. On the cPanel server, set
`APP_VENV` to the Python environment created by **Setup Python App**, pull the
tested `main` branch, and run `bash deploy/deploy_cpanel.sh` from the application
directory. Keep the production `.env` on the server; never add it to Git.
