"""
Campus Event Hybrid Recommendation Engine
Assignment No. 32
Author: Adarsh S

Implements:
1. Content-Based Filtering (TF-IDF + Cosine Similarity)
2. Collaborative Filtering (User-Item Matrix Factorization & Cosine Similarity)
3. Hybrid Ensemble with Adaptive Cold-Start Resolution
4. Time-Aware Scheduling Boost & Decay
5. Explainability Reason Engine
"""

from datetime import datetime
import numpy as np
import pandas as pd


class ContentBasedRecommender:
    """
    Computes event similarity based on event text features (tags, category, description)
    and student declared interest profiles.
    """
    def __init__(self, events_df):
        self.events_df = events_df.copy()
        self._prepare_event_features()

    def _prepare_event_features(self):
        # Create a rich text corpus per event
        self.events_df["content_soup"] = (
            self.events_df["title"] + " " +
            self.events_df["category"] + " " +
            self.events_df["tags"] + " " +
            self.events_df["description"]
        ).str.lower()
        
        # Build vocabulary and term frequencies (offline, pure python / scikit-learn compatible)
        self.vocabulary = set()
        for soup in self.events_df["content_soup"]:
            for word in self._tokenize(soup):
                self.vocabulary.add(word)
        self.vocab_list = sorted(list(self.vocabulary))
        self.vocab_idx = {w: i for i, w in enumerate(self.vocab_list)}

        # Vectorize events using TF-IDF
        self.event_vectors = np.zeros((len(self.events_df), len(self.vocab_list)))
        doc_count = len(self.events_df)
        df_counts = np.zeros(len(self.vocab_list))

        tokenized_docs = [self._tokenize(soup) for soup in self.events_df["content_soup"]]
        for tokens in tokenized_docs:
            seen = set(tokens)
            for w in seen:
                if w in self.vocab_idx:
                    df_counts[self.vocab_idx[w]] += 1

        idf = np.log((doc_count + 1) / (df_counts + 1)) + 1.0

        for row_idx, tokens in enumerate(tokenized_docs):
            t_counts = {}
            for w in tokens:
                t_counts[w] = t_counts.get(w, 0) + 1
            for w, cnt in t_counts.items():
                if w in self.vocab_idx:
                    col_idx = self.vocab_idx[w]
                    tf = cnt / len(tokens)
                    self.event_vectors[row_idx, col_idx] = tf * idf[col_idx]

        # L2 Normalize
        norms = np.linalg.norm(self.event_vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1e-9
        self.event_vectors = self.event_vectors / norms
        self.idf = idf

    def _tokenize(self, text):
        import re
        words = re.findall(r"\b[a-zA-Z]{2,}\b", text.lower())
        stopwords = {
            "the", "and", "for", "with", "from", "this", "that", "over", "into",
            "your", "out", "annual", "hands", "real", "guest", "test"
        }
        return [w for w in words if w not in stopwords]

    def predict(self, student_profile):
        """
        Calculates content similarity score [0.0, 1.0] for every event.
        """
        # Vectorize student profile
        interests_text = (
            student_profile.get("interests", "") + " " +
            student_profile.get("preferred_categories", "") + " " +
            student_profile.get("major", "")
        ).lower()
        
        tokens = self._tokenize(interests_text)
        if not tokens:
            # Completely blank profile
            return np.zeros(len(self.events_df)), {}

        stu_vec = np.zeros(len(self.vocab_list))
        t_counts = {}
        for w in tokens:
            t_counts[w] = t_counts.get(w, 0) + 1

        for w, cnt in t_counts.items():
            if w in self.vocab_idx:
                col_idx = self.vocab_idx[w]
                tf = cnt / len(tokens)
                stu_vec[col_idx] = tf * self.idf[col_idx]

        norm = np.linalg.norm(stu_vec)
        if norm > 0:
            stu_vec = stu_vec / norm

        # Cosine similarity
        sim_scores = np.dot(self.event_vectors, stu_vec)
        # Clip to [0, 1]
        sim_scores = np.clip(sim_scores, 0.0, 1.0)

        # Generate matched keywords for explainability
        matched_tags_map = {}
        stu_token_set = set(tokens)
        for idx, row in self.events_df.iterrows():
            evt_tags = [t.strip().lower() for t in row["tags"].split(",")]
            evt_cat = row["category"].lower()
            
            matched = [t for t in evt_tags if any(tok in t for tok in stu_token_set)]
            if evt_cat in interests_text:
                matched.append(row["category"])
            matched_tags_map[row["event_id"]] = list(set(matched))

        return sim_scores, matched_tags_map


class CollaborativeRecommender:
    """
    Computes user-item collaborative filtering scores using user similarity
    and historical attendance/ratings.
    """
    def __init__(self, interactions_df, students_df, events_df):
        self.interactions_df = interactions_df.copy()
        self.students_df = students_df.copy()
        self.events_df = events_df.copy()
        self._build_interaction_matrix()

    def _build_interaction_matrix(self):
        # Pivot table of student_id x event_id with ratings (or attended flag)
        self.rating_matrix = self.interactions_df.pivot(
            index="student_id", columns="event_id", values="rating"
        ).fillna(0)
        
        self.student_ids = list(self.rating_matrix.index)
        self.event_ids = list(self.rating_matrix.columns)
        self.matrix_values = self.rating_matrix.values.astype(float)

        # Precompute user-user cosine similarities
        norms = np.linalg.norm(self.matrix_values, axis=1, keepdims=True)
        norms[norms == 0] = 1e-9
        normed_matrix = self.matrix_values / norms
        self.user_similarity = np.dot(normed_matrix, normed_matrix.T)

    def predict(self, student_id):
        """
        Returns collaborative scores for all events for the given student.
        Handles cold-start: if student not found or has 0 ratings, returns is_cold_start=True.
        """
        event_count = len(self.events_df)
        event_id_to_idx = {eid: idx for idx, eid in enumerate(self.events_df["event_id"])}
        collab_scores = np.zeros(event_count)
        peer_reasons = {}

        if student_id not in self.rating_matrix.index:
            return collab_scores, peer_reasons, True

        user_idx = self.rating_matrix.index.get_loc(student_id)
        user_ratings = self.matrix_values[user_idx]

        # Check if user has zero ratings (cold-start)
        if np.sum(user_ratings) == 0:
            return collab_scores, peer_reasons, True

        # Find top k most similar peers (excluding self)
        similarities = self.user_similarity[user_idx].copy()
        similarities[user_idx] = -1.0
        top_peer_indices = np.argsort(similarities)[::-1][:7]

        # Calculate weighted average predicted rating
        sim_weights = similarities[top_peer_indices]
        sim_weights[sim_weights < 0] = 0
        total_weight = np.sum(sim_weights)

        if total_weight > 0:
            peer_ratings = self.matrix_values[top_peer_indices] # shape (k, num_events)
            predicted_ratings = np.dot(sim_weights, peer_ratings) / total_weight
            
            # Map back to events_df order and normalize to [0, 1] (max rating is 5.0)
            for matrix_col_idx, eid in enumerate(self.event_ids):
                if eid in event_id_to_idx:
                    evt_idx = event_id_to_idx[eid]
                    norm_score = predicted_ratings[matrix_col_idx] / 5.0
                    collab_scores[evt_idx] = np.clip(norm_score, 0.0, 1.0)
                    
                    # Peers attended count
                    attendees = np.sum(peer_ratings[:, matrix_col_idx] > 0)
                    if attendees > 0:
                        peer_reasons[eid] = f"{int(attendees)} peer(s) with similar campus taste attended/rated this"
                    else:
                        peer_reasons[eid] = "Based on campus collaborative pattern"

        return collab_scores, peer_reasons, False


class HybridRecommender:
    """
    Combines Content-Based and Collaborative Filtering signals with:
    - Adaptive Cold-Start Resolution
    - Time-Aware Scheduling Boost & Decay
    - Natural Language Explainability Badges
    """
    def __init__(self, events_df, students_df, interactions_df):
        self.events_df = events_df.copy()
        self.students_df = students_df.copy()
        self.interactions_df = interactions_df.copy()

        self.content_engine = ContentBasedRecommender(self.events_df)
        self.collab_engine = CollaborativeRecommender(self.interactions_df, self.students_df, self.events_df)

    def calculate_time_factor(self, event_datetime_str):
        """
        Optional Enhancement: Time-Aware Recommendations
        - Past events: heavily down-weighted (0.15)
        - Imminent events (next 1-5 days): boost factor (1.15)
        - Future events (6-15 days): standard factor (1.0)
        - Far future (>15 days): slight decay (0.90)
        """
        try:
            event_dt = datetime.strptime(event_datetime_str, "%Y-%m-%d %H:%M")
            now = datetime.now()
            diff_days = (event_dt - now).total_seconds() / 86400.0

            if diff_days < 0:
                # Event already passed
                return 0.15, "Past event"
            elif diff_days <= 5:
                # Coming up this week!
                return 1.15, "Happening soon (Next 5 days!)"
            elif diff_days <= 14:
                return 1.0, "Scheduled in next 2 weeks"
            else:
                return 0.85, "Later this month"
        except Exception:
            return 1.0, "Date pending"

    def recommend(
        self,
        student_id=None,
        custom_profile=None,
        content_weight=0.5,
        collaborative_weight=0.5,
        enable_time_aware=True,
        filter_past_events=False,
        top_n=10
    ):
        """
        Generates top-N hybrid recommendations with explanation metadata.
        """
        # Determine student profile
        if custom_profile is not None:
            student_profile = custom_profile
            sid = custom_profile.get("student_id", "STU_CUSTOM")
        else:
            matching = self.students_df[self.students_df["student_id"] == student_id]
            if not matching.empty:
                student_profile = matching.iloc[0].to_dict()
                sid = student_id
            else:
                student_profile = {
                    "student_id": "STU_UNKNOWN",
                    "name": "Guest Student",
                    "major": "General",
                    "interests": "",
                    "preferred_categories": ""
                }
                sid = "STU_UNKNOWN"

        # 1. Content-based scores
        content_scores, matched_tags_map = self.content_engine.predict(student_profile)

        # 2. Collaborative scores
        collab_scores, peer_reasons, is_cold_start = self.collab_engine.predict(sid)

        # 3. Dynamic Cold-Start Adaptation
        if is_cold_start:
            # Check if student has declared interests
            has_interests = bool(student_profile.get("interests", "").strip() or student_profile.get("preferred_categories", "").strip())
            
            if has_interests:
                effective_content_w = 0.90
                effective_collab_w = 0.0
                popularity_w = 0.10
                cold_start_mode = "Cold-Start: Content-Preference Prioritized"
            else:
                # True cold-start (zero history + zero profile)
                effective_content_w = 0.20
                effective_collab_w = 0.0
                popularity_w = 0.80
                cold_start_mode = "True Cold-Start: Campus Popularity Fallback"
        else:
            # Normalize user-selected weights
            total_w = content_weight + collaborative_weight
            if total_w == 0:
                content_weight, collaborative_weight = 0.5, 0.5
                total_w = 1.0
            effective_content_w = content_weight / total_w
            effective_collab_w = collaborative_weight / total_w
            popularity_w = 0.0
            cold_start_mode = "Warm-Start: Full Hybrid Integration"

        # Normalize event popularity ratings (scale 3.0-5.0 -> 0.0-1.0)
        pop_scores = (self.events_df["popularity"] - 3.0) / 2.0
        pop_scores = np.clip(pop_scores.values, 0.0, 1.0)

        # 4. Composite Hybrid Score
        hybrid_base = (
            effective_content_w * content_scores +
            effective_collab_w * collab_scores +
            popularity_w * pop_scores
        )

        results = []
        for idx, row in self.events_df.iterrows():
            eid = row["event_id"]
            c_score = float(content_scores[idx])
            cf_score = float(collab_scores[idx])
            pop_score = float(pop_scores[idx])
            base_score = float(hybrid_base[idx])

            # Apply Time-Aware Enhancement
            time_factor, time_label = self.calculate_time_factor(row["datetime"])
            if enable_time_aware:
                final_score = base_score * time_factor
            else:
                final_score = base_score

            # Check if past event filter applies
            if filter_past_events and time_factor == 0.15:
                continue

            # Generate natural language explanation
            reasons = []
            matched_tags = matched_tags_map.get(eid, [])
            if matched_tags:
                reasons.append(f"Matches interests in {', '.join(matched_tags[:3])}")
            
            if not is_cold_start and eid in peer_reasons:
                reasons.append(peer_reasons[eid])
            elif is_cold_start:
                if popularity_w > 0.5:
                    reasons.append(f"Trending on campus with {row['popularity']}★ rating")
                elif matched_tags:
                    reasons.append("Selected from your declared interest tags")

            if enable_time_aware and time_factor > 1.0:
                reasons.append(time_label)

            if not reasons:
                reasons.append(f"Curated for {row['category']}")

            results.append({
                "event_id": eid,
                "title": row["title"],
                "category": row["category"],
                "tags": row["tags"],
                "description": row["description"],
                "datetime": row["datetime"],
                "location": row["location"],
                "capacity": row["capacity"],
                "popularity": row["popularity"],
                "content_score": round(c_score, 3),
                "collab_score": round(cf_score, 3),
                "popularity_score": round(pop_score, 3),
                "hybrid_score": round(float(final_score), 4),
                "match_percentage": int(min(max(final_score * 100, 5), 99)),
                "time_factor": time_factor,
                "time_label": time_label,
                "primary_reason": reasons[0],
                "all_reasons": reasons
            })

        # Rank by hybrid score descending
        results_df = pd.DataFrame(results)
        if not results_df.empty:
            results_df = results_df.sort_values(by="hybrid_score", ascending=False).reset_index(drop=True)

        meta = {
            "student_id": sid,
            "student_name": student_profile.get("name", "Unknown"),
            "major": student_profile.get("major", ""),
            "cold_start_mode": cold_start_mode,
            "is_cold_start": is_cold_start,
            "content_weight_used": round(effective_content_w, 2),
            "collab_weight_used": round(effective_collab_w, 2),
            "popularity_weight_used": round(popularity_w, 2),
            "total_candidates": len(self.events_df)
        }

        return results_df.head(top_n), meta
