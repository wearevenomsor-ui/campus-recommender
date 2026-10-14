"""
Data Generator for Campus Event Recommendation Engine
Assignment No. 32
Author: Adarsh S
"""

import random
from datetime import datetime, timedelta
import numpy as np

# Seed for reproducibility
random.seed(42)
np.random.seed(42)

CATEGORIES = [
    "Technology & AI",
    "Career & Networking",
    "Arts & Culture",
    "Sports & Wellness",
    "Academic & Research",
    "Social & Entertainment"
]

TAGS_POOL = {
    "Technology & AI": ["Python", "Machine Learning", "Web Dev", "Cybersecurity", "Hackathon", "Cloud", "Robotics", "Data Science"],
    "Career & Networking": ["Resume Workshop", "Internship Fair", "Alumni Talk", "Startup Pitch", "Interview Prep", "Finance", "Leadership"],
    "Arts & Culture": ["Film Screening", "Live Music", "Theater", "Photography", "Pottery", "Debate Club", "Poetry Slam"],
    "Sports & Wellness": ["Yoga", "Football Tournament", "Basketball League", "Mental Health", "Marathon", "Badminton", "Chess"],
    "Academic & Research": ["Physics Seminar", "Biology Symposium", "Math Olympiad", "Paper Writing", "Ethics in Tech", "Quantum Computing"],
    "Social & Entertainment": ["Trivia Night", "Gaming Lan Party", "Food Fest", "Campus Carnival", "Karaoke Night", "Comedy Club"]
}

