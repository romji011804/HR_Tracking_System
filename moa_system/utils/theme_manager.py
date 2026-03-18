"""
Theme Manager for Light/Dark Mode
Handles application theme switching
"""
from PyQt5.QtCore import QObject, pyqtSignal

class ThemeManager(QObject):
    """Manages application themes (Light/Dark)"""
    
    theme_changed = pyqtSignal(str)  # Emits 'light' or 'dark'
    
    def __init__(self):
        super().__init__()
        self.current_theme = 'light'
    
    def get_theme(self) -> str:
        """Get current theme"""
        return self.current_theme
    
    def set_theme(self, theme: str):
        """Set application theme"""
        if theme in ['light', 'dark']:
            self.current_theme = theme
            self.theme_changed.emit(theme)
    
    def toggle_theme(self):
        """Toggle between light and dark theme"""
        new_theme = 'dark' if self.current_theme == 'light' else 'light'
        self.set_theme(new_theme)
    
    def get_stylesheet(self, component: str = 'main') -> str:
        """Get stylesheet for a component based on current theme"""
        
        if self.current_theme == 'light':
            return self.get_light_stylesheet(component)
        else:
            return self.get_dark_stylesheet(component)
    
    @staticmethod
    def get_light_stylesheet(component: str) -> str:
        """Get light mode stylesheet"""

        # Modern light theme palette (Tailwind-inspired)
        # Background: #f3f4f6, Surface: #ffffff, Border: #e5e7eb
        # Text: #0f172a / #4b5563, Primary: #4f46e5, Accent: #10b981
        styles = {
            'main': """
                QMainWindow {
                    background-color: #f3f4f6;
                }
            """,
            'page': """
                QWidget {
                    background-color: #f3f4f6;
                    color: #0f172a;
                }
            """,
            'sidebar': """
                Sidebar {
                    background-color: #ffffff;
                    border-right: 1px solid #e5e7eb;
                }
            """,
            'button': """
                QPushButton {
                    background-color: #4f46e5;
                    color: #ffffff;
                    border-radius: 6px;
                    padding: 6px 12px;
                    border: none;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #4338ca;
                }
                QPushButton:disabled {
                    background-color: #e5e7eb;
                    color: #9ca3af;
                }
            """,
            'input': """
                QLineEdit, QComboBox, QDateEdit, QSpinBox {
                    background-color: #ffffff;
                    color: #111827;
                    border: 1px solid #e5e7eb;
                    border-radius: 6px;
                    padding: 6px 10px;
                    selection-background-color: #4f46e5;
                    selection-color: #ffffff;
                }
                QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
                    border: 1px solid #4f46e5;
                    background-color: #ffffff;
                }
            """,
            'table': """
                QTableWidget {
                    background-color: #ffffff;
                    alternate-background-color: #f9fafb;
                    gridline-color: #e5e7eb;
                    border-radius: 8px;
                    border: 1px solid #e5e7eb;
                }
                QTableWidget::item {
                    padding: 8px;
                    color: #111827;
                    border-bottom: 1px solid #e5e7eb;
                }
                QHeaderView::section {
                    background-color: #f9fafb;
                    color: #4b5563;
                    padding: 8px;
                    border: none;
                    border-bottom: 1px solid #e5e7eb;
                    font-weight: 600;
                    font-size: 11px;
                }
                QTableWidget::item:selected {
                    background-color: #e0e7ff;
                    color: #111827;
                }
            """,
            'label': """
                QLabel {
                    color: #111827;
                }
            """
        }
        
        return styles.get(component, '')
    
    @staticmethod
    def get_dark_stylesheet(component: str) -> str:
        """Get dark mode stylesheet"""

        # Modern dark theme palette
        # Background: #020617, Surface: #0f172a, Border: #1f2937
        # Text: #e5e7eb, Muted: #9ca3af, Primary: #4f46e5
        styles = {
            'main': """
                QMainWindow {
                    background-color: #020617;
                }
            """,
            'page': """
                QWidget {
                    background-color: #020617;
                    color: #e5e7eb;
                }
                DashboardPage, ViewRecordsPage, AddRecordPage, RecordViewComponent {
                    background-color: #020617;
                    color: #e5e7eb;
                }
            """,
            'sidebar': """
                Sidebar {
                    background-color: #020617;
                    border-right: 1px solid #1f2937;
                }
            """,
            'button': """
                QPushButton {
                    color: #e5e7eb;
                    background-color: #4f46e5;
                    border-radius: 6px;
                    padding: 6px 12px;
                    border: none;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #4338ca;
                }
                QPushButton:disabled {
                    background-color: #1f2937;
                    color: #6b7280;
                }
            """,
            'input': """
                QLineEdit, QComboBox, QDateEdit, QSpinBox {
                    background-color: #020617;
                    color: #e5e7eb;
                    border: 1px solid #1f2937;
                    border-radius: 6px;
                    padding: 6px 10px;
                    selection-background-color: #4f46e5;
                    selection-color: #ffffff;
                }
                QLineEdit:focus, QComboBox:focus, QDateEdit:focus, QSpinBox:focus {
                    border: 1px solid #4f46e5;
                }
            """,
            'table': """
                QTableWidget {
                    background-color: #020617;
                    alternate-background-color: #020617;
                    gridline-color: #1f2937;
                    color: #e5e7eb;
                    border-radius: 8px;
                    border: 1px solid #1f2937;
                }
                QTableWidget::item {
                    padding: 8px;
                    color: #e5e7eb;
                    border-bottom: 1px solid #1f2937;
                }
                QHeaderView::section {
                    background-color: #020617;
                    color: #9ca3af;
                    padding: 8px;
                    border: none;
                    border-bottom: 1px solid #1f2937;
                    font-weight: 600;
                    font-size: 11px;
                }
                QTableWidget::item:selected {
                    background-color: #1d4ed8;
                    color: #e5e7eb;
                }
            """,
            'label': """
                QLabel {
                    color: #e5e7eb;
                }
            """
        }
        
        return styles.get(component, '')


# Global theme manager instance
_theme_manager = None

def get_theme_manager() -> ThemeManager:
    """Get or create the global theme manager"""
    global _theme_manager
    if _theme_manager is None:
        _theme_manager = ThemeManager()
    return _theme_manager
