"""
Sidebar Navigation Component
Reusable sidebar with navigation buttons and theme toggle
"""
from qt_compat import QtCore, QtGui, QtWidgets, Signal
from utils.theme_manager import get_theme_manager

class Sidebar(QtWidgets.QWidget):
    """Sidebar navigation component"""
    
    # Signals
    dashboard_clicked = Signal()
    add_record_clicked = Signal()
    view_records_clicked = Signal()
    
    def __init__(self):
        super().__init__()
        self.theme_manager = get_theme_manager()
        self.init_ui()
    
    def init_ui(self):
        """Initialize sidebar UI"""
        self.setObjectName("Sidebar")
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 20, 0, 20)
        layout.setSpacing(0)
        
        # Title
        title = QtWidgets.QLabel("MOA & LO\nTracking System")
        title.setObjectName("SidebarTitle")
        title_font = QtGui.QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setContentsMargins(0, 0, 0, 22)
        layout.addWidget(title)
        
        # Platform Navigation Label
        nav_label = QtWidgets.QLabel("Platform Navigation")
        nav_label.setObjectName("SidebarSectionLabel")
        nav_font = QtGui.QFont()
        nav_font.setPointSize(9)
        nav_font.setBold(True)
        nav_label.setFont(nav_font)
        nav_label.setContentsMargins(12, 0, 0, 10)
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
        mode_layout = QtWidgets.QVBoxLayout()
        mode_layout.setSpacing(10)
        
        self.light_btn = QtWidgets.QPushButton("☀️ Light Mode")
        self.dark_btn = QtWidgets.QPushButton("🌙 Dark Mode")
        self.light_btn.setProperty("themeToggle", True)
        self.dark_btn.setProperty("themeToggle", True)
        
        self.light_btn.clicked.connect(lambda: self.set_theme('light'))
        self.dark_btn.clicked.connect(lambda: self.set_theme('dark'))
        
        mode_layout.addWidget(self.light_btn)
        mode_layout.addWidget(self.dark_btn)
        
        layout.addLayout(mode_layout)
        
        self.setLayout(layout)
        self.setFixedWidth(215)
        self._sync_theme_toggle_state()
    
    def create_nav_button(self, text: str) -> QtWidgets.QPushButton:
        """Create a navigation button"""
        btn = QtWidgets.QPushButton(text)
        btn.setFixedHeight(45)
        btn.setProperty("nav", True)
        return btn
    
    def set_active_button(self, button: QtWidgets.QPushButton):
        """Set active button styling"""
        for btn in [self.dashboard_btn, self.add_record_btn, self.view_records_btn]:
            btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()

        button.setProperty("active", True)
        button.style().unpolish(button)
        button.style().polish(button)
        button.update()
    
    def set_theme(self, theme: str):
        """Set application theme"""
        self.theme_manager.set_theme(theme)
        self._sync_theme_toggle_state()

    def _sync_theme_toggle_state(self):
        theme = self.theme_manager.get_theme()
        self.light_btn.setProperty("active", theme == "light")
        self.dark_btn.setProperty("active", theme == "dark")
        for btn in (self.light_btn, self.dark_btn):
            btn.style().unpolish(btn)
            btn.style().polish(btn)
            btn.update()
    
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
