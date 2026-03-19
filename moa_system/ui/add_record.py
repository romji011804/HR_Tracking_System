"""
Add Record Window for MOA Tracking System
Form for creating new MOA and Legal Opinion records
"""
from qt_compat import QtCore, QtGui, QtWidgets, Signal
from database import Database
from models import Record
from utils.file_handler import FileHandler
from utils.control_number_generator import generate_control_number

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
QSpinBox = QtWidgets.QSpinBox
QGridLayout = QtWidgets.QGridLayout
QScrollArea = QtWidgets.QScrollArea

class AddRecordWindow(QMainWindow):
    """Window for adding new records"""
    
    record_added = Signal(int)  # Emit record ID when added
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.lo_file_path = None
        self.moa_file_path = None
        self.setWindowTitle("Add New Record")
        self.setGeometry(100, 100, 900, 800)
        self.init_ui()
    
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
        title = QLabel("Add New Record")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Basic Information Group
        basic_group = QGroupBox("Basic Information")
        basic_layout = QGridLayout()
        
        # Control Number (auto-generated, read-only)
        basic_layout.addWidget(QLabel("Control Number:"), 0, 0)
        self.control_number_input = QLineEdit()
        self.control_number_input.setReadOnly(True)
        self.control_number_input.setText(generate_control_number(self.db))
        basic_layout.addWidget(self.control_number_input, 0, 1)
        
        # School Name
        basic_layout.addWidget(QLabel("School/University Name:"), 1, 0)
        self.school_name_input = QLineEdit()
        basic_layout.addWidget(self.school_name_input, 1, 1)
        
        # Course
        basic_layout.addWidget(QLabel("Course:"), 2, 0)
        self.course_input = QLineEdit()
        basic_layout.addWidget(self.course_input, 2, 1)
        
        # Number of Hours
        basic_layout.addWidget(QLabel("Number of Hours:"), 3, 0)
        self.hours_input = QSpinBox()
        self.hours_input.setMaximum(10000)
        basic_layout.addWidget(self.hours_input, 3, 1)
        
        # Date Received
        basic_layout.addWidget(QLabel("Date Received:"), 4, 0)
        self.date_received_input = QDateEdit()
        self.date_received_input.setDate(QDate.currentDate())
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
        self.date_lo_input.setDate(QDate.currentDate())
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
        lo_layout.addWidget(QLabel("Upload LO File (PDF):"), 3, 0)
        self.lo_file_label = QLineEdit()
        self.lo_file_label.setReadOnly(True)
        lo_layout.addWidget(self.lo_file_label, 3, 1)
        
        lo_file_btn = QPushButton("Browse...")
        lo_file_btn.clicked.connect(self.browse_lo_file)
        lo_layout.addWidget(lo_file_btn, 3, 2)
        
        lo_group.setLayout(lo_layout)
        main_layout.addWidget(lo_group)
        
        # MOA Section
        moa_group = QGroupBox("MOA Section")
        moa_layout = QGridLayout()
        
        # Date of MOA
        moa_layout.addWidget(QLabel("Date of MOA:"), 0, 0)
        self.date_moa_input = QDateEdit()
        self.date_moa_input.setDate(QDate.currentDate())
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
        moa_layout.addWidget(QLabel("Upload MOA File (PDF):"), 3, 0)
        self.moa_file_label = QLineEdit()
        self.moa_file_label.setReadOnly(True)
        moa_layout.addWidget(self.moa_file_label, 3, 1)
        
        moa_file_btn = QPushButton("Browse...")
        moa_file_btn.clicked.connect(self.browse_moa_file)
        moa_layout.addWidget(moa_file_btn, 3, 2)
        
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
        
        save_btn = QPushButton("Save Record")
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
    
    def save_record(self):
        """Save the record to database"""
        # Validation
        if not self.school_name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter School/University name")
            return
        
        if not self.course_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Please enter Course name")
            return
        
        try:
            control_number = self.control_number_input.text()
            
            # Check if control number already exists
            if self.db.record_exists(control_number):
                QMessageBox.warning(self, "Error", "This control number already exists")
                return
            
            # Upload files if selected
            lo_file_path = None
            moa_file_path = None
            
            if self.lo_file_path:
                lo_file_path = FileHandler.upload_file(
                    self.lo_file_path, 'lo', control_number
                )
                if not lo_file_path:
                    QMessageBox.warning(self, "Error", "Failed to upload Legal Opinion file")
                    return
            
            if self.moa_file_path:
                moa_file_path = FileHandler.upload_file(
                    self.moa_file_path, 'moa', control_number
                )
                if not moa_file_path:
                    QMessageBox.warning(self, "Error", "Failed to upload MOA file")
                    return
            
            # Prepare data
            data = {
                'control_number': control_number,
                'school_name': self.school_name_input.text(),
                'course': self.course_input.text(),
                'number_of_hours': self.hours_input.value(),
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
            
            # Add to database
            record_id = self.db.add_record(data)
            
            QMessageBox.information(
                self, "Success",
                f"Record added successfully!\nControl Number: {control_number}"
            )
            
            self.record_added.emit(record_id)
            self.close()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save record: {str(e)}")
