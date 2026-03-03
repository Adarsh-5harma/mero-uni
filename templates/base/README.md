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

Made with ❤️ by Adar5h 5harma
AKA Mr_Ikigai
print("hello world")
version 1.0