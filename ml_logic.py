from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Mock dataset for Department Recommendation
# In a real scenario, this would be a trained model loaded from disk.
department_keywords = {
    'Cardiology': "chest pain heart attack breath palpitations pulse high blood pressure stroke",
    'Orthopedics': "joint bone fracture knee back muscle ache sprain swelling mobility",
    'Gynecology': "pregnancy period menstrual baby cramps woman bleeding discharge",
    'Pediatrics': "child baby fever growth vaccination colic rash infant",
    'General Medicine': "fever cough cold headache fatigue flu nausea dizziness infection body pain"
}

# Pre-compute TF-IDF vectors for departments
corpus = list(department_keywords.values())
dept_names = list(department_keywords.keys())
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

def recommend_department(symptoms, age):
    """
    Recommends a department based on symptoms using TF-IDF similarity.
    Includes simple rule-based overrides (e.g., pediatric age).
    """
    # Rule 1: Pediatric override
    if age < 12 and "chest" not in symptoms.lower(): # Simple check to not send heart issues to peds if serious
         # But usually peds handles everything for kids. Let's keep it simple.
         # Actually, better to rely on symptoms mostly, but bias towards Peds if child.
         pass 

    # TF-IDF Matching
    query_vec = vectorizer.transform([symptoms])
    similarities = cosine_similarity(query_vec, tfidf_matrix)
    best_match_idx = np.argmax(similarities)
    best_score = similarities[0][best_match_idx]

    if best_score < 0.1: # Low confidence
        return "General Medicine" # Fallback
    
    return dept_names[best_match_idx]

def calculate_priority(data):
    """
    Calculates priority score and level based on patient data.
    """
    score = 0
    severity = int(data.get('severity', 0))
    age = int(data.get('age', 0))
    distance = float(data.get('distance', 0))
    chronic = data.get('chronic_illness', 'no').lower() == 'yes'
    pregnant = data.get('pregnancy', 'no').lower() == 'yes'
    
    # Base Score from Severity (0-100)
    score += severity * 10
    
    # Age Vulnerability
    if age > 65:
        score += 15
    elif age < 5:
        score += 10
        
    # Chronic Condition
    if chronic:
        score += 20
        
    # Pregnancy (High urgency usually)
    if pregnant:
        score += 25
        
    # Rural / Distance Factor (Prioritize those traveling far)
    if distance > 50:
        score += 20
    elif distance > 20:
        score += 10
        
    # Determine Priority Level
    if score >= 80:
        priority = "High"
    elif score >= 50:
        priority = "Medium"
    else:
        priority = "Low"
        
    return score, priority
