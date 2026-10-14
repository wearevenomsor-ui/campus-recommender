# How to Host this Project on Render.com
**Campus Event Recommendation Engine by Adarsh S**

Yes! **Render.com** can host Python and Streamlit apps completely free 24/7 in the cloud without needing your laptop to stay on.

---

## ⚡ The 2-Minute Deployment Steps

### Step 1: Put Your Code on GitHub
1. Go to [github.com](https://github.com/) and create a new repository (e.g. `campus-event-recommender`).
2. Upload these files to your repository:
   - `app.py`
   - `recommender.py`
   - `data_generator.py`
   - `requirements.txt`
   - `render.yaml`
   - `Procfile`

*(Or if you use git terminal):*
```bash
git init
git add .
git commit -m "Campus Recommender by Adarsh S"
git remote add origin https://github.com/<your-username>/campus-event-recommender.git
git push -u origin main
```

---

### Step 2: Connect to Render.com
1. Go to **[render.com](https://render.com/)** and log in (you can click *"Sign in with GitHub"*).
2. Click the **"New +"** button at the top right and select **"Web Service"**.
3. Choose **"Build and deploy from a Git repository"** and connect your GitHub repository.

---

### Step 3: Configure Settings (Render auto-detects most of this):

| Field | Setting to Enter |
| :--- | :--- |
| **Name** | `campus-recommender-adarsh` (or any name you like) |
| **Language** | `Python 3` |
| **Region** | Singapore / Oregon / Frankfurt (closest to you) |
| **Branch** | `main` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false` |
| **Instance Type** | **Free** |

---

### Step 4: Click "Deploy Web Service"
- Render will install `streamlit`, `pandas`, and `scikit-learn`.
- In about 2 minutes, Render will give you your permanent, live 24/7 URL:
  👉 **`https://campus-recommender-adarsh.onrender.com`**

---

## 🎉 Benefits of Render.com:
- **Free 24/7 Hosting:** You can turn your computer off and the link stays alive.
- **Permanent URL:** The link never changes or expires.
- **Automatic SSL/HTTPS:** Secure padlock for everyone who visits.
- **Mobile Friendly:** Works on any smartphone or tablet worldwide.