EVENT_TEMPLATES = [
    # Technology & AI
    ("AI & Machine Learning Bootcamp", "Technology & AI", ["Python", "Machine Learning", "Data Science"], "Hands-on crash course on neural networks and scikit-learn models."),
    ("Annual 24-Hour Campus Hackathon", "Technology & AI", ["Hackathon", "Web Dev", "Cloud", "Python"], "Build real-world apps overnight, pitch to industry leaders, win prizes."),
    ("Cybersecurity CTF Challenge", "Technology & AI", ["Cybersecurity", "Web Dev"], "Capture the Flag security competition testing penetration testing and cryptography skills."),
    ("Cloud Architecture with AWS & GCP", "Technology & AI", ["Cloud", "Web Dev"], "Master serverless computing, microservices, and containerization."),
    ("Autonomous Robotics Showcase", "Technology & AI", ["Robotics", "Python"], "Live demonstration of student-built autonomous drones and rovers."),
    ("Intro to Deep Learning & PyTorch", "Technology & AI", ["Machine Learning", "Data Science"], "Foundational session exploring backpropagation and vision transformers."),

    # Career & Networking
    ("Fall Tech Career & Internship Fair", "Career & Networking", ["Internship Fair", "Resume Workshop", "Finance"], "Connect directly with recruiters from top tech companies and startups."),
    ("Alumni Founder Fireside Chat", "Career & Networking", ["Startup Pitch", "Alumni Talk", "Leadership"], "Listen to alumni founders share their journey from dorm room to Series A."),
    ("Ace the Technical & Behavioral Interview", "Career & Networking", ["Interview Prep", "Resume Workshop"], "Mock interview drills, behavioral framework breakdowns, and live Q&A."),
    ("Venture Capital & Startup Pitch Slam", "Career & Networking", ["Startup Pitch", "Finance", "Leadership"], "Pitch your student startup to seed investors for grant funding."),
    ("Resume Review & LinkedIn Clinic", "Career & Networking", ["Resume Workshop", "Interview Prep"], "One-on-one portfolio critiques with career advisors and industry mentors."),

    # Arts & Culture
    ("Independent Student Film Festival", "Arts & Culture", ["Film Screening", "Photography"], "Screening of short indie films produced by university filmmakers."),
    ("Acoustic Sunset Jam Session", "Arts & Culture", ["Live Music"], "Open mic acoustic performances under the campus amphitheater."),
    ("Campus Drama Guild: Spring Production", "Arts & Culture", ["Theater"], "Annual theatrical stage performance by the student drama society."),
    ("Urban Photography Photo-Walk", "Arts & Culture", ["Photography"], "Guided photo-walk exploring urban architecture and campus landscapes."),
    ("Inter-College Parliamentary Debate", "Arts & Culture", ["Debate Club"], "Heated debates on global economics, policy, and digital privacy."),
    ("Spoken Word & Poetry Night", "Arts & Culture", ["Poetry Slam"], "Expressive storytelling and spoken word poetry in an intimate cafe setting."),

    # Sports & Wellness
    ("Sunrise Mindfulness & Vinyasa Yoga", "Sports & Wellness", ["Yoga", "Mental Health"], "Calm breathing exercises and energizing yoga flow to de-stress before midterms."),
    ("Intramural 5v5 Basketball Championship", "Sports & Wellness", ["Basketball League"], "High-stakes inter-department basketball tournament."),
    ("Campus 5K Charity Fun Run", "Sports & Wellness", ["Marathon", "Mental Health"], "Run or walk for wellness, supporting student mental health initiatives."),
    ("Blitz Chess Rapid Tournament", "Sports & Wellness", ["Chess"], "5-minute blitz chess tournament with rated tournament rules."),
    ("Campus Badminton Smash Open", "Sports & Wellness", ["Badminton"], "Fast-paced singles and doubles badminton showdown."),

    # Academic & Research
    ("Frontiers of Quantum Computing Seminar", "Academic & Research", ["Quantum Computing", "Physics Seminar"], "Guest lecture from leading quantum researchers on qubit entanglement."),
    ("Bioengineering & CRISPR Horizons", "Academic & Research", ["Biology Symposium"], "Exploration of modern gene editing technologies and ethical boundaries."),
    ("Writing & Publishing High-Impact Papers", "Academic & Research", ["Paper Writing", "Ethics in Tech"], "Proven strategies for drafting IEEE/ACM format research submissions."),
    ("Ethics of Artificial General Intelligence", "Academic & Research", ["Ethics in Tech", "Machine Learning"], "Interdisciplinary panel analyzing societal impacts of autonomous systems."),

    # Social & Entertainment
    ("Inter-Dorm Geek Trivia Battle", "Social & Entertainment", ["Trivia Night", "Gaming Lan Party"], "Test your knowledge on pop culture, sci-fi, gaming, and history."),
    ("All-Night Esports LAN Tournament", "Social & Entertainment", ["Gaming Lan Party"], "Compete in Valorant, Smash Bros, and Rocket League for the campus cup."),
    ("Campus Food Truck Carnival", "Social & Entertainment", ["Food Fest"], "Over 15 local food trucks, live DJ, games, and outdoor seating."),
    ("Stand-Up Comedy Spotlight", "Social & Entertainment", ["Comedy Club"], "Student and guest stand-up comedians bringing non-stop laughs."),
    ("Open Stage Karaoke Extravaganza", "Social & Entertainment", ["Karaoke Night", "Live Music"], "Sing your heart out on the grand student union stage.")
]

MAJORS = [
    "Computer Science", "Electrical Engineering", "Data Science", 
    "Business Administration", "Mechanical Engineering", "Biotechnology", 
    "Psychology", "Fine Arts", "Economics"
]

FIRST_NAMES = ["Aarav", "Priya", "Rohan", "Ananya", "Dev", "Isha", "Rahul", "Neha", "Kabir", "Meera", "Vikram", "Sneha", "Karan", "Tanvi", "Aditya", "Rhea", "Arjun", "Kavya", "Siddharth", "Pooja"]
LAST_NAMES = ["Sharma", "Verma", "Patel", "Nair", "Iyer", "Reddy", "Gupta", "Rao", "Menon", "Joshi", "Singh", "Kumar", "Das", "Chopra", "Bose"]

