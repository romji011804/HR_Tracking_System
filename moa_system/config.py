"""
Configuration settings for MOA & Legal Opinion Tracking System
"""
import os
from pathlib import Path

# Application metadata
APP_NAME = "MOA & Legal Opinion Tracking System"
APP_VERSION = "1.0.0"
ORGANIZATION = "HR Department"

# Paths
BASE_DIR = Path(__file__).parent.absolute()
DATABASE_DIR = BASE_DIR
DATABASE_NAME = "moa_tracking.db"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

UPLOADS_DIR = BASE_DIR / "uploads"
LO_UPLOADS_DIR = UPLOADS_DIR / "lo"
MOA_UPLOADS_DIR = UPLOADS_DIR / "moa"

# Database settings
DB_TIMEOUT = 30.0
DB_CHECK_SAME_THREAD = False

# File upload settings
ALLOWED_FILE_EXTENSIONS = {'.pdf', '.PDF'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50 MB
UPLOAD_CHUNK_SIZE = 1024 * 1024  # 1 MB

# UI Settings
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800
DASHBOARD_WINDOW_WIDTH = 1200
DASHBOARD_WINDOW_HEIGHT = 600
FORM_WINDOW_WIDTH = 900
FORM_WINDOW_HEIGHT = 800
RECORDS_TABLE_WIDTH = 1400
RECORDS_TABLE_HEIGHT = 700

# Color scheme
COLORS = {
    'success': '#27ae60',  # Green
    'warning': '#f39c12',  # Yellow
    'danger': '#e74c3c',   # Red
    'info': '#3498db',      # Blue
    'missing_lo': '#e67e22',  # Orange
    'missing_moa': '#e74c3c', # Red
}

# Workflow stages
WORKFLOW_STAGES = [
    'Received',
    'For Legal Review',
    'Legal Opinion Issued',
    'MOA Preparation',
    'For Signing',
    'Completed'
]

# Record status options
RECORD_STATUS = ['Ongoing', 'Completed']

# Control number settings
CONTROL_NUMBER_PREFIX = 'MOA'
CONTROL_NUMBER_SEQUENCE_LENGTH = 3

# Date format
DATE_FORMAT = 'yyyy-MM-dd'
DISPLAY_DATE_FORMAT = 'MMM dd, yyyy'

# Create necessary directories
os.makedirs(LO_UPLOADS_DIR, exist_ok=True)
os.makedirs(MOA_UPLOADS_DIR, exist_ok=True)
