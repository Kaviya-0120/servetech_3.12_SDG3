import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class DepartmentRecommender:
    def __init__(self):
        self.departments = {
            'General Medicine': [
                'fever', 'cough', 'cold', 'flu', 'headache', 'fatigue', 'weakness',
                'nausea', 'vomiting', 'diarrhea', 'stomach', 'general', 'tired',
                'sick', 'unwell', 'body ache', 'muscle pain', 'sore throat'
            ],
            'Cardiology': [
                'chest pain', 'heart', 'cardiac', 'palpitation', 'shortness of breath',
                'breathing difficulty', 'chest tightness', 'heart attack', 'angina',
                'blood pressure', 'hypertension', 'heart rate', 'cardiovascular'
            ],
            'Orthopedics': [
                'joint pain', 'bone', 'fracture', 'sprain', 'back pain', 'neck pain',
                'knee pain', 'shoulder pain', 'hip pain', 'arthritis', 'muscle',
                'ligament', 'tendon', 'sports injury', 'mobility', 'walking difficulty'
            ],
            'Gynecology': [
                'pregnancy', 'pregnant', 'menstrual', 'period', 'pelvic pain',
                'vaginal', 'uterine', 'ovarian', 'breast', 'reproductive',
                'gynecological', 'women health', 'contraception', 'fertility'
            ],
            'Pediatrics': [
                'child', 'baby', 'infant', 'toddler', 'pediatric', 'vaccination',
                'growth', 'development', 'feeding', 'crying', 'rash', 'diaper'
            ],
            'Dermatology': [
                'skin', 'rash', 'acne', 'eczema', 'psoriasis', 'mole', 'itching',
                'burning', 'dermatitis', 'allergic reaction', 'hives', 'wound',
                'cut', 'burn', 'bruise', 'skin condition'
            ],
            'Neurology': [
                'headache', 'migraine', 'seizure', 'stroke', 'numbness', 'tingling',
                'paralysis', 'memory loss', 'confusion', 'dizziness', 'vertigo',
                'neurological', 'brain', 'nerve', 'spinal'
            ],
            'Emergency': [
                'emergency', 'urgent', 'severe', 'critical', 'accident', 'trauma',
                'bleeding', 'unconscious', 'difficulty breathing', 'chest pain severe',
                'poisoning', 'overdose', 'suicide', 'violence', 'life threatening'
            ]
        }
        
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)
        self._prepare_department_vectors()
    
    def _prepare_department_vectors(self):
        """Prepare TF-IDF vectors for each department"""
        # Create department documents
        dept_docs = []
        self.dept_names = []
        
        for dept, keywords in self.departments.items():
            dept_doc = ' '.join(keywords)
            dept_docs.append(dept_doc)
            self.dept_names.append(dept)
        
        # Fit vectorizer on department documents
        self.dept_vectors = self.vectorizer.fit_transform(dept_docs)
    
    def recommend_department(self, symptom_text):
        """Recommend department based on symptom text"""
        # Clean and preprocess symptom text
        symptom_text = self._preprocess_text(symptom_text)
        
        # Rule-based matching first (for high confidence cases)
        rule_based_dept = self._rule_based_matching(symptom_text)
        if rule_based_dept:
            return rule_based_dept
        
        # TF-IDF based similarity matching
        symptom_vector = self.vectorizer.transform([symptom_text])
        similarities = cosine_similarity(symptom_vector, self.dept_vectors)[0]
        
        # Get department with highest similarity
        best_dept_idx = np.argmax(similarities)
        best_similarity = similarities[best_dept_idx]
        
        # If similarity is too low, default to General Medicine
        if best_similarity < 0.1:
            return 'General Medicine'
        
        return self.dept_names[best_dept_idx]
    
    def _preprocess_text(self, text):
        """Clean and preprocess symptom text"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters but keep spaces
        text = re.sub(r'[^a-zA-Z\s]', ' ', text)
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        return text
    
    def _rule_based_matching(self, symptom_text):
        """Rule-based department matching for high-confidence cases"""
        symptom_lower = symptom_text.lower()
        
        # Emergency keywords (highest priority)
        emergency_keywords = [
            'emergency', 'urgent', 'severe chest pain', 'can\'t breathe',
            'unconscious', 'bleeding heavily', 'overdose', 'suicide',
            'accident', 'trauma', 'life threatening'
        ]
        
        for keyword in emergency_keywords:
            if keyword in symptom_lower:
                return 'Emergency'
        
        # Pregnancy-related (high priority)
        if any(word in symptom_lower for word in ['pregnant', 'pregnancy', 'labor', 'contractions']):
            return 'Gynecology'
        
        # Age-specific (pediatrics)
        if any(word in symptom_lower for word in ['baby', 'infant', 'child', 'toddler']):
            return 'Pediatrics'
        
        # Specific conditions
        if 'chest pain' in symptom_lower or 'heart' in symptom_lower:
            return 'Cardiology'
        
        if any(word in symptom_lower for word in ['joint pain', 'back pain', 'fracture', 'sprain']):
            return 'Orthopedics'
        
        if any(word in symptom_lower for word in ['skin', 'rash', 'acne', 'eczema']):
            return 'Dermatology'
        
        if any(word in symptom_lower for word in ['headache', 'migraine', 'seizure', 'stroke']):
            return 'Neurology'
        
        return None  # No rule-based match found
    
    def get_department_keywords(self, department):
        """Get keywords for a specific department"""
        return self.departments.get(department, [])
    
    def get_all_departments(self):
        """Get list of all available departments"""
        return list(self.departments.keys())