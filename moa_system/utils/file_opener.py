"""
File and URL Opener Utility
STRICT FILE vs LINK detection
"""
import os
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

# Get the base directory of the application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def open_file(path_or_url: str, show_error_callback=None) -> bool:
    """
    Open a file or URL with STRICT detection logic:
    
    1. If empty → show "No file available"
    2. If file EXISTS on disk → open locally (NOT in browser)
    3. If file does NOT exist → treat as link (open in browser)
    
    Args:
        path_or_url: File path or URL to open
        show_error_callback: Function to show errors f(title, message)
    
    Returns:
        bool: True if successful, False otherwise
    """
    print(f"[DEBUG] Opening: {path_or_url}")
    
    # Step 1: Validate input
    if not path_or_url:
        _show_error("No File Available", "No file or link provided", show_error_callback)
        return False
    
    # Trim whitespace
    path_or_url = str(path_or_url).strip()
    
    # Empty after trim
    if not path_or_url or path_or_url == "No file available":
        _show_error("No File Available", "No file or link available for this record", show_error_callback)
        return False
    
    # Step 2: STRICT detection - check if file exists FIRST
    # If path is relative, try to make it absolute from BASE_DIR
    check_path = path_or_url
    if not os.path.isabs(path_or_url):
        # Try relative to BASE_DIR first (for uploads/)
        check_path = os.path.join(BASE_DIR, path_or_url)
    
    if os.path.exists(check_path):
        print(f"[DEBUG] File exists: {check_path} → Opening locally")
        return _open_local_file(check_path, show_error_callback)
    else:
        # File doesn't exist → treat as link
        print(f"[DEBUG] File not found: {path_or_url} → Treating as link")
        return _open_link(path_or_url, show_error_callback)


def _open_local_file(file_path: str, show_error_callback=None) -> bool:
    """
    Open a local file using ONLY:
    QDesktopServices.openUrl(QUrl.fromLocalFile(path))
    
    This ensures files open in system default apps (PDF reader, etc.)
    NOT in browser
    """
    try:
        # Convert to absolute path
        abs_path = os.path.abspath(file_path)
        
        # Check file still exists
        if not os.path.exists(abs_path):
            _show_error(
                "File Not Found",
                f"File does not exist:\n{abs_path}",
                show_error_callback
            )
            return False
        
        print(f"[DEBUG] Opening file: {abs_path}")
        
        # ONLY use fromLocalFile for local files
        QDesktopServices.openUrl(QUrl.fromLocalFile(abs_path))
        return True
    
    except Exception as e:
        error_msg = f"{str(e)}\n\nFile: {file_path}"
        _show_error("Failed to Open File", error_msg, show_error_callback)
        return False


def _open_link(url: str, show_error_callback=None) -> bool:
    """
    Open a URL/link using:
    QDesktopServices.openUrl(QUrl(link))
    
    Auto-completes https:// if missing
    """
    try:
        url = url.strip()
        
        # Auto-complete https:// if missing protocol
        if not url.startswith('http://') and not url.startswith('https://'):
            url = 'https://' + url
            print(f"[DEBUG] Auto-completed URL: {url}")
        
        print(f"[DEBUG] Opening URL: {url}")
        
        # Open URL in browser
        QDesktopServices.openUrl(QUrl(url))
        return True
    
    except Exception as e:
        error_msg = f"{str(e)}\n\nURL: {url}"
        _show_error("Failed to Open Link", error_msg, show_error_callback)
        return False


def _show_error(title: str, message: str, callback=None):
    """Show error message using callback or fallback to console"""
    if callback:
        callback(title, message)
    else:
        print(f"[ERROR] {title}: {message}")

