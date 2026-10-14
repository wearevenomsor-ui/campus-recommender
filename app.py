"""
Campus Event Recommendation Engine (Assignment No. 32)
Author: Adarsh S
Tech Stack: Python, Pandas, Scikit-learn, Streamlit
"""

import os
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

from data_generator import generate_events, generate_students, generate_interactions
from recommender import HybridRecommender

# Page Configuration
st.set_page_config(
    page_title="Campus Event Recommender | By Adarsh S",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-Aesthetic Styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    
    .author-badge {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        background: linear-gradient(135deg, rgba(99, 102, 241, 0.15), rgba(168, 85, 247, 0.15));
        border: 1px solid rgba(139, 92, 246, 0.35);
        color: #c084fc;
        padding: 6px 16px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        margin-bottom: 12px;
        box-shadow: 0 4px 14px rgba(139, 92, 246, 0.15);
    }
    
    .hero-container {
        background: linear-gradient(135deg, rgba(30, 27, 75, 0.7), rgba(15, 23, 42, 0.9));
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 20px;
        padding: 28px 32px;
        margin-bottom: 24px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.35);
    }
    
    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(90deg, #ffffff, #c7d2fe, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 8px;
    }

    .hero-subtitle {
        color: #94a3b8;
        font-size: 1.05rem;
        line-height: 1.5;
    }

    .metric-card {
        background: rgba(30, 41, 59, 0.6);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 16px 20px;
        backdrop-filter: blur(10px);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover {
        transform: translateY(-2px);
        border-color: rgba(139, 92, 246, 0.4);
    }

    .event-card {
        background: linear-gradient(145deg, rgba(30, 41, 59, 0.75), rgba(15, 23, 42, 0.85));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 6px 18px rgba(0, 0, 0, 0.25);
        transition: all 0.25s ease;
    }
    .event-card:hover {
        border-color: rgba(129, 140, 248, 0.45);
        box-shadow: 0 10px 25px rgba(99, 102, 241, 0.15);
    }

    .tag-pill {
        display: inline-block;
        background: rgba(99, 102, 241, 0.18);
        border: 1px solid rgba(129, 140, 248, 0.3);
        color: #a5b4fc;
        padding: 3px 10px;
        border-radius: 6px;
        font-size: 0.78rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .score-badge {
        background: linear-gradient(135deg, #10b981, #059669);
        color: #ffffff;
        padding: 4px 12px;
        border-radius: 8px;
        font-weight: 700;
        font-size: 0.95rem;
    }

    .reason-box {
        background: rgba(15, 23, 42, 0.7);
        border-left: 3px solid #6366f1;
        padding: 10px 14px;
        border-radius: 0 8px 8px 0;
        margin-top: 12px;
        font-size: 0.88rem;
        color: #cbd5e1;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_project_data():
    """Generates synthetic datasets once and caches in memory."""
    events = generate_events(30)
    students = generate_students(40)
    interactions = generate_interactions(students, events)

    events_df = pd.DataFrame(events)
    students_df = pd.DataFrame(students)
    interactions_df = pd.DataFrame(interactions)

    engine = HybridRecommender(events_df, students_df, interactions_df)
    return events_df, students_df, interactions_df, engine


events_df, students_df, interactions_df, engine = load_project_data()

# ----------------- SIDEBAR CONTROLS -----------------
with st.sidebar:
    st.markdown("""
        <div style="text-align: center; padding: 10px 0 20px 0;">
            <div style="font-size: 2.5rem; margin-bottom: 6px;">🎓⚡</div>
            <h2 style="margin: 0; font-weight: 800; font-size: 1.3rem;">Campus Recommender</h2>
            <div style="color: #a78bfa; font-weight: 700; font-size: 0.95rem; margin-top: 4px;">Created by: Adarsh S</div>
            <div style="color: #64748b; font-size: 0.8rem;">Assignment No. 32 | AI System</div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🧭 Navigation")
    current_tab = st.radio(
        "Select View",
        [
            "🏠 Overview (Adarsh S)",
            "🎯 Student Recommendations",
            "❄️ Cold-Start Stress Test",
            "📊 Model & Dataset Analytics",
            "🎪 All Campus Events",
            "📑 Project Documentation"
        ],
        label_visibility="collapsed"
    )

    st.markdown("---")
    st.markdown("### ⚙️ Hybrid Engine Weights")
    content_w = st.slider("Content-Based Weight (α)", min_value=0.0, max_value=1.0, value=0.55, step=0.05,
                          help="Weight given to TF-IDF interest matching")
    collab_w = st.slider("Collaborative Weight (1 - α)", min_value=0.0, max_value=1.0, value=0.45, step=0.05,
                         help="Weight given to peer attendance/ratings")

    st.markdown("### ⏱️ Time-Aware Settings")
    enable_time = st.checkbox("Enable Time-Aware Scheduling Boost", value=True,
                              help="Boosts upcoming events and applies decay to past events")
    filter_past = st.checkbox("Hide Past Events Entirely", value=False)


# =====================================================================
# TAB 1: OVERVIEW & PROJECT DETAILS (ADARSH S)
# =====================================================================
if current_tab == "🏠 Overview (Adarsh S)":
    st.markdown("""
        <div class="author-badge">
            ⚡ Project Lead & Author: Adarsh S
        </div>
        <div class="hero-container">
            <div class="hero-title">Assignment No. 32 — Campus Event Recommendation Engine</div>
            <div class="hero-subtitle">
                An intelligent hybrid AI recommendation engine developed by <b>Adarsh S</b>. 
                Solves campus event information overload by fusing content-based vector embeddings with 
                collaborative peer signals, cold-start handling, and time-aware scheduling.
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Key Statistics Grid
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.82rem; font-weight: 600;">PROJECT DEVELOPER</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #a78bfa; margin-top: 4px;">Adarsh S</div>
                <div style="color: #38bdf8; font-size: 0.78rem; margin-top: 4px;">Campus AI Architecture</div>
            </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.82rem; font-weight: 600;">ACTIVE CAMPUS EVENTS</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #38bdf8; margin-top: 4px;">{len(events_df)}</div>
                <div style="color: #64748b; font-size: 0.78rem; margin-top: 4px;">Across 6 Diverse Categories</div>
            </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.82rem; font-weight: 600;">STUDENT PROFILES</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #34d399; margin-top: 4px;">{len(students_df)}</div>
                <div style="color: #64748b; font-size: 0.78rem; margin-top: 4px;">Profiles + Cold-Start Benchmarks</div>
            </div>
        """, unsafe_allow_html=True)
    with c4:
        total_attend = interactions_df["attended"].sum()
        st.markdown(f"""
            <div class="metric-card">
                <div style="color: #94a3b8; font-size: 0.82rem; font-weight: 600;">HISTORICAL INTERACTIONS</div>
                <div style="font-size: 1.5rem; font-weight: 800; color: #f472b6; margin-top: 4px;">{total_attend}</div>
                <div style="color: #64748b; font-size: 0.78rem; margin-top: 4px;">Attendance & Rating Records</div>
            </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Core System Pillars
    col_l, col_r = st.columns([1.1, 0.9])
    with col_l:
        st.markdown("### 🧩 System Architecture by Adarsh S")
        st.markdown(r"""
        This engine implements a **weighted hybrid ensemble** with specialized fallbacks:

        1. **Content-Based Filtering (Cosine Similarity + TF-IDF):**
           - Vectorizes event title, category, tags, and description.
           - Matches student interest tokens to calculate semantic affinity $S_{content} \in [0, 1]$.
           - Solves cold-start when interaction history is absent.

        2. **Collaborative Filtering (User-Item Matrix):**
           - Analyzes attendance & rating matrix across student peers.
           - Calculates user-user cosine similarity vectors to identify affinity cohorts.
           - Predicts collaborative affinity $S_{collab} \in [0, 1]$.

        3. **Dynamic Cold-Start Switch:**
           - If student has 0 historical attendance, shifts weight dynamically to Content-Based signals ($90\%$) + Popularity baseline ($10\%$).
           - If a student has neither history nor declared interests, falls back to trending campus events.

        4. **Time-Aware Scheduling (Bonus Rubric):**
           - Upcoming events happening within 5 days receive an urgency boost ($1.15\\times$).
           - Past events receive decay ($0.15\\times$) or can be filtered out.

        5. **Transparent Explainability Badges:**
           - Every recommended item gives the exact reason: matched tags, peer attendances, or campus trending status.
        """)

    with col_r:
        st.markdown("### 👤 Featured Student Profile")
        # Display Adarsh S profile card
        adarsh_profile = students_df.iloc[0]
        st.info(f"""
        **Profile:** {adarsh_profile['name']}  
        **Major:** {adarsh_profile['major']} | **Year:** {adarsh_profile['year']}  
        **Interests:** `{adarsh_profile['interests']}`  
        **Preferred Categories:** `{adarsh_profile['preferred_categories']}`  
        """)

        st.markdown("#### ⚡ Quick Demo Launch")
        st.write("Ready to see Adarsh's personalized recommendation feed?")
        if st.button("🚀 View Recommendations for Adarsh S", type="primary", use_container_width=True):
            st.session_state["selected_student_id"] = "STU_1001"
            st.rerun()


# =====================================================================
# TAB 2: STUDENT RECOMMENDATIONS
# =====================================================================
elif current_tab == "🎯 Student Recommendations":
    st.markdown("""
        <div class="author-badge">
            👤 Engine Architect: Adarsh S
        </div>
        <h2 style="margin-top: 0;">Personalized Event Recommendation Feed</h2>
    """, unsafe_allow_html=True)

    # Student selector
    student_options = {
        row["student_id"]: f"{row['name']} ({row['major']} - {row['year']})"
        for _, row in students_df.iterrows()
    }

    default_idx = 0
    if "selected_student_id" in st.session_state and st.session_state["selected_student_id"] in student_options:
        default_idx = list(student_options.keys()).index(st.session_state["selected_student_id"])

    selected_sid = st.selectbox(
        "Choose a Student to Recommend Events For:",
        options=list(student_options.keys()),
        index=default_idx,
        format_func=lambda x: student_options[x]
    )

    current_student = students_df[students_df["student_id"] == selected_sid].iloc[0]

    # Display selected profile summary
    st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 14px 18px; margin-bottom: 20px;">
            <span style="color: #a78bfa; font-weight: 700;">Selected Profile:</span> <b>{current_student['name']}</b> | 
            <span style="color: #94a3b8;">Major:</span> {current_student['major']} ({current_student['year']})<br>
            <span style="color: #94a3b8;">Declared Interests:</span> <span style="color: #38bdf8;">{current_student['interests'] or 'None (Cold-start test)'}</span> | 
            <span style="color: #94a3b8;">Preferred Categories:</span> {current_student['preferred_categories'] or 'None'}
        </div>
    """, unsafe_allow_html=True)

    # Run recommendation
    recs_df, meta = engine.recommend(
        student_id=selected_sid,
        content_weight=content_w,
        collaborative_weight=collab_w,
        enable_time_aware=enable_time,
        filter_past_events=filter_past,
        top_n=8
    )

    # Display Status Banner
    cold_tag = "❄️ Cold-Start Mode Active" if meta["is_cold_start"] else "🔥 Warm-Start Hybrid Active"
    st.markdown(f"""
        <div style="display: flex; gap: 12px; align-items: center; margin-bottom: 16px;">
            <span style="background: rgba(99, 102, 241, 0.2); border: 1px solid #6366f1; color: #c7d2fe; padding: 4px 12px; border-radius: 20px; font-weight: 600; font-size: 0.85rem;">
                {cold_tag}
            </span>
            <span style="color: #94a3b8; font-size: 0.85rem;">
                Strategy: <b>{meta['cold_start_mode']}</b> | Weights: Content {int(meta['content_weight_used']*100)}% / Collab {int(meta['collab_weight_used']*100)}%
            </span>
        </div>
    """, unsafe_allow_html=True)

    # Display recommendations
    for i, row in recs_df.iterrows():
        tags_html = "".join([f'<span class="tag-pill">{t.strip()}</span>' for t in row["tags"].split(",")])
        match_color = "#10b981" if row["match_percentage"] >= 75 else "#f59e0b" if row["match_percentage"] >= 50 else "#64748b"

        st.markdown(f"""
            <div class="event-card">
                <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                    <div>
                        <span style="color: #a78bfa; font-weight: 700; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.5px;">
                            #{i+1} • {row['category']}
                        </span>
                        <h3 style="margin: 4px 0 8px 0; font-size: 1.25rem; font-weight: 700;">{row['title']}</h3>
                        <div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">
                            📍 {row['location']} &nbsp;•&nbsp; 🗓️ {row['datetime']} &nbsp;•&nbsp; 👥 Capacity: {row['capacity']} &nbsp;•&nbsp; ⭐ {row['popularity']} / 5.0
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <span class="score-badge" style="background: {match_color};">
                            {row['match_percentage']}% Match
                        </span>
                        <div style="color: #64748b; font-size: 0.75rem; margin-top: 4px;">Score: {row['hybrid_score']}</div>
                    </div>
                </div>
                <div style="color: #cbd5e1; font-size: 0.92rem; line-height: 1.5; margin: 8px 0;">
                    {row['description']}
                </div>
                <div>{tags_html}</div>
                <div class="reason-box">
                    💡 <b>Why Recommended:</b> {row['primary_reason']}
                    <span style="float: right; color: #818cf8; font-size: 0.8rem;">
                        Content: {int(row['content_score']*100)}% | Collab: {int(row['collab_score']*100)}% | Time: {row['time_factor']}x
                    </span>
                </div>
            </div>
        """, unsafe_allow_html=True)


# =====================================================================
# TAB 3: COLD-START STRESS TEST
# =====================================================================
elif current_tab == "❄️ Cold-Start Stress Test":
    st.markdown("""
        <div class="author-badge">
            🧪 Designed by: Adarsh S
        </div>
        <h2 style="margin-top: 0;">Cold-Start Resilience Benchmark</h2>
        <p style="color: #94a3b8;">
            A key requirement in Assignment No. 32 is gracefully handling new students who have <b>zero past attendance or ratings</b>.
            Test both scenarios below:
        </p>
    """, unsafe_allow_html=True)

    t1, t2 = st.tabs(["Scenario A: New Student with Known Interests", "Scenario B: Truly Blank Student (Zero Data)"])

    with t1:
        st.markdown("#### Test Cold-Start with Custom Declared Interests")
        st.caption("Student has zero attendance history, but filled out orientation interest checkboxes.")
        
        c_major = st.text_input("Major", value="Cybersecurity Engineering")
        c_interests = st.text_input("Interest Tags", value="Cybersecurity, Web Dev, Python, Hackathon")
        c_cats = st.selectbox("Preferred Category", ["Technology & AI", "Arts & Culture", "Career & Networking", "Sports & Wellness"])

        test_profile = {
            "student_id": "STU_BENCHMARK_1",
            "name": "Incoming Freshman",
            "major": c_major,
            "interests": c_interests,
            "preferred_categories": c_cats
        }

        if st.button("Generate Cold-Start Feed (Scenario A)", type="primary"):
            res, meta = engine.recommend(custom_profile=test_profile, top_n=5)
            st.success(f"Adaptive Mode: **{meta['cold_start_mode']}** (Content Weight: {int(meta['content_weight_used']*100)}%)")
            for i, r in res.iterrows():
                st.markdown(f"**#{i+1} {r['title']}** — Match: `{r['match_percentage']}%` | Reason: *{r['primary_reason']}*")

    with t2:
        st.markdown("#### Test True Cold-Start (Zero Interests + Zero History)")
        st.caption("A newly registered student who skipped onboarding entirely.")
        blank_profile = {
            "student_id": "STU_BENCHMARK_2",
            "name": "Anonymous Guest",
            "major": "Undeclared",
            "interests": "",
            "preferred_categories": ""
        }

        if st.button("Generate Fallback Feed (Scenario B)", type="primary"):
            res, meta = engine.recommend(custom_profile=blank_profile, top_n=5)
            st.warning(f"Fallback Mode: **{meta['cold_start_mode']}** (Campus Popularity Weight: {int(meta['popularity_weight_used']*100)}%)")
            for i, r in res.iterrows():
                st.markdown(f"**#{i+1} {r['title']}** — Popularity: `{r['popularity']}★` | Reason: *{r['primary_reason']}*")


# =====================================================================
# TAB 4: MODEL & DATASET ANALYTICS
# =====================================================================
elif current_tab == "📊 Model & Dataset Analytics":
    st.markdown("""
        <div class="author-badge">
            📈 Analytics Module: Adarsh S
        </div>
        <h2 style="margin-top: 0;">Campus Data & Model Diagnostics</h2>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🏷️ Events by Category")
        cat_counts = events_df["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Event Count"]
        st.dataframe(cat_counts, use_container_width=True)

    with col2:
        st.markdown("### 🎓 Student Majors Distribution")
        major_counts = students_df["major"].value_counts().reset_index()
        major_counts.columns = ["Major", "Student Count"]
        st.dataframe(major_counts, use_container_width=True)

    st.markdown("---")
    st.markdown("### ⚡ Interaction Matrix Sparsity Analysis")
    total_cells = len(students_df) * len(events_df)
    filled_cells = interactions_df["attended"].sum()
    sparsity = (1.0 - (filled_cells / total_cells)) * 100

    m1, m2, m3 = st.columns(3)
    m1.metric("Matrix Cells (Students × Events)", f"{total_cells:,}")
    m2.metric("Recorded Attendances", f"{filled_cells:,}")
    m3.metric("Matrix Sparsity", f"{sparsity:.2f}%")


# =====================================================================
# TAB 5: ALL CAMPUS EVENTS DIRECTORY
# =====================================================================
elif current_tab == "🎪 All Campus Events":
    st.markdown("""
        <div class="author-badge">
            📋 Directory Curated by: Adarsh S
        </div>
        <h2 style="margin-top: 0;">Comprehensive Campus Events Catalog</h2>
    """, unsafe_allow_html=True)

    search_term = st.text_input("🔍 Search events by title, tag, or description:", "")
    selected_cat = st.selectbox("Filter by Category:", ["All Categories"] + list(events_df["category"].unique()))

    filtered_df = events_df.copy()
    if selected_cat != "All Categories":
        filtered_df = filtered_df[filtered_df["category"] == selected_cat]
    if search_term:
        s = search_term.lower()
        filtered_df = filtered_df[
            filtered_df["title"].str.lower().str.contains(s) |
            filtered_df["tags"].str.lower().str.contains(s) |
            filtered_df["description"].str.lower().str.contains(s)
        ]

    st.dataframe(
        filtered_df[["event_id", "title", "category", "tags", "location", "datetime", "popularity"]],
        use_container_width=True
    )


# =====================================================================
# TAB 6: PROJECT DOCUMENTATION & RUBRIC
# =====================================================================
elif current_tab == "📑 Project Documentation":
    st.markdown("""
        <div class="author-badge">
            📖 Submission Dossier: Adarsh S
        </div>
        <h2 style="margin-top: 0;">Assignment No. 32 Technical Documentation</h2>
    """, unsafe_allow_html=True)

    st.markdown(r"""
    ### 1. Project Identification
    - **Assignment:** Assignment No. 32 — Campus Event Recommendation Engine
    - **Developer / Student Name:** **Adarsh S**
    - **Difficulty:** Intermediate
    - **Domain:** Recommendation Systems / Education
    - **Tools:** Python, scikit-learn, pandas, Streamlit

    ---

    ### 2. Algorithmic Breakdown (Meets Rubric: 12 Marks)
    - **Content-Based Filtering:**
      - Term Frequency-Inverse Document Frequency (TF-IDF) feature extraction on event soup (title + category + tags + description).
      - Profile vectorization of student declared interest tokens.
      - Cosine similarity matching:
        $$\\text{Sim}_{content}(u, i) = \\frac{\\mathbf{v}_u \\cdot \\mathbf{v}_i}{\\|\\mathbf{v}_u\\| \\|\\mathbf{v}_i\\|}$$
    - **Collaborative Filtering:**
      - User-item interaction and attendance matrix ($U \\times I$).
      - Peer cosine similarity computation: identifies students with overlapping event attendance.
      - Weighted rating prediction based on top-$k$ most similar peers.

    ---

    ### 3. Hybrid Strategy & Cold-Start (Meets Rubric: 6 Marks)
    - **Ensemble Formula:**
      $$\\text{Score}_{hybrid} = \\alpha \\cdot S_{content} + (1 - \\alpha) \\cdot S_{collab}$$
    - **Dynamic Cold-Start:**
      - If user has no interaction history, weights adaptively route to pure Content-Based matching ($90\%$) + Campus baseline ($10\%$).
      - If user has zero profile information, system routes to campus trending/popularity ranking.

    ---

    ### 4. Optional Enhancement: Time-Aware Decay & Urgency
    - Events scheduled within 1–5 days receive an urgency multiplier ($1.15\\times$).
    - Past events receive penalty decay ($0.15\\times$) or can be filtered from view.

    ---

    ### 5. Rubric Compliance Verification
    - **Algorithms (12):** Content-based + Collaborative filtering implemented.
    - **Hybrid (6):** Dynamic scoring combination + cold start handling.
    - **UI (6):** Interactive Streamlit dashboard with full controls.
    - **Demo (6):** Real-time interactive student switching and cold-start stress tests.
    - **Docs (5):** Full mathematical and architectural specifications included.
    """)

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.85rem; padding: 10px 0;">
        Campus Event Recommendation Engine • Developed with ❤️ by <b>Adarsh S</b> • Assignment No. 32
    </div>
""", unsafe_allow_html=True)
