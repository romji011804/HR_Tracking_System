"""
Edit Record Window for MOA Tracking System
Form for editing existing MOA and Legal Opinion records
"""
from qt_compat import QtCore, QtGui, QtWidgets, Signal
from database import Database
from models import Record
from utils.file_handler import FileHandler
from utils.file_opener import open_file
from components.recent_input_widget import RecentInputComboBox

Qt = QtCore.Qt
QDate = QtCore.QDate
QFont = QtGui.QFont

QMainWindow = QtWidgets.QMainWindow
QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QGroupBox = QtWidgets.QGroupBox
QLabel = QtWidgets.QLabel
QLineEdit = QtWidgets.QLineEdit
QDateEdit = QtWidgets.QDateEdit
QComboBox = QtWidgets.QComboBox
QCheckBox = QtWidgets.QCheckBox
QPushButton = QtWidgets.QPushButton
QFileDialog = QtWidgets.QFileDialog
QMessageBox = QtWidgets.QMessageBox
QGridLayout = QtWidgets.QGridLayout
QScrollArea = QtWidgets.QScrollArea
QDialog = QtWidgets.QDialog


class EditRecordWindow(QMainWindow):
    """Window for editing existing records"""
    
    record_updated = Signal(int)  # Emit record ID when updated
    
    def __init__(self, db: Database, record_id: int):
        super().__init__()
        self.db = db
        self.record_id = record_id
        self.record_data = None
        self.lo_file_path = None
        self.moa_file_path = None
        self.setWindowTitle("Edit Record")
        self.setGeometry(100, 100, 900, 800)
        self.init_ui()
        self.load_record()
    
    def init_ui(self):
        """Initialize the form UI"""
        # Scroll area for the form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        # Central widget
        form_widget = QWidget()
        main_layout = QVBoxLayout(form_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Edit Record")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Basic Information Group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QGridLayout()
        
        # Control Number (read-only)
        basic_layout.addWidget(QLabel("Control Number:"), 0, 0)
        self.control_number_input = QLineEdit()
        self.control_number_input.setReadOnly(True)
        basic_layout.addWidget(self.control_number_input, 0, 1)
        
        # School Name
        basic_layout.addWidget(QLabel("School/University Name:"), 1, 0)
        self.school_name_input = RecentInputComboBox("school")
        basic_layout.addWidget(self.school_name_input, 1, 1)
        
        # Course
        basic_layout.addWidget(QLabel("Course:"), 2, 0)
        self.course_input = RecentInputComboBox("course")
        basic_layout.addWidget(self.course_input, 2, 1)
        
        # Number of Hours
        basic_layout.addWidget(QLabel("Number of Hours:"), 3, 0)
        self.hours_input = RecentInputComboBox("hours")
        basic_layout.addWidget(self.hours_input, 3, 1)
        
        # Date Received
        basic_layout.addWidget(QLabel("Date Received:"), 4, 0)
        self.date_received_input = QDateEdit()
        self.date_received_input.setCalendarPopup(True)
        basic_layout.addWidget(self.date_received_input, 4, 1)
        
        basic_group.setLayout(basic_layout)
        main_layout.addWidget(basic_group)
        
        # Legal Opinion Section
        lo_group = QGroupBox("Legal Opinion Section")
        lo_layout = QGridLayout()
        
        # Date of Legal Opinion
        lo_layout.addWidget(QLabel("Date of Legal Opinion:"), 0, 0)
        self.date_lo_input = QDateEdit()
        self.date_lo_input.setCalendarPopup(True)
        lo_layout.addWidget(self.date_lo_input, 0, 1)
        
        # Legal Opinion Available
        lo_layout.addWidget(QLabel("Legal Opinion Available:"), 1, 0)
        self.lo_available_check = QCheckBox()
        lo_layout.addWidget(self.lo_available_check, 1, 1, alignment=Qt.AlignLeft)
        
        # LO Scanned
        lo_layout.addWidget(QLabel("LO Scanned:"), 2, 0)
        self.lo_scanned_check = QCheckBox()
        lo_layout.addWidget(self.lo_scanned_check, 2, 1, alignment=Qt.AlignLeft)
        
        # Upload LO File
        lo_layout.addWidget(QLabel("LO File:"), 3, 0)
        self.lo_file_label = QLineEdit()
        self.lo_file_label.setReadOnly(True)
        lo_layout.addWidget(self.lo_file_label, 3, 1)
        
        lo_file_btn = QPushButton("Browse...")
        lo_file_btn.clicked.connect(self.browse_lo_file)
        lo_layout.addWidget(lo_file_btn, 3, 2)
        
        lo_clear_btn = QPushButton("Clear")
        lo_clear_btn.clicked.connect(self.clear_lo_file)
        lo_layout.addWidget(lo_clear_btn, 3, 3)
        
        lo_open_btn = QPushButton("Open")
        lo_open_btn.clicked.connect(self.open_lo_file)
        lo_layout.addWidget(lo_open_btn, 3, 4)
        
        lo_group.setLayout(lo_layout)
        main_layout.addWidget(lo_group)
        
        # MOA Section
        moa_group = QGroupBox("MOA Section")
        moa_layout = QGridLayout()
        
        # Date of MOA
        moa_layout.addWidget(QLabel("Date of MOA:"), 0, 0)
        self.date_moa_input = QDateEdit()
        self.date_moa_input.setCalendarPopup(True)
        moa_layout.addWidget(self.date_moa_input, 0, 1)
        
        # MOA Available
        moa_layout.addWidget(QLabel("MOA Available:"), 1, 0)
        self.moa_available_check = QCheckBox()
        moa_layout.addWidget(self.moa_available_check, 1, 1, alignment=Qt.AlignLeft)
        
        # MOA Scanned
        moa_layout.addWidget(QLabel("MOA Scanned:"), 2, 0)
        self.moa_scanned_check = QCheckBox()
        moa_layout.addWidget(self.moa_scanned_check, 2, 1, alignment=Qt.AlignLeft)
        
        # Upload MOA File
        moa_layout.addWidget(QLabel("MOA File:"), 3, 0)
        self.moa_file_label = QLineEdit()
        self.moa_file_label.setReadOnly(True)
        moa_layout.addWidget(self.moa_file_label, 3, 1)
        
        moa_file_btn = QPushButton("Browse...")
        moa_file_btn.clicked.connect(self.browse_moa_file)
        moa_layout.addWidget(moa_file_btn, 3, 2)
        
        moa_clear_btn = QPushButton("Clear")
        moa_clear_btn.clicked.connect(self.clear_moa_file)
        moa_layout.addWidget(moa_clear_btn, 3, 3)
        
        moa_open_btn = QPushButton("Open")
        moa_open_btn.clicked.connect(self.open_moa_file)
        moa_layout.addWidget(moa_open_btn, 3, 4)
        
        moa_group.setLayout(moa_layout)
        main_layout.addWidget(moa_group)
        
        # Status Section
        status_group = QGroupBox("Status")
        status_layout = QGridLayout()
        
        # Workflow Stage
        status_layout.addWidget(QLabel("Workflow Stage:"), 0, 0)
        self.workflow_combo = QComboBox()
        self.workflow_combo.addItems([
            'Received',
            'For Legal Review',
            'Legal Opinion Issued',
            'MOA Preparation',
            'For Signing',
            'Completed'
        ])
        status_layout.addWidget(self.workflow_combo, 0, 1)
        
        # Status
        status_layout.addWidget(QLabel("Status:"), 1, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Ongoing', 'Completed'])
        status_layout.addWidget(self.status_combo, 1, 1)
        
        status_group.setLayout(status_layout)
        main_layout.addWidget(status_group)
        
        main_layout.addStretch()
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("Save Changes")
        save_btn.clicked.connect(self.save_record)
        save_btn.setFixedWidth(150)
        
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.close)
        cancel_btn.setFixedWidth(150)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        
        main_layout.addLayout(button_layout)
        
        # Set scroll area
        scroll.setWidget(form_widget)
        self.setCentralWidget(scroll)
    
    def load_record(self):
        """Load record data from database"""
        try:
            self.record_data = self.db.get_record(self.record_id)
            if not self.record_data:
                QMessageBox.warning(self, "Error", "Record not found")
                self.close()
                return
            
            record = Record.from_dict(self.record_data)
            
            # Fill form fields
            self.control_number_input.setText(record.control_number)
            self.school_name_input.setEditText(record.school_name)
            self.course_input.setEditText(record.course)
            self.hours_input.setEditText(str(record.number_of_hours))
            self.date_received_input.setDate(QDate.fromString(record.date_received, 'yyyy-MM-dd'))
            
            if record.date_lo:
                self.date_lo_input.setDate(QDate.fromString(record.date_lo, 'yyyy-MM-dd'))
            self.lo_available_check.setChecked(record.legal_opinion)
            self.lo_scanned_check.setChecked(record.lo_scanned)
            if record.lo_file:
                self.lo_file_label.setText(record.lo_file)
            
            if record.date_moa:
                self.date_moa_input.setDate(QDate.fromString(record.date_moa, 'yyyy-MM-dd'))
            self.moa_available_check.setChecked(record.moa_available)
            self.moa_scanned_check.setChecked(record.moa_scanned)
            if record.moa_file:
                self.moa_file_label.setText(record.moa_file)
            
            self.workflow_combo.setCurrentText(record.workflow_stage)
            self.status_combo.setCurrentText(record.status)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load record: {str(e)}")
            self.close()
    
    def browse_lo_file(self):
        """Browse and select Legal Opinion file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Legal Opinion PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.lo_file_path = file_path
            self.lo_file_label.setText(file_path)
    
    def browse_moa_file(self):
        """Browse and select MOA file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select MOA PDF", "", "PDF Files (*.pdf)"
        )
        if file_path:
            self.moa_file_path = file_path
            self.moa_file_label.setText(file_path)
    
    def clear_lo_file(self):
        """Clear Legal Opinion file"""
        self.lo_file_path = None
        self.lo_file_label.setText("")
    
    def clear_moa_file(self):
        """Clear MOA file"""
        self.moa_file_path = None
        self.moa_file_label.setText("")
    
    def open_lo_file(self):
        """Open stored Legal Opinion file"""
        lo_file = self.record_data.get('lo_file') if self.record_data else None
        if lo_file:
            # Use unified file/link opener so URLs also work
            if not open_file(lo_file, show_error_callback=lambda title, msg: QMessageBox.warning(self, title, msg)):
                QMessageBox.warning(self, "Error", "Could not open file or link")
        else:
            QMessageBox.information(self, "Info", "No Legal Opinion file available")
    
    def open_moa_file(self):
        """Open stored MOA file"""
        moa_file = self.record_data.get('moa_file') if self.record_data else None
        if moa_file:
            # Use unified file/link opener so URLs also work
            if not open_file(moa_file, show_error_callback=lambda title, msg: QMessageBox.warning(self, title, msg)):
                QMessageBox.warning(self, "Error", "Could not open file or link")
        else:
            QMessageBox.information(self, "Info", "No MOA file available")
    
    def save_record(self):
        """Save changes to record"""
        # Validation
        if not self.school_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter School/University name")
            return
        
        if not self.course_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter Course name")
            return
        
        try:
            control_number = self.control_number_input.text()
            # Parse hours from text with fallback to 0
            hours_text = self.hours_input.text().strip()
            try:
                hours_value = int(hours_text) if hours_text else 0
            except ValueError:
                QMessageBox.warning(self, "Validation Error", "Number of Hours must be a whole number")
                return
            
            # Handle new file uploads
            lo_file_path = self.record_data.get('lo_file')
            moa_file_path = self.record_data.get('moa_file')
            
            # If new LO file selected, upload it and delete old one
            if self.lo_file_path:
                if lo_file_path:
                    FileHandler.delete_file(lo_file_path)
                lo_file_path = FileHandler.upload_file(
                    self.lo_file_path, 'lo', control_number
                )
                if not lo_file_path:
                    QMessageBox.warning(self, "Error", "Failed to upload Legal Opinion file")
                    return
            
            # If new MOA file selected, upload it and delete old one
            if self.moa_file_path:
                if moa_file_path:
                    FileHandler.delete_file(moa_file_path)
                moa_file_path = FileHandler.upload_file(
                    self.moa_file_path, 'moa', control_number
                )
                if not moa_file_path:
                    QMessageBox.warning(self, "Error", "Failed to upload MOA file")
                    return
            
            # Prepare updated data
            data = {
                'control_number': control_number,
                'school_name': self.school_name_input.text().strip(),
                'course': self.course_input.text().strip(),
                'number_of_hours': hours_value,
                'date_received': self.date_received_input.date().toString('yyyy-MM-dd'),
                'date_lo': self.date_lo_input.date().toString('yyyy-MM-dd'),
                'legal_opinion': self.lo_available_check.isChecked(),
                'lo_scanned': self.lo_scanned_check.isChecked(),
                'lo_file': lo_file_path,
                'date_moa': self.date_moa_input.date().toString('yyyy-MM-dd'),
                'moa_available': self.moa_available_check.isChecked(),
                'moa_scanned': self.moa_scanned_check.isChecked(),
                'moa_file': moa_file_path,
                'workflow_stage': self.workflow_combo.currentText(),
                'status': self.status_combo.currentText()
            }
            
            # Update in database
            if self.db.update_record(self.record_id, data):
                QMessageBox.information(self, "Success", "Record updated successfully!")
                # Save to recent inputs for autocomplete
                self.school_name_input.on_input_finished()
                self.course_input.on_input_finished()
                self.hours_input.on_input_finished()
                self.record_updated.emit(self.record_id)
                self.close()
            else:
                QMessageBox.warning(self, "Error", "Failed to update record")
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save record: {str(e)}")
