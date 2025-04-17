# Task 5: Full Weekly Internship Report (Tasks 1-4)

This report documents all major actions, commands, and results from Tasks 1 through 4, completed during the internship.

---

## ✅ Task 1: GitHub Repositories and Documentation

**Objective:** Create one public and one private GitHub repository. Push existing project using Git CLI. Document everything.

### 🔹 Repositories Created
- **Public:** [vuln-webapp-project](https://github.com/Hjones360/vuln-webapp-project)
- **Private:** `vuln-webapp-pri`

### 🔹 Commands Used
```bash
git init
git remote add origin https://github.com/Hjones360/vuln-webapp-project.git
git add .
git commit -m "Initial commit - Vulnerable Flask Web App for Security Learning"
git push -u origin main
```

### 🔹 Tags
```bash
git tag v1
git push origin v1
```

### 🔹 Document File Created
- `week1_readme.md`: Documented setup, CLI usage, and tasks

---

## ✅ Task 2: Visual Studio Integration and Version Control (v1–v4)

**Objective:** Use Git in VS Code to track improvements across insecure and secure versions.

### 🔹 Versions Created
| Version | Summary |
|---------|---------|
| `v1` | Insecure base: plain text passwords, no validation |
| `v2` | Password hashing with `werkzeug.security` |
| `v3` | Input validation, duplicate user checks |
| `v4` | File upload restrictions and error handling |

### 🔹 Git Commands
```bash
git tag v2
git push origin v2
git tag v3
git push origin v3
git tag v4
git push origin v4
```

---

## ✅ Task 3: Dockerization of Flask App

**Objective:** Package the app using Docker and push the image to Docker Hub.

### 🔹 Docker Hub Repo
- Username: `hjones360`
- Image: `hjones360/vuln-webapp:latest`

### 🔹 Files Created
- `requirements.txt`
- `Dockerfile`

### 🔹 Commands Used
```bash
pip freeze > requirements.txt
# Dockerfile was created and edited in VS Code
docker build -t hjones360/vuln-webapp:latest .
docker run -p 5000:5000 hjones360/vuln-webapp
docker login
docker push hjones360/vuln-webapp:latest
```

---

## ✅ Task 4: Hourly Discord Notification Script

**Objective:** Automate a script using Windows Task Scheduler that sends a timestamp to Discord every hour.

### 🔹 Script Created: `hourly_notifier.py`
```python
import requests
from datetime import datetime

WEBHOOK_URL = 'https://discord.com/api/webhooks/...'
now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
data = {"content": f"✅ Cron job ran at {now}"}
requests.post(WEBHOOK_URL, json=data)
```

### 🔹 Test Run Output
```bash
python hourly_notifier.py
Success: Sent at 2025-04-16 17:00:00
```

### 🔹 Scheduled Using
- Windows Task Scheduler
- Frequency: Every 1 hour
- Program path: `python.exe`
- Arguments: `hourly_notifier.py`
- Start in: Project folder path

---

## ✅ Status
All 4 tasks completed and verified successfully.
- All code versioned using Git (v1-v4)
- Docker container is live on Docker Hub
- Discord automation works hourly via Task Scheduler