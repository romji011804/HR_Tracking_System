"""
Sidebar Navigation Component
Reusable sidebar with navigation buttons and theme toggle
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPushButton, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QIcon
from utils.theme_manager import get_theme_manager

class Sidebar(QWidget):
    """Sidebar navigation component"""
    
    # Signals
    dashboard_clicked = pyqtSignal()
    add_record_clicked = pyqtSignal()
    view_records_clicked = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.theme_manager = get_theme_manager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize sidebar UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(0)
        
        # Title
        title = QLabel("MOA & LO\nTracking System")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("color: #1a1a1a; margin-bottom: 30px;")
        layout.addWidget(title)
        
        # Platform Navigation Label
        nav_label = QLabel("Platform Navigation")
        nav_font = QFont()
        nav_font.setPointSize(9)
        nav_font.setBold(True)
        nav_label.setFont(nav_font)
        nav_label.setStyleSheet("color: #666666; margin-bottom: 15px; margin-left: 10px;")
        layout.addWidget(nav_label)
        
        # Navigation Buttons
        self.dashboard_btn = self.create_nav_button("🏠 Dashboard")
        self.add_record_btn = self.create_nav_button("➕ Add Records")
        self.view_records_btn = self.create_nav_button("📊 View Records")
        
        self.dashboard_btn.clicked.connect(self.on_dashboard_clicked)
        self.add_record_btn.clicked.connect(self.on_add_record_clicked)
        self.view_records_btn.clicked.connect(self.on_view_records_clicked)
        
        layout.addWidget(self.dashboard_btn)
        layout.addWidget(self.add_record_btn)
        layout.addWidget(self.view_records_btn)
        
        layout.addStretch()
        
        # Light/Dark Mode Toggle
        mode_layout = QVBoxLayout()
        mode_layout.setSpacing(10)
        
        self.light_btn = QPushButton("☀️ Light Mode")
        self.dark_btn = QPushButton("🌙 Dark Mode")
        
        self.light_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 11px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        self.dark_btn.setStyleSheet("""
            QPushButton {
                background-color: white;
                border: 1px solid #ddd;
                border-radius: 4px;
                padding: 8px;
                font-size: 11px;
                color: #333;
            }
            QPushButton:hover {
                background-color: #f5f5f5;
            }
        """)
        
        self.light_btn.clicked.connect(lambda: self.set_theme('light'))
        self.dark_btn.clicked.connect(lambda: self.set_theme('dark'))
        
        mode_layout.addWidget(self.light_btn)
        mode_layout.addWidget(self.dark_btn)
        
        layout.addLayout(mode_layout)
        
        self.setLayout(layout)
        self.setStyleSheet("""
            Sidebar {
                background-color: #f0f0f0;
                border-right: 1px solid #ddd;
            }
        """)
        self.setFixedWidth(215)
    
    def create_nav_button(self, text: str) -> QPushButton:
        """Create a navigation button"""
        btn = QPushButton(text)
        btn.setFixedHeight(45)
        btn.setStyleSheet("""
            QPushButton {
                background-color: transparent;
                border: none;
                border-left: 4px solid transparent;
                padding-left: 15px;
                text-align: left;
                font-size: 13px;
                color: #333;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                border-left: 4px solid #007acc;
            }
        """)
        return btn
    
    def set_active_button(self, button: QPushButton):
        """Set active button styling"""
        # Reset all buttons
        for btn in [self.dashboard_btn, self.add_record_btn, self.view_records_btn]:
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    border-left: 4px solid transparent;
                    padding-left: 15px;
                    text-align: left;
                    font-size: 13px;
                    color: #333;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #e8e8e8;
                    border-left: 4px solid #007acc;
                }
            """)
        
        # Set active button
        button.setStyleSheet("""
            QPushButton {
                background-color: #e8e8e8;
                border: none;
                border-left: 4px solid #007acc;
                padding-left: 15px;
                text-align: left;
                font-size: 13px;
                color: #007acc;
                font-weight: 600;
            }
            QPushButton:hover {
                background-color: #e8e8e8;
                border-left: 4px solid #007acc;
            }
        """)
    
    def set_theme(self, theme: str):
        """Set application theme"""
        self.theme_manager.set_theme(theme)
        
        # Update theme button appearance
        if theme == 'light':
            self.light_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6366f1;
                    border: 1px solid #6366f1;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            self.dark_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
            """)
        else:  # dark
            self.dark_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6366f1;
                    border: 1px solid #6366f1;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11px;
                    color: white;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            self.light_btn.setStyleSheet("""
                QPushButton {
                    background-color: white;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 8px;
                    font-size: 11px;
                    color: #333;
                }
                QPushButton:hover {
                    background-color: #f5f5f5;
                }
            """)
    
    def on_dashboard_clicked(self):
        """Handle dashboard click"""
        self.set_active_button(self.dashboard_btn)
        self.dashboard_clicked.emit()
    
    def on_add_record_clicked(self):
        """Handle add record click"""
        self.set_active_button(self.add_record_btn)
        self.add_record_clicked.emit()
    
    def on_view_records_clicked(self):
        """Handle view records click"""
        self.set_active_button(self.view_records_btn)
        self.view_records_clicked.emit()
