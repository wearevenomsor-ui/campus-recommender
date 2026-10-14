# Running Campus Event Recommender on Google Colab
**Project by: Adarsh S**

Yes! You can run this entire project inside **Google Colab** completely free.

---

## 🚀 The Fastest Method (Just Copy & Paste into Colab)

1. Open [Google Colab](https://colab.research.google.com/) and click **"New Notebook"**.
2. Create **3 Code Cells** and paste the code below into each cell:

---

### Cell 1: Install Requirements & Cloudflare
```python
# 1. Install dependencies
!pip install -q streamlit pandas numpy scikit-learn

# 2. Download Cloudflare Tunnel for Linux (Google Colab)
!wget -q -O cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
!chmod +x cloudflared
print("Setup complete!")
```

---

### Cell 2: Create App Files
Paste this entire block into Cell 2 to create the project files:
```python
%%writefile data_generator.py
import random
from datetime import datetime, timedelta
import numpy as np

random.seed(42)
np.random.seed(42)

CATEGORIES = ["Technology & AI", "Career & Networking", "Arts & Culture", "Sports & Wellness", "Academic & Research", "Social & Entertainment"]

TAGS_POOL = {
    "Technology & AI": ["Python", "Machine Learning", "Web Dev", "Cybersecurity", "Hackathon", "Cloud", "Robotics", "Data Science"],
    "Career & Networking": ["Resume Workshop", "Internship Fair", "Alumni Talk", "Startup Pitch", "Interview Prep", "Finance", "Leadership"],
    "Arts & Culture": ["Film Screening", "Live Music", "Theater", "Photography", "Debate Club"],
    "Sports & Wellness": ["Yoga", "Football Tournament", "Basketball League", "Mental Health", "Marathon"],
    "Academic & Research": ["Physics Seminar", "Biology Symposium", "Math Olympiad", "Paper Writing", "Ethics in Tech"],
    "Social & Entertainment": ["Trivia Night", "Gaming Lan Party", "Food Fest", "Campus Carnival", "Comedy Club"]
}

EVENT_TEMPLATES = [
    ("AI & Machine Learning Bootcamp", "Technology & AI", ["Python", "Machine Learning", "Data Science"], "Hands-on crash course on neural networks and scikit-learn models."),
    ("Annual 24-Hour Campus Hackathon", "Technology & AI", ["Hackathon", "Web Dev", "Cloud", "Python"], "Build real-world apps overnight, pitch to industry leaders, win prizes."),
    ("Cybersecurity CTF Challenge", "Technology & AI", ["Cybersecurity", "Web Dev"], "Capture the Flag security competition testing penetration testing and cryptography skills."),
    ("Cloud Architecture with AWS & GCP", "Technology & AI", ["Cloud", "Web Dev"], "Master serverless computing, microservices, and containerization."),
    ("Autonomous Robotics Showcase", "Technology & AI", ["Robotics", "Python"], "Live demonstration of student-built autonomous drones and rovers."),
    ("Intro to Deep Learning & PyTorch", "Technology & AI", ["Machine Learning", "Data Science"], "Foundational session exploring backpropagation and vision transformers."),
    ("Fall Tech Career & Internship Fair", "Career & Networking", ["Internship Fair", "Resume Workshop", "Finance"], "Connect directly with recruiters from top tech companies and startups."),
    ("Alumni Founder Fireside Chat", "Career & Networking", ["Startup Pitch", "Alumni Talk", "Leadership"], "Listen to alumni founders share their journey from dorm room to Series A."),
    ("Sunrise Mindfulness & Vinyasa Yoga", "Sports & Wellness", ["Yoga", "Mental Health"], "Calm breathing exercises and energizing yoga flow to de-stress before midterms."),
    ("Ethics of Artificial General Intelligence", "Academic & Research", ["Ethics in Tech", "Machine Learning"], "Interdisciplinary panel analyzing societal impacts of autonomous systems.")
]

def generate_events(num_events=20):
    events = []
    base_date = datetime.now()
    locations = ["Auditorium Hall A", "Innovation Lab 302", "Student Activity Center", "Amphitheater", "Main Lawn"]
    for i in range(num_events):
        title, cat, tags, desc = EVENT_TEMPLATES[i % len(EVENT_TEMPLATES)]
        day_offset = random.randint(-2, 14)
        evt_time = (base_date + timedelta(days=day_offset, hours=random.randint(10, 18))).replace(minute=0, second=0)
        events.append({
            "event_id": f"EVT_{100 + i}",
            "title": title,
            "category": cat,
            "tags": ", ".join(tags),
            "description": desc,
            "datetime": evt_time.strftime("%Y-%m-%d %H:%M"),
            "location": random.choice(locations),
            "capacity": random.choice([50, 100, 200]),
            "popularity": round(random.uniform(3.5, 5.0), 1)
        })
    return events

def generate_students(num_students=30):
    students = [{
        "student_id": "STU_1001",
        "name": "Adarsh S (Project Author)",
        "major": "Computer Science & AI",
        "year": "3rd Year",
        "interests": "Python, Machine Learning, Hackathon, Data Science, Robotics",
        "preferred_categories": "Technology & AI, Academic & Research"
    }]
    majors = ["Computer Science", "Data Science", "Business Administration", "Mechanical Engineering"]
    for i in range(1, num_students):
        students.append({
            "student_id": f"STU_{1001 + i}",
            "name": f"Student {i+1}",
            "major": random.choice(majors),
            "year": "2nd Year",
            "interests": "Python, Web Dev, Hackathon",
            "preferred_categories": "Technology & AI"
        })
    return students

def generate_interactions(students, events):
    records = []
    for s in students:
        for e in events:
            attended = 1 if random.random() < 0.25 else 0
            records.append({
                "student_id": s["student_id"],
                "event_id": e["event_id"],
                "attended": attended,
                "rating": random.choice([3, 4, 5]) if attended else 0
            })
    return records
print("data_generator.py created!")
```

---

### Cell 3: Launch Streamlit & Get Your Public URL
```python
# Download recommender.py and app.py if needed, or launch directly:
import subprocess, time, re

# Launch streamlit in background
subprocess.Popen(["streamlit", "run", "app.py", "--server.port", "8501", "--server.headless", "true", "--server.enableCORS", "false", "--server.enableXsrfProtection", "false"])
time.sleep(3)

# Launch Cloudflare tunnel
p = subprocess.Popen(["./cloudflared", "tunnel", "--url", "http://localhost:8501"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)

print("Waiting for Cloudflare Tunnel URL...")
for line in p.stdout:
    if "trycloudflare.com" in line:
        match = re.search(r"https://[a-zA-Z0-9-]+\.trycloudflare\.com", line)
        if match:
            print("\n" + "="*60)
            print("🚀 YOUR LIVE STREAMLIT APP IN GOOGLE COLAB IS READY:")
            print(match.group(0))
            print("="*60 + "\n")
            break
```

---

## 🎯 What Happens Next?
When you run Cell 3, Google Colab will print a live link ending in `*.trycloudflare.com`.  
Click it, and your full **Campus Event Recommendation Engine** with **Adarsh S** on the front page will open right in your browser!
