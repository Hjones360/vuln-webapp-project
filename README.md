# Vulnerable Web App (Flask Security Training Project)

This is a deliberately vulnerable Flask-based web application created for hands-on cybersecurity practice and OWASP Top 10 training. It includes basic user authentication, image uploads, personal galleries, and text-based post creation — all intentionally coded without validations or security protections.

> **Disclaimer:** This app is intentionally insecure and should only be used in controlled environments for ethical hacking and security education. **Do not deploy it in production.**

---

##  Features

- User registration and login system
- User profile page displaying username and email
- Password change functionality
- Image upload and personal gallery views
- Simple post creation with SQLite database storage
- Deployed using PythonAnywhere with WSGI configuration

---

## Technologies Used

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, Jinja2 Templates
- **Hosting:** PythonAnywhere
- **Tools/Concepts:** Linux CLI, Bash, Git, GitHub, WSGI, OWASP Top 10

---

## Learning Goals

This project helped me understand:

- How insecure web apps are built and where vulnerabilities arise
- Common threats like SQL Injection, insecure file uploads, and IDOR
- Secure development lifecycle and how to plan mitigation
- End-to-end deployment using a cloud-based Linux environment

---

## Live Demo

[https://jjones404.pythonanywhere.com](https://jjones404.pythonanywhere.com)

---

## Project Structure

vuln_webapp/ ├── app.py ├── database.db (excluded in Git) ├── static/ │ └── uploads/ ├── templates/ │ ├── base.html │ ├── index.html │ ├── login.html │ ├── register.html │ ├── profile.html │ ├── change_password.html │ ├── gallery.html │ └── create_post.html └── README.md


---

## About Me

 Hi, I’m [@Hjones360](https://github.com/Hjones360) — an aspiring cybersecurity professional passionate about learning how apps are broken so I can learn how to build and protect them better.

---

## Contact & Connect

- GitHub: [Hjones360](https://github.com/Hjones360)
- LinkedIn: _(https://www.linkedin.com/in/houston-jones-8999b412b/)_
