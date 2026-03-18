"""
Dashboard Window for MOA Tracking System
Displays summary statistics
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
    QLabel, QPushButton, QMessageBox
)
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QBrush
from database import Database
from models import DashboardStats

class StatisticCard(QWidget):
    """Custom widget for displaying statistics"""
    
    def __init__(self, title: str, value: int, color: str = '#3498db'):
        super().__init__()
        self.title = title
        self.value = value
        self.color = color
        self.init_ui()
    
    def init_ui(self):
        """Initialize the card UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)
        
        # Set background color
        self.setStyleSheet(f'''
            StatisticCard {{
                background-color: {self.color};
                border-radius: 8px;
                color: white;
            }}
        ''')
        
        # Title label
        title_label = QLabel(self.title)
        title_font = QFont()
        title_font.setPointSize(10)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        
        # Value label
        value_label = QLabel(str(self.value))
        value_font = QFont()
        value_font.setPointSize(32)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setAlignment(Qt.AlignCenter)
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addStretch()
        
        self.setLayout(layout)
        self.setMinimumHeight(150)

class DashboardWindow(QMainWindow):
    """Dashboard window displaying system statistics"""
    
    refresh_requested = pyqtSignal()
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.setWindowTitle("MOA & LO Tracking System - Dashboard")
        self.setGeometry(100, 100, 1200, 600)
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """Initialize the dashboard UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Dashboard - Statistics")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Statistics grid
        stats_layout = QGridLayout()
        stats_layout.setSpacing(15)
        
        self.total_card = StatisticCard("Total Records", 0, '#3498db')
        self.ongoing_card = StatisticCard("Ongoing Records", 0, '#f39c12')
        self.completed_card = StatisticCard("Completed Records", 0, '#27ae60')
        self.missing_lo_card = StatisticCard("Missing Legal Opinion", 0, '#e67e22')
        self.missing_moa_card = StatisticCard("Missing MOA", 0, '#e74c3c')
        
        stats_layout.addWidget(self.total_card, 0, 0)
        stats_layout.addWidget(self.ongoing_card, 0, 1)
        stats_layout.addWidget(self.completed_card, 0, 2)
        stats_layout.addWidget(self.missing_lo_card, 1, 0)
        stats_layout.addWidget(self.missing_moa_card, 1, 1)
        
        main_layout.addLayout(stats_layout)
        main_layout.addStretch()
        
        # Buttons layout
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_statistics)
        refresh_btn.setFixedWidth(100)
        
        button_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(button_layout)
    
    def load_statistics(self):
        """Load and display statistics from database"""
        try:
            stats_dict = self.db.get_dashboard_stats()
            stats = DashboardStats.from_dict(stats_dict)
            
            self.total_card.value = stats.total_records
            self.update_card_value(self.total_card, stats.total_records)
            
            self.ongoing_card.value = stats.ongoing_records
            self.update_card_value(self.ongoing_card, stats.ongoing_records)
            
            self.completed_card.value = stats.completed_records
            self.update_card_value(self.completed_card, stats.completed_records)
            
            self.missing_lo_card.value = stats.missing_lo
            self.update_card_value(self.missing_lo_card, stats.missing_lo)
            
            self.missing_moa_card.value = stats.missing_moa
            self.update_card_value(self.missing_moa_card, stats.missing_moa)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load statistics: {str(e)}")
    
    @staticmethod
    def update_card_value(card: StatisticCard, value: int):
        """Update card value label"""
        for widget in card.findChildren(QLabel):
            if widget.font().pointSize() > 20:
                widget.setText(str(value))
                break
