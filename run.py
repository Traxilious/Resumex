import os
import sys
import webbrowser
from app import app

if __name__ == '__main__':
    print("=" * 65)
    print("  ResumeX - Smart Resume Scoring & ATS Feedback Platform")
    print("=" * 65)
    print("[1/3] Initializing local database & pre-seeding job roles...")
    print("[2/3] Application ready! Opening web browser at http://127.0.0.1:5000...")
    print("[3/3] Starting Flask application server on host 0.0.0.0:5000...")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
