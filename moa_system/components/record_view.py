"""
Record View Component
Displays detailed view of a single record in a card-based layout
"""
from qt_compat import QtCore, QtGui, QtWidgets, Signal
import os
from database import Database
from models import Record
from utils.file_handler import FileHandler
from utils.file_opener import open_file  # Renamed from open_file_or_url
from ui.edit_record import EditRecordWindow

class RecordViewComponent(QtWidgets.QWidget):
    """Component for viewing a single record with detailed information"""
    
    back_clicked = Signal()
    record_updated = Signal(int)  # Emitted when record is updated
    
    def __init__(self, record_id: int, db: Database, parent=None, *, show_back: bool = True):
        super().__init__(parent)
        self.record_id = record_id
        self.db = db
        self.file_handler = FileHandler()
        self.record = None
        self.show_back = show_back
        self.init_ui()
        self.load_record()
    
    def init_ui(self):
        """Initialize record view UI"""
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header with back button
        header_layout = QtWidgets.QHBoxLayout()
        
        self.title_label = QtWidgets.QLabel()
        title_font = QtGui.QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        self.title_label.setFont(title_font)
        self.title_label.setStyleSheet("color: #1a1a1a;")
        
        header_layout.addWidget(self.title_label)
        header_layout.addStretch()
        
        if self.show_back:
            back_btn = QtWidgets.QPushButton("← Back")
            back_btn.setFixedWidth(100)
            back_btn.setFixedHeight(35)
            back_btn.clicked.connect(self.back_clicked.emit)
            back_btn.setStyleSheet("""
                QPushButton {
                    background-color: #6366f1;
                    color: white;
                    border: none;
                    border-radius: 5px;
                    font-weight: 500;
                }
                QPushButton:hover {
                    background-color: #4f46e5;
                }
            """)
            header_layout.addWidget(back_btn)
        
        main_layout.addLayout(header_layout)
        
        # Scroll area for content
        scroll = QtWidgets.QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
        """)
        
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(15)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Fields container
        self.fields_layout = QtWidgets.QVBoxLayout()
        self.fields_layout.setSpacing(12)
        content_layout.addLayout(self.fields_layout)
        content_layout.addStretch()
        
        scroll.setWidget(content_widget)
        main_layout.addWidget(scroll)
        
        # Action buttons
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        self.edit_btn = QtWidgets.QPushButton("✏️ Edit Record")
        self.edit_btn.setFixedWidth(140)
        self.edit_btn.setFixedHeight(40)
        self.edit_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: 500;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.edit_btn.clicked.connect(self.on_edit_clicked)
        button_layout.addWidget(self.edit_btn)
        
        self.delete_btn = QtWidgets.QPushButton("🗑️ Delete Record")
        self.delete_btn.setFixedWidth(140)
        self.delete_btn.setFixedHeight(40)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #ef4444;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: 500;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #dc2626;
            }
        """)
        self.delete_btn.clicked.connect(self.on_delete_clicked)
        button_layout.addWidget(self.delete_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        self.setStyleSheet("""
            RecordViewComponent {
                background-color: #f5f5f5;
            }
        """)
    
    def load_record(self):
        """Load record from database"""
        try:
            record_dict = self.db.get_record(self.record_id)
            if record_dict:
                self.record = Record.from_dict(record_dict)
                self.display_record()
            else:
                QtWidgets.QMessageBox.warning(self, "Error", "Record not found")
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load record: {e}")
    
    def display_record(self):
        """Display record fields"""
        if not self.record:
            return
        
        # Clear previous fields
        while self.fields_layout.count():
            child = self.fields_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
        
        # Update title
        self.title_label.setText(f"{self.record.control_number}")
        
        # Field definitions - mark clickable fields
        fields = [
            ("Building", "🏫", self.record.school_name, False),
            ("Course", "📖", self.record.course, False),
            ("Hours", "⏱️", str(self.record.number_of_hours), False),
            ("Date Received", "📅", self.record.date_received, False),
            ("Status", "✓", self.record.status, False),
            ("Workflow", "→", self.record.workflow_stage, False),
            ("Memorandum of Agreement", "📄", self.record.moa_file or "No file available", True),
            ("Legal Opinion", "📜", self.record.lo_file or "No file available", True),
        ]
        
        for label_text, icon, value, is_clickable in fields:
            if is_clickable:
                field_widget = self.create_clickable_field_widget(label_text, icon, value)
            else:
                field_widget = self.create_field_widget(label_text, icon, value)
            self.fields_layout.addWidget(field_widget)
    
    def create_field_widget(self, label: str, icon: str, value: str) -> QtWidgets.QWidget:
        """Create a field display widget"""
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)
        
        # Icon and label
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        icon_label.setFixedWidth(30)
        layout.addWidget(icon_label)
        
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(3)
        
        label_widget = QtWidgets.QLabel(label)
        label_font = QtGui.QFont()
        label_font.setPointSize(9)
        label_widget.setFont(label_font)
        label_widget.setStyleSheet("color: #666666; font-weight: 500;")
        text_layout.addWidget(label_widget)
        
        value_widget = QtWidgets.QLabel(value)
        value_font = QtGui.QFont()
        value_font.setPointSize(11)
        value_widget.setFont(value_font)
        value_widget.setStyleSheet("color: #1a1a1a; font-weight: 500;")
        value_widget.setWordWrap(True)
        text_layout.addWidget(value_widget)
        
        layout.addLayout(text_layout, 1)
        
        # Style container
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
            }
        """)
        
        return container
    
    def create_clickable_field_widget(self, label: str, icon: str, value: str) -> QtWidgets.QWidget:
        """Create a clickable field widget (for MOA and LO)"""
        # Check if value is available
        is_available = value and value != "No file available"
        
        container = QtWidgets.QWidget()
        layout = QtWidgets.QHBoxLayout(container)
        layout.setContentsMargins(15, 12, 15, 12)
        layout.setSpacing(10)
        
        # Icon and label
        icon_label = QtWidgets.QLabel(icon)
        icon_label.setStyleSheet("font-size: 16px;")
        icon_label.setFixedWidth(30)
        layout.addWidget(icon_label)
        
        text_layout = QtWidgets.QVBoxLayout()
        text_layout.setSpacing(3)
        
        label_widget = QtWidgets.QLabel(label)
        label_font = QtGui.QFont()
        label_font.setPointSize(9)
        label_widget.setFont(label_font)
        label_widget.setStyleSheet("color: #666666; font-weight: 500;")
        text_layout.addWidget(label_widget)
        
        # Create clickable value widget
        value_widget = QtWidgets.QLabel(value)
        value_font = QtGui.QFont()
        value_font.setPointSize(11)
        value_font.setUnderline(True)  # Underline to show it's clickable
        value_widget.setFont(value_font)
        value_widget.setWordWrap(True)
        
        # Style based on availability
        if is_available:
            # Clickable style
            value_widget.setStyleSheet(f"""
                QLabel {{
                    color: #6366f1;
                    font-weight: 500;
                    text-decoration: underline;
                }}
            """)
            value_widget.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
            
            # Make it clickable
            value_widget.mousePressEvent = lambda event: self.on_file_click(value, label)
        else:
            # Disabled style
            value_widget.setStyleSheet("""
                QLabel {
                    color: #999999;
                    font-weight: 400;
                }
            """)
            # Not clickable, leave cursor as default
        
        text_layout.addWidget(value_widget)
        layout.addLayout(text_layout, 1)
        
        # Style container
        if is_available:
            container.setStyleSheet("""
                QWidget {
                    background-color: white;
                    border: 1px solid #e8e8e8;
                    border-radius: 8px;
                }
                QWidget:hover {
                    background-color: #f9f7ff;
                    border: 1px solid #d4cff9;
                }
            """)
        else:
            container.setStyleSheet("""
                QWidget {
                    background-color: #f9f9f9;
                    border: 1px solid #e8e8e8;
                    border-radius: 8px;
                }
            """)
        
        return container
    
    def on_file_click(self, path_or_url: str, field_name: str):
        """Handle click on MOA or LO field"""
        success = open_file(path_or_url, show_error_callback=self.show_file_error)
        if success:
            print(f"[DEBUG] Opened {field_name}: {path_or_url}")
    
    def show_file_error(self, title: str, message: str):
        """Show error message for file operations"""
        QtWidgets.QMessageBox.warning(self, title, message)
    
    def on_edit_clicked(self):
        """Handle edit button click"""
        # Open edit window for this record
        try:
            window = EditRecordWindow(self.db, self.record_id)
            window.record_updated.connect(self.on_record_updated)
            window.show()
            # Keep a reference to prevent garbage collection
            self._edit_window = window
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to open edit window: {e}")

    def on_record_updated(self, record_id: int):
        """Handle record updated from edit window"""
        # Reload current record data
        self.load_record()
        # Notify parent pages so they can refresh tables
        self.record_updated.emit(record_id)
    
    def on_delete_clicked(self):
        """Handle delete button click"""
        reply = QtWidgets.QMessageBox.question(
            self, 
            "Delete Record", 
            f"Are you sure you want to delete {self.record.control_number}?",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            try:
                # Delete files
                if self.record.lo_file:
                    self.file_handler.delete_file(self.record.lo_file)
                if self.record.moa_file:
                    self.file_handler.delete_file(self.record.moa_file)
                
                # Delete from database
                self.db.delete_record(self.record.id)
                QtWidgets.QMessageBox.information(self, "Success", "Record deleted successfully")
                self.back_clicked.emit()
            except Exception as e:
                QtWidgets.QMessageBox.critical(self, "Error", f"Failed to delete record: {e}")
