# AI-Powered Literacy Assistant for Neo-Learners

## Project Overview

The AI-Powered Literacy Assistant is a web-based learning platform designed to improve literacy skills for neo-learners. The system provides structured learning content, assessments, learner progress tracking, gamification through XP and leaderboards, and certificate generation upon course completion.

This project is developed as part of the Infosys Internship Program.

---

## Tech Stack

### Backend
- Python
- Flask
- Flask-JWT-Extended
- MySQL
- MySQL Connector
- Werkzeug (Password Hashing)

### API Testing
- Postman

### Database
- MySQL

---

## Features

### User Authentication
- User Registration
- User Login (JWT Authentication)
- Password Hashing

### User Management
- User Profile
- Dashboard

### Learning Module
- Curriculum
- Lessons
- Lesson Materials

### Progress Tracking
- Complete Lesson
- XP Tracking
- Streak Tracking
- Completed Lessons

### Assessment Module
- Reading Score
- Writing Score
- Comprehension Score
- Overall Score Calculation
- Automatic Proficiency Level Update

### Gamification
- Leaderboard
- Certificate Generation

---

## Database Tables

- users
- learner_profiles
- curriculum
- lessons
- lesson_materials
- lesson_categories
- difficulty_levels
- languages
- lesson_progress
- assessment_results
- certificates

---

## Authentication

JWT Authentication is used.

After successful login, every protected API requires:

Authorization

Bearer <JWT_TOKEN>

---

## Folder Structure

backend/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
│
├── routes/
│ ├── user_routes.py
│ ├── curriculum_routes.py
│ ├── lesson_routes.py
│ ├── lesson_material_routes.py
│ ├── progress_routes.py
│ ├── assessment_routes.py
│ ├── leaderboard_routes.py
│ └── certificate_routes.py
│
├── services/
├── models/
└── utils/

---

## How to Run

### Clone Repository

git clone <repository-url>

### Install Dependencies

pip install -r requirements.txt

### Configure Database

Create the MySQL database and import the SQL tables.

Update database.py with:

- Host
- Username
- Password
- Database Name

### Start Server

python app.py

Server runs on:

http://127.0.0.1:5000

---

## Future Enhancements

- AI Chatbot Integration
- Speech Recognition
- OCR-Based Reading Assessment
- Personalized Learning Recommendations
- Mobile Application

---

## Author

Isha Agarwal

Infosys Internship Project