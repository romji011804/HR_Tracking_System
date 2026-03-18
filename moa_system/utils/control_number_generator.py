"""
Control Number Generator utility
Generates auto-formatted control numbers for records
"""
from datetime import datetime

def generate_control_number(base_db, year: int = None) -> str:
    """
    Generate next control number in format: MOA-YYYY-###
    
    Args:
        base_db: Database instance
        year: Year for control number (defaults to current year)
    
    Returns:
        str: Next control number
    """
    if year is None:
        year = datetime.now().year
    
    return base_db.get_next_control_number(year)

def validate_control_number(control_number: str) -> bool:
    """
    Validate control number format
    
    Args:
        control_number: Control number to validate
    
    Returns:
        bool: True if valid format
    """
    parts = control_number.split('-')
    if len(parts) != 3:
        return False
    
    if parts[0] != 'MOA':
        return False
    
    try:
        year = int(parts[1])
        sequence = int(parts[2])
        if sequence < 1 or sequence > 999:
            return False
        return True
    except ValueError:
        return False
