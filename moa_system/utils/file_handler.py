"""
File Handler utility
Manages file uploads, storage, and operations
"""
import os
import shutil
from pathlib import Path
from typing import Optional, Tuple

# Base directories for file storage
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPLOADS_DIR = os.path.join(BASE_DIR, 'uploads')
LO_UPLOADS_DIR = os.path.join(UPLOADS_DIR, 'lo')
MOA_UPLOADS_DIR = os.path.join(UPLOADS_DIR, 'moa')

# Create directories if they don't exist
os.makedirs(LO_UPLOADS_DIR, exist_ok=True)
os.makedirs(MOA_UPLOADS_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = {'.pdf'}

class FileHandler:
    """Handle file operations for documents"""
    
    @staticmethod
    def upload_file(source_path: str, file_type: str, control_number: str) -> Optional[str]:
        """
        Upload a file to appropriate directory
        
        Args:
            source_path: Path to source file
            file_type: 'lo' for Legal Opinion or 'moa' for MOA
            control_number: Control number for filename
        
        Returns:
            str: Relative file path if successful, None otherwise
        """
        if not os.path.exists(source_path):
            print(f"Source file not found: {source_path}")
            return None
        
        # Validate file extension
        file_ext = os.path.splitext(source_path)[1].lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            print(f"Invalid file type: {file_ext}")
            return None
        
        # Determine destination directory
        if file_type.lower() == 'lo':
            dest_dir = LO_UPLOADS_DIR
            folder = 'lo'
        elif file_type.lower() == 'moa':
            dest_dir = MOA_UPLOADS_DIR
            folder = 'moa'
        else:
            print(f"Invalid file type: {file_type}")
            return None
        
        # Create filename: CTRL_NUMBER_TYPE.pdf
        filename = f"{control_number}_{file_type.upper()}.pdf"
        dest_path = os.path.join(dest_dir, filename)
        
        try:
            shutil.copy2(source_path, dest_path)
            # Return relative path for database storage
            return f"uploads/{folder}/{filename}"
        except Exception as e:
            print(f"Error uploading file: {e}")
            return None
    
    @staticmethod
    def get_file_path(relative_path: str) -> Optional[str]:
        """
        Get absolute path from relative path
        
        Args:
            relative_path: Relative path stored in database
        
        Returns:
            str: Absolute file path if exists, None otherwise
        """
        if not relative_path:
            return None
        
        abs_path = os.path.join(BASE_DIR, relative_path)
        if os.path.exists(abs_path):
            return abs_path
        return None
    
    @staticmethod
    def delete_file(relative_path: str) -> bool:
        """
        Delete a file
        
        Args:
            relative_path: Relative path stored in database
        
        Returns:
            bool: True if successful
        """
        if not relative_path:
            return False
        
        abs_path = FileHandler.get_file_path(relative_path)
        if abs_path and os.path.exists(abs_path):
            try:
                os.remove(abs_path)
                return True
            except Exception as e:
                print(f"Error deleting file: {e}")
                return False
        return False
    
    @staticmethod
    def file_exists(relative_path: str) -> bool:
        """
        Check if file exists
        
        Args:
            relative_path: Relative path stored in database
        
        Returns:
            bool: True if file exists
        """
        return FileHandler.get_file_path(relative_path) is not None
    
    @staticmethod
    def open_file(relative_path: str) -> bool:
        """
        Open file with default application
        
        Args:
            relative_path: Relative path stored in database
        
        Returns:
            bool: True if successful
        """
        abs_path = FileHandler.get_file_path(relative_path)
        if abs_path:
            try:
                import subprocess
                import platform
                
                if platform.system() == 'Windows':
                    os.startfile(abs_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.Popen(['open', abs_path])
                else:  # Linux and others
                    subprocess.Popen(['xdg-open', abs_path])
                return True
            except Exception as e:
                print(f"Error opening file: {e}")
                return False
        return False
