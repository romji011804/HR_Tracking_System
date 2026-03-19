"""
PDF Viewer Dialog Component
For viewing PDF files within the application
"""
from qt_compat import QtCore, QtGui, QtWidgets, load_qurl, load_web_engine_view

Qt = QtCore.Qt
QUrl = load_qurl()
HAS_WEB_ENGINE, _QWebEngineView = load_web_engine_view()

class PDFViewer(QtWidgets.QDialog):
    """Dialog for viewing PDF files"""
    
    def __init__(self, file_path: str, title: str = "PDF Viewer", parent=None):
        super().__init__(parent)
        self.file_path = file_path
        self.init_ui(title)
        self.load_pdf()
    
    def init_ui(self, title: str):
        """Initialize PDF viewer UI"""
        self.setWindowTitle(title)
        self.setGeometry(100, 100, 900, 700)
        
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Toolbar
        toolbar = QtWidgets.QHBoxLayout()
        toolbar.setContentsMargins(10, 10, 10, 10)
        
        title_label = QtWidgets.QLabel(title)
        title_font = QtGui.QFont()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title_label.setFont(title_font)
        toolbar.addWidget(title_label)
        toolbar.addStretch()
        
        close_btn = QtWidgets.QPushButton("Close")
        close_btn.setFixedWidth(100)
        close_btn.clicked.connect(self.close)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 8px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        toolbar.addWidget(close_btn)
        
        layout.addLayout(toolbar)
        
        # PDF Viewer
        if HAS_WEB_ENGINE:
            self.viewer = _QWebEngineView()
            layout.addWidget(self.viewer)
        else:
            # Fallback message
            fallback_label = QtWidgets.QLabel(
                "PDF Web Engine not available.\n"
                "Install Qt WebEngine support for your Qt binding.\n\n"
                "Alternatively, install and use system PDF viewer."
            )
            fallback_label.setAlignment(Qt.AlignCenter)
            layout.addWidget(fallback_label)
        
        self.setLayout(layout)
    
    def load_pdf(self):
        """Load PDF file"""
        if HAS_WEB_ENGINE:
            try:
                pdf_url = QUrl.fromLocalFile(self.file_path)
                self.viewer.load(pdf_url)
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to load PDF: {str(e)}")
        else:
            # Fall back to system viewer
            import os
            try:
                import subprocess
                import platform
                
                if platform.system() == 'Windows':
                    os.startfile(self.file_path)
                elif platform.system() == 'Darwin':
                    subprocess.Popen(['open', self.file_path])
                else:
                    subprocess.Popen(['xdg-open', self.file_path])
                
                self.close()
            except Exception as e:
                QtWidgets.QMessageBox.warning(self, "Error", f"Failed to open PDF: {str(e)}")
