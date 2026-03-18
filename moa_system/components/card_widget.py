"""
Card Widget Component
Reusable card widget with rounded corners, shadow, and icon support
"""
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

class CardWidget(QWidget):
    """Reusable card widget for displaying information"""
    
    def __init__(self, title: str = "", value: str = "", icon: str = "", bg_color: str = "#ffffff"):
        super().__init__()
        self.title_text = title
        self.value_text = value
        self.icon_char = icon
        self.bg_color = bg_color
        self.init_ui()
    
    def init_ui(self):
        """Initialize card UI"""
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)
        
        # Icon + Title Layout
        header_layout = QHBoxLayout()
        header_layout.setSpacing(10)
        
        # Icon
        if self.icon_char:
            icon_label = QLabel(self.icon_char)
            icon_font = QFont()
            icon_font.setPointSize(20)
            icon_label.setFont(icon_font)
            icon_label.setStyleSheet(f"color: #17a2b8;")
            header_layout.addWidget(icon_label)
        
        # Title
        title_label = QLabel(self.title_text)
        title_font = QFont()
        title_font.setPointSize(11)
        title_font.setWeight(QFont.Normal)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #666666;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        layout.addLayout(header_layout)
        
        # Value
        value_label = QLabel(self.value_text)
        value_font = QFont()
        value_font.setPointSize(28)
        value_font.setBold(True)
        value_label.setFont(value_font)
        value_label.setStyleSheet("color: #1a1a1a;")
        layout.addWidget(value_label)
        
        layout.addStretch()
        
        self.setLayout(layout)
        self.set_style()
        self.setMinimumHeight(120)
    
    def set_style(self):
        """Apply card styling with shadow and rounded corners"""
        self.setStyleSheet(f"""
            CardWidget {{
                background-color: {self.bg_color};
                border-radius: 8px;
                border: 1px solid #e8e8e8;
            }}
            CardWidget:hover {{
                border: 1px solid #ddd;
            }}
        """)
    
    def set_value(self, value: str):
        """Update card value"""
        self.value_text = value
        for label in self.findChildren(QLabel):
            if label.font().pointSize() > 20:
                label.setText(value)
                break
