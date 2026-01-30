# MediFlow - Telemedicine Queue Optimizer

A modern, ML-powered patient prioritization system designed for efficient clinical decision support.

## Features
- **Smart Patient Prioritization**: Uses Rule-based ML scoring to prioritize patients by urgency (Severity, Age, Pregnancy, Distance).
- **Department Recommendation**: Suggests the correct department (Cardiology, Orthopedics, etc.) based on symptoms using TF-IDF matching.
- **Unified Admin Dashboard**:
    - **Real-time Overview** of hospital load.
    - **Priority Queue** view with visual badges.
    - **Analytics** with Chart.js visualizations.
- **Modern UI**:
    - Mobile-first, responsive design.
    - Professional Teal/Blue medical theme.
    - Sidebar navigation with collapsible menu.

## Tech Stack
- **Backend**: Python (Flask)
- **Database**: SQLite
- **Front-end**: HTML5, CSS3 (Variables, Flexbox/Grid), JavaScript
- **ML**: scikit-learn (TF-IDF), Rule-based logic

## Setup & Run

1.  **Install Requirements**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Initialize Database**
    (Happens automatically on first run, or run manually)
    ```bash
    python database.py
    ```

3.  **Start Application**
    ```bash
    python app.py
    ```

4.  **Access App**
    - Open `http://127.0.0.1:5000` in your browser.
    - **Patient View**: Home page (No login required).
    - **Admin View**: Click "Admin Login" in sidebar.

## Credentials
- **Admin**: `admin@gmail.com`
- **Password**: `admin`
