# API Documentation

Base URL

http://127.0.0.1:5000

---

# Authentication

## Register

POST /api/register

Request

```json
{
    "full_name":"Isha Agarwal",
    "email":"isha@gmail.com",
    "password":"123456",
    "preferred_language_id":1
}
```

Response

```json
{
    "message":"User registered successfully.",
    "user_id":1
}
```

---

## Login

POST /api/login

Request

```json
{
    "email":"isha@gmail.com",
    "password":"123456"
}
```

Response

```json
{
    "message":"Login Successful",
    "access_token":"JWT_TOKEN"
}
```

---

# User APIs

## Profile

GET /api/profile

Authentication Required

---

## Dashboard

GET /api/dashboard

Authentication Required

---

# Curriculum APIs

## Get Curriculum

GET /api/curriculum

Authentication Required

---

# Lesson APIs

## Get All Lessons

GET /api/lessons

Authentication Required

---

## Get Lessons by Curriculum

GET /api/lessons/{curriculum_id}

Authentication Required

Example

GET /api/lessons/1

---

## Get Lesson Details

GET /api/lesson/{lesson_id}

Authentication Required

---

## Get Lesson Materials

GET /api/lesson-materials/{lesson_id}

Authentication Required

---

# Progress APIs

## Complete Lesson

POST /api/complete-lesson

Authentication Required

Request

```json
{
    "lesson_id":1
}
```

---

## My Progress

GET /api/my-progress

Authentication Required

---

# Assessment APIs

## Submit Assessment

POST /api/submit-assessment

Authentication Required

Request

```json
{
    "lesson_id":1,
    "reading_score":80,
    "writing_score":90,
    "comprehension_score":85
}
```

---

# Leaderboard APIs

GET /api/leaderboard

Authentication Required

---

# Certificate APIs

POST /api/generate-certificate

Authentication Required

Request

```json
{
    "curriculum_id":1
}
```

---

# Status Codes

200 OK

201 Created

400 Bad Request

401 Unauthorized

404 Not Found

500 Internal Server Error

---

# Authentication Header

Authorization

Bearer <JWT_TOKEN>