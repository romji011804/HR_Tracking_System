"""
Main Application Window
Refactored with sidebar navigation and modular pages
"""
import sys
import os
from qt_compat import QtCore, QtGui, QtWidgets, qapplication_exec, QT_API
from database import Database
from components.sidebar import Sidebar
from pages.dashboard import DashboardPage
from pages.add_record import AddRecordPage
from pages.records_page import ViewRecordsPage
from utils.theme_manager import get_theme_manager

try:
    import qdarkstyle
    from qdarkstyle.light.palette import LightPalette
    from qdarkstyle.dark.palette import DarkPalette
except Exception:
    qdarkstyle = None
    LightPalette = None
    DarkPalette = None

class MainWindow(QtWidgets.QMainWindow):
    """Main application window with sidebar and pages"""
    
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.current_page = None
        self.theme_manager = get_theme_manager()
        
        # Window metadata
        self.setWindowTitle("MOA & Legal Opinion Tracking System")
        self.setGeometry(50, 50, 1400, 800)

        # Ensure the window itself also uses the app icon
        base_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(base_dir, "assets", "app_icon.png")
        if os.path.exists(icon_path):
            self.setWindowIcon(QtGui.QIcon(icon_path))
        
        # Create central widget
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QtWidgets.QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.dashboard_clicked.connect(self.show_dashboard)
        self.sidebar.add_record_clicked.connect(self.show_add_record)
        self.sidebar.view_records_clicked.connect(self.show_view_records)
        
        main_layout.addWidget(self.sidebar)
        
        # Page container
        self.page_container = QtWidgets.QWidget()
        self.page_layout = QtWidgets.QHBoxLayout(self.page_container)
        self.page_layout.setContentsMargins(0, 0, 0, 0)
        self.page_layout.setSpacing(0)
        
        main_layout.addWidget(self.page_container, 1)
        
        # Create pages
        self.dashboard_page = DashboardPage(self.db)
        self.add_record_page = AddRecordPage(self.db)
        self.view_records_page = ViewRecordsPage(self.db)
        
        # Connect signals
        self.add_record_page.record_added.connect(self.on_record_added)
        self.dashboard_page.view_records_requested.connect(self.show_view_records)

        # React to theme changes
        self.theme_manager.theme_changed.connect(self.apply_theme)
        
        # Apply initial theme and show dashboard by default
        self.apply_theme(self.theme_manager.get_theme())
        self.show_dashboard()
    
    def show_page(self, page: QtWidgets.QWidget):
        """Show a page in the container"""
        # Remove current page
        if self.current_page:
            self.page_layout.removeWidget(self.current_page)
            self.current_page.hide()
        
        # Add new page
        self.page_layout.addWidget(page)
        page.show()
        self.current_page = page
    
    def show_dashboard(self):
        """Show dashboard page"""
        self.sidebar.set_active_button(self.sidebar.dashboard_btn)
        self.dashboard_page.load_statistics()
        self.show_page(self.dashboard_page)
    
    def show_add_record(self):
        """Show add record page"""
        self.sidebar.set_active_button(self.sidebar.add_record_btn)
        self.show_page(self.add_record_page)
    
    def show_view_records(self):
        """Show view records page"""
        self.sidebar.set_active_button(self.sidebar.view_records_btn)
        self.view_records_page.load_records()
        self.show_page(self.view_records_page)
    
    def on_record_added(self, record_id: int):
        """Handle record addition"""
        self.dashboard_page.load_statistics()
        self.view_records_page.load_records()

    def apply_theme(self, theme: str):
        """Apply light/dark theme stylesheets across the app"""
        # Prefer QDarkStyle (modern, consistent widgets) if installed
        if qdarkstyle is not None and LightPalette is not None and DarkPalette is not None:
            palette = LightPalette() if theme == "light" else DarkPalette()
            base = qdarkstyle.load_stylesheet(qt_api=QT_API, palette=palette)
            # Remove checkbox/indicator decorations from dropdown lists (combobox popup)
            override = """
                QComboBox QAbstractItemView::indicator,
                QComboBox QListView::indicator {
                    image: none;
                    border: none;
                    background: transparent;
                    width: 0px;
                    height: 0px;
                    margin: 0px;
                    padding: 0px;
                }
                QComboBox QAbstractItemView::indicator:checked,
                QComboBox QAbstractItemView::indicator:unchecked,
                QComboBox QListView::indicator:checked,
                QComboBox QListView::indicator:unchecked {
                    image: none;
                    border: none;
                    background: transparent;
                    width: 0px;
                    height: 0px;
                    margin: 0px;
                    padding: 0px;
                }
                QComboBox QAbstractItemView::item,
                QComboBox QListView::item {
                    padding-left: 0px;
                    margin-left: 0px;
                }
            """
            QtWidgets.QApplication.instance().setStyleSheet(base + override)
            return

        # Fallback to built-in stylesheet bundle
        tm = self.theme_manager
        app_stylesheet = "".join([
            tm.get_stylesheet("main"),
            tm.get_stylesheet("page"),
            tm.get_stylesheet("sidebar"),
            tm.get_stylesheet("button"),
            tm.get_stylesheet("input"),
            tm.get_stylesheet("table"),
            tm.get_stylesheet("label"),
        ])
        QtWidgets.QApplication.instance().setStyleSheet(app_stylesheet)

def main():
    """Main application entry point"""
    app = QtWidgets.QApplication(sys.argv)
    
    # Apply style
    app.setStyle('Fusion')

    # Set application icon
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QtGui.QIcon(icon_path))

    window = MainWindow()
    window.show()
    
    sys.exit(qapplication_exec(app))

if __name__ == '__main__':
    main()