def generate_events(num_events=30):
    events = []
    base_date = datetime.now()
    
    locations = [
        "Auditorium Hall A", "Innovation Lab 302", "Student Activity Center",
        "Amphitheater", "Sports Complex Court 1", "Engineering Block B-10",
        "Library Quiet Hall", "Main Campus Lawn", "Tech Hub Seminar Room"
    ]
    
    for i in range(num_events):
        template = EVENT_TEMPLATES[i % len(EVENT_TEMPLATES)]
        title, category, tags, desc = template
        
        if i >= len(EVENT_TEMPLATES):
            title = f"{title} (Session {i // len(EVENT_TEMPLATES) + 1})"
        
        day_offset = random.randint(-5, 20)
        event_time = (base_date + timedelta(days=day_offset, hours=random.randint(9, 19))).replace(minute=0, second=0, microsecond=0)
        
        events.append({
            "event_id": f"EVT_{100 + i}",
            "title": title,
            "category": category,
            "tags": ", ".join(tags),
            "description": desc,
            "datetime": event_time.strftime("%Y-%m-%d %H:%M"),
            "location": random.choice(locations),
            "capacity": random.choice([50, 100, 150, 250, 400]),
            "popularity": round(random.uniform(3.0, 5.0), 1)
        })
        
    return events

def generate_students(num_students=45):
    students = []
    
    # Adarsh S (Project Author) as the showcase student
    students.append({
        "student_id": "STU_1001",
        "name": "Adarsh S (Project Author)",
        "major": "Computer Science & AI",
        "year": "3rd Year",
        "interests": "Python, Machine Learning, Hackathon, Data Science, Robotics",
        "preferred_categories": "Technology & AI, Academic & Research"
    })
    
    for i in range(1, num_students):
        fname = random.choice(FIRST_NAMES)
        lname = random.choice(LAST_NAMES)
        major = random.choice(MAJORS)
        year = random.choice(["1st Year", "2nd Year", "3rd Year", "4th Year", "Graduate"])
        
        prefs = random.sample(CATEGORIES, k=random.choice([1, 2]))
        
        chosen_tags = []
        for cat in prefs:
            chosen_tags.extend(random.sample(TAGS_POOL[cat], k=min(2, len(TAGS_POOL[cat]))))
        
        if random.random() < 0.3:
            wild_cat = random.choice(CATEGORIES)
            chosen_tags.append(random.choice(TAGS_POOL[wild_cat]))
            
        chosen_tags = list(set(chosen_tags))
        
        students.append({
            "student_id": f"STU_{1001 + i}",
            "name": f"{fname} {lname}",
            "major": major,
            "year": year,
            "interests": ", ".join(chosen_tags),
            "preferred_categories": ", ".join(prefs)
        })
        
    students.append({
        "student_id": "STU_COLD_1",
        "name": "Newbie Fresher (Cold-Start with Interests)",
        "major": "Data Science",
        "year": "1st Year",
        "interests": "Web Dev, Cloud, Cybersecurity",
        "preferred_categories": "Technology & AI"
    })
    students.append({
        "student_id": "STU_COLD_2",
        "name": "Zero-Profile Student (True Cold-Start)",
        "major": "Undeclared",
        "year": "1st Year",
        "interests": "",
        "preferred_categories": ""
    })
    
    return students

def generate_interactions(students, events):
    records = []
    
    for stu in students:
        sid = stu["student_id"]
        
        if "COLD" in sid:
            for evt in events:
                records.append({
                    "student_id": sid,
                    "event_id": evt["event_id"],
                    "attended": 0,
                    "rating": 0
                })
            continue
            
        stu_interests = [t.strip().lower() for t in stu["interests"].split(",") if t.strip()]
        stu_cats = [c.strip().lower() for c in stu["preferred_categories"].split(",") if c.strip()]
        
        for evt in events:
            eid = evt["event_id"]
            evt_tags = [t.strip().lower() for t in evt["tags"].split(",") if t.strip()]
            evt_cat = evt["category"].lower()
            
            match_tags = len(set(stu_interests).intersection(set(evt_tags)))
            match_cat = 1 if evt_cat in stu_cats else 0
            
            p_attend = 0.08
            if match_cat:
                p_attend += 0.25
            if match_tags > 0:
                p_attend += 0.35 * min(match_tags, 2)
                
            p_attend = min(p_attend, 0.85)
            attended = 1 if random.random() < p_attend else 0
            
            if attended:
                if match_tags or match_cat:
                    rating = random.choices([3, 4, 5], weights=[0.2, 0.4, 0.4])[0]
                else:
                    rating = random.choices([1, 2, 3, 4], weights=[0.2, 0.3, 0.3, 0.2])[0]
            else:
                rating = 0
                
            records.append({
                "student_id": sid,
                "event_id": eid,
                "attended": attended,
                "rating": rating
            })
            
    return records
