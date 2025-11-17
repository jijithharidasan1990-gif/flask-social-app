# Mini Social Media Project

A simple Flask-based mini social media app where users can:

* Register and log in
* Create posts (text + optional image/video)
* View all posts
* Like posts (frontend counter)
* Delete their own posts

---

## 📌 Features

### ✅ User Authentication

* User registration
* Login/Logout functionality
* Secure password hashing

### ✅ Post System

* Users can create posts with:

  * Text
  * Optional media (image/video)
* All posts displayed in a feed

### ✅ Like Button (Frontend)

* Each post has a like button with unique counters
* Works using JavaScript

### ✅ Media Uploads

* Uploaded media are stored in `static/uploads/`

### ✅ Delete Post

* Only post owner can delete their posts

---

## 📁 Project Structure

```
project_folder/
│
├── static/
│   └── uploads/
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   └── posts.html
│
├── app.py
├── requirements.txt
└── README.md
```

---

##
