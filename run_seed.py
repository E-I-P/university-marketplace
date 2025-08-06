import sys
import os

# Add the parent directory to the Python path so we can import from app.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from seed_db import seed_database

if __name__ == '__main__':
    seed_database()