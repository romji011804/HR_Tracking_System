"""
Add Record Page
Form for creating new MOA and Legal Opinion records with 2-column layout
"""
from qt_compat import QtCore, QtGui, QtWidgets, Signal
from database import Database
from utils.file_handler import FileHandler
from utils.control_number_generator import generate_control_number
from components.recent_input_widget import RecentInputComboBox
import sqlite3

Qt = QtCore.Qt
QDate = QtCore.QDate
QFont = QtGui.QFont

QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QGroupBox = QtWidgets.QGroupBox
QGridLayout = QtWidgets.QGridLayout
QLabel = QtWidgets.QLabel
QLineEdit = QtWidgets.QLineEdit
QDateEdit = QtWidgets.QDateEdit
QComboBox = QtWidgets.QComboBox
QCheckBox = QtWidgets.QCheckBox
QPushButton = QtWidgets.QPushButton
QFileDialog = QtWidgets.QFileDialog
QMessageBox = QtWidgets.QMessageBox
QSpinBox = QtWidgets.QSpinBox
QScrollArea = QtWidgets.QScrollArea
QRadioButton = QtWidgets.QRadioButton
QButtonGroup = QtWidgets.QButtonGroup


class AddRecordPage(QWidget):
    """Page for adding new records with 2-column layout"""
    
    record_added = Signal(int)
    
    def __init__(self, db: Database, record_id: int = None):
        super().__init__()
        self.db = db
        self.record_id = record_id  # For edit mode
        self.is_edit_mode = record_id is not None
        self.original_record = None  # Preserve original DB values for edit mode
        self.lo_file_path = None
        self.moa_file_path = None
        self.recent_schools = self.load_recent_schools()
        self.recent_courses = self.load_recent_courses()
        self.init_ui()
    
    def load_recent_schools(self):
        """Load recently used schools from database"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT school_name FROM records WHERE school_name IS NOT NULL AND school_name != "" ORDER BY created_at DESC LIMIT 5')
            schools = []
            for row in cursor.fetchall():
                if row[0]:  # Check if value exists
                    schools.append(row[0])
            cursor.close()
            conn.close()
            return schools
        except Exception as e:
            print(f"[WARNING] Failed to load recent schools: {e}")
            return []
    
    def load_recent_courses(self):
        """Load recently used courses from database"""
        try:
            conn = self.db.get_connection()
            cursor = conn.cursor()
            cursor.execute('SELECT DISTINCT course FROM records WHERE course IS NOT NULL AND course != "" ORDER BY created_at DESC LIMIT 5')
            courses = []
            for row in cursor.fetchall():
                if row[0]:  # Check if value exists
                    courses.append(row[0])
            cursor.close()
            conn.close()
            return courses
        except Exception as e:
            print(f"[WARNING] Failed to load recent courses: {e}")
            return []
    
    def init_ui(self):
        """Initialize form UI with 2-column layout"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Page Title
        title_text = "Edit Record" if self.is_edit_mode else "Add New Record"
        title = QLabel(title_text)
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a1a1a;")
        main_layout.addWidget(title)
        
        # Scroll area for form
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: white;
            }
            QScrollBar:vertical {
                width: 8px;
                background: white;
            }
            QScrollBar::handle:vertical {
                background: #d1d5db;
                border-radius: 4px;
            }
            QScrollBar::handle:vertical:hover {
                background: #999;
            }
        """)
        
        form_widget = QWidget()
        form_layout = QHBoxLayout(form_widget)
        form_layout.setSpacing(30)
        form_layout.setContentsMargins(0, 0, 0, 0)
        
        # ============== LEFT COLUMN ==============
        left_layout = QVBoxLayout()
        left_layout.setSpacing(15)
        
        # Control Number (read-only)
        control_group = self.create_group_box("Control Information")
        control_layout = QGridLayout()
        control_layout.addWidget(QLabel("Control Number:"), 0, 0)
        self.control_number_input = QLineEdit()
        self.control_number_input.setReadOnly(True)
        self.control_number_input.setText(generate_control_number(self.db))
        self.control_number_input.setFixedHeight(35)
        control_layout.addWidget(self.control_number_input, 0, 1)
        control_group.setLayout(control_layout)
        left_layout.addWidget(control_group)
        
        # Basic Information
        basic_group = self.create_group_box("Basic Information")
        basic_layout = QGridLayout()
        basic_layout.setSpacing(12)
        
        # School/University with recent inputs dropdown
        basic_layout.addWidget(QLabel("🏫 School/University:"), 0, 0)
        self.school_name_input = RecentInputComboBox("school")
        self.school_name_input.setFixedHeight(35)
        basic_layout.addWidget(self.school_name_input, 0, 1)
        
        # Course with recent inputs dropdown
        basic_layout.addWidget(QLabel("📖 Course:"), 1, 0)
        self.course_input = RecentInputComboBox("course")
        self.course_input.setFixedHeight(35)
        basic_layout.addWidget(self.course_input, 1, 1)
        
        # Hours with recent inputs dropdown
        basic_layout.addWidget(QLabel("⏱️ Hours:"), 2, 0)
        self.hours_input = RecentInputComboBox("hours")
        self.hours_input.setFixedHeight(35)
        basic_layout.addWidget(self.hours_input, 2, 1)
        
        # Date Received
        basic_layout.addWidget(QLabel("📅 Date Received:"), 3, 0)
        self.date_received_input = QDateEdit()
        self.date_received_input.setDate(QDate.currentDate())
        self.date_received_input.setCalendarPopup(True)
        self.date_received_input.setFixedHeight(35)
        basic_layout.addWidget(self.date_received_input, 3, 1)
        
        basic_group.setLayout(basic_layout)
        left_layout.addWidget(basic_group)
        
        # Status Section
        status_group = self.create_group_box("Status & Workflow")
        status_layout = QGridLayout()
        status_layout.setSpacing(12)
        
        status_layout.addWidget(QLabel("✓ Status:"), 0, 0)
        self.status_combo = QComboBox()
        self.status_combo.addItems(['Ongoing', 'Completed'])
        self.status_combo.setFixedHeight(35)
        status_layout.addWidget(self.status_combo, 0, 1)
        
        status_layout.addWidget(QLabel("→ Workflow Stage:"), 1, 0)
        self.workflow_combo = QComboBox()
        self.workflow_combo.addItems([
            'Received',
            'For Legal Review',
            'Legal Opinion Issued',
            'MOA Preparation',
            'For Signing',
            'Completed'
        ])
        self.workflow_combo.setFixedHeight(35)
        status_layout.addWidget(self.workflow_combo, 1, 1)
        
        status_group.setLayout(status_layout)
        left_layout.addWidget(status_group)
        left_layout.addStretch()
        
        # ============== RIGHT COLUMN ==============
        right_layout = QVBoxLayout()
        right_layout.setSpacing(15)
        
        # Legal Opinion Section
        lo_group = self.create_group_box("Legal Opinion")
        lo_layout = QGridLayout()
        lo_layout.setSpacing(12)
        
        lo_layout.addWidget(QLabel("Date:"), 0, 0)
        self.date_lo_input = QDateEdit()
        self.date_lo_input.setDate(QDate.currentDate())
        self.date_lo_input.setCalendarPopup(True)
        self.date_lo_input.setFixedHeight(35)
        lo_layout.addWidget(self.date_lo_input, 0, 1)
        
        lo_layout.addWidget(QLabel("Available:"), 1, 0)
        self.lo_available_check = QCheckBox()
        lo_layout.addWidget(self.lo_available_check, 1, 1, alignment=Qt.AlignLeft)
        
        lo_layout.addWidget(QLabel("Scanned:"), 2, 0)
        self.lo_scanned_check = QCheckBox()
        lo_layout.addWidget(self.lo_scanned_check, 2, 1, alignment=Qt.AlignLeft)
        
        # LO File - Upload or Link
        lo_layout.addWidget(QLabel("File/Link:"), 3, 0)
        lo_file_type_layout = QHBoxLayout()
        self.lo_upload_radio = QRadioButton("Upload")
        self.lo_link_radio = QRadioButton("Paste Link")
        self.lo_upload_radio.setChecked(True)
        self.lo_type_group = QButtonGroup(self)
        self.lo_type_group.addButton(self.lo_upload_radio, 0)
        self.lo_type_group.addButton(self.lo_link_radio, 1)
        lo_file_type_layout.addWidget(self.lo_upload_radio)
        lo_file_type_layout.addWidget(self.lo_link_radio)
        lo_layout.addLayout(lo_file_type_layout, 3, 1)
        
        lo_layout.addWidget(QLabel(""), 4, 0)
        lo_file_layout = QHBoxLayout()
        self.lo_file_input = QLineEdit()
        self.lo_file_input.setFixedHeight(35)
        self.lo_file_input.setPlaceholderText("Click Browse... or paste URL")
        self.lo_file_input.setReadOnly(True)
        lo_file_layout.addWidget(self.lo_file_input)
        
        self.lo_browse_btn = QPushButton("Browse...")
        self.lo_browse_btn.setFixedWidth(100)
        self.lo_browse_btn.setFixedHeight(35)
        self.lo_browse_btn.clicked.connect(self.browse_lo_file)
        lo_file_layout.addWidget(self.lo_browse_btn)
        lo_layout.addLayout(lo_file_layout, 4, 1)

        # Switch between upload and link modes
        self.lo_upload_radio.toggled.connect(self.update_lo_input_mode)
        self.lo_link_radio.toggled.connect(self.update_lo_input_mode)
        
        lo_group.setLayout(lo_layout)
        right_layout.addWidget(lo_group)
        
        # MOA Section
        moa_group = self.create_group_box("Memorandum of Agreement")
        moa_layout = QGridLayout()
        moa_layout.setSpacing(12)
        
        moa_layout.addWidget(QLabel("Date:"), 0, 0)
        self.date_moa_input = QDateEdit()
        self.date_moa_input.setDate(QDate.currentDate())
        self.date_moa_input.setCalendarPopup(True)
        self.date_moa_input.setFixedHeight(35)
        moa_layout.addWidget(self.date_moa_input, 0, 1)
        
        moa_layout.addWidget(QLabel("Available:"), 1, 0)
        self.moa_available_check = QCheckBox()
        moa_layout.addWidget(self.moa_available_check, 1, 1, alignment=Qt.AlignLeft)
        
        moa_layout.addWidget(QLabel("Scanned:"), 2, 0)
        self.moa_scanned_check = QCheckBox()
        moa_layout.addWidget(self.moa_scanned_check, 2, 1, alignment=Qt.AlignLeft)
        
        # MOA File - Upload or Link
        moa_layout.addWidget(QLabel("File/Link:"), 3, 0)
        moa_file_type_layout = QHBoxLayout()
        self.moa_upload_radio = QRadioButton("Upload")
        self.moa_link_radio = QRadioButton("Paste Link")
        self.moa_upload_radio.setChecked(True)
        self.moa_type_group = QButtonGroup(self)
        self.moa_type_group.addButton(self.moa_upload_radio, 0)
        self.moa_type_group.addButton(self.moa_link_radio, 1)
        moa_file_type_layout.addWidget(self.moa_upload_radio)
        moa_file_type_layout.addWidget(self.moa_link_radio)
        moa_layout.addLayout(moa_file_type_layout, 3, 1)
        
        moa_layout.addWidget(QLabel(""), 4, 0)
        moa_file_layout = QHBoxLayout()
        self.moa_file_input = QLineEdit()
        self.moa_file_input.setFixedHeight(35)
        self.moa_file_input.setPlaceholderText("Click Browse... or paste URL")
        self.moa_file_input.setReadOnly(True)
        moa_file_layout.addWidget(self.moa_file_input)
        
        self.moa_browse_btn = QPushButton("Browse...")
        self.moa_browse_btn.setFixedWidth(100)
        self.moa_browse_btn.setFixedHeight(35)
        self.moa_browse_btn.clicked.connect(self.browse_moa_file)
        moa_file_layout.addWidget(self.moa_browse_btn)
        moa_layout.addLayout(moa_file_layout, 4, 1)

        # Switch between upload and link modes
        self.moa_upload_radio.toggled.connect(self.update_moa_input_mode)
        self.moa_link_radio.toggled.connect(self.update_moa_input_mode)
        
        moa_group.setLayout(moa_layout)
        right_layout.addWidget(moa_group)
        right_layout.addStretch()
        
        # Add columns to main layout
        form_layout.addLayout(left_layout, 1)
        form_layout.addLayout(right_layout, 1)
        
        scroll.setWidget(form_widget)
        main_layout.addWidget(scroll)
        
        # Buttons
        button_layout = QHBoxLayout()
        button_layout.addStretch()
        
        save_btn = QPushButton("💾 Save Record")
        save_btn.setFixedWidth(140)
        save_btn.setFixedHeight(40)
        save_btn.setStyleSheet("""
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
        save_btn.clicked.connect(self.save_record)
        
        clear_btn = QPushButton("🔄 Clear Form")
        clear_btn.setFixedWidth(140)
        clear_btn.setFixedHeight(40)
        clear_btn.setStyleSheet("""
            QPushButton {
                background-color: #e5e7eb;
                color: #333;
                border: none;
                border-radius: 5px;
                font-weight: 500;
            }
            QPushButton:hover {
                background-color: #d1d5db;
            }
        """)
        clear_btn.clicked.connect(self.clear_form)
        
        button_layout.addWidget(save_btn)
        button_layout.addWidget(clear_btn)
        
        main_layout.addLayout(button_layout)
        
        self.setLayout(main_layout)
        self.setStyleSheet("""
            AddRecordPage {
                background-color: #f5f5f5;
            }
        """)
        
        # Load record if in edit mode
        if self.is_edit_mode:
            self.load_record_data()
    
    def create_group_box(self, title: str) -> QGroupBox:
        """Create a styled group box"""
        group = QGroupBox(title)
        group_font = QFont()
        group_font.setPointSize(11)
        group_font.setBold(True)
        group.setFont(group_font)
        group.setStyleSheet("""
            QGroupBox {
                border: 1px solid #e8e8e8;
                border-radius: 6px;
                margin-top: 10px;
                padding-top: 10px;
                background-color: white;
                color: #333;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                subcontrol-position: top left;
                left: 10px;
                padding: 0 3px 0 3px;
            }
        """)
        return group
    
    def browse_lo_file(self):
        """Browse and select Legal Opinion file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Legal Opinion PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.lo_file_path = file_path
            self.lo_file_input.setText(file_path)
            self.lo_upload_radio.setChecked(True)
            # Ensure we are in upload mode
            self.update_lo_input_mode()
    
    def browse_moa_file(self):
        """Browse and select MOA file"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select MOA PDF", "", "PDF Files (*.pdf);;All Files (*)"
        )
        if file_path:
            self.moa_file_path = file_path
            self.moa_file_input.setText(file_path)
            self.moa_upload_radio.setChecked(True)
            # Ensure we are in upload mode
            self.update_moa_input_mode()

    def update_lo_input_mode(self):
        """Toggle LO input between file upload and URL paste modes"""
        is_upload = self.lo_upload_radio.isChecked()
        # Upload mode: read-only input, browse enabled
        self.lo_file_input.setReadOnly(is_upload)
        self.lo_browse_btn.setEnabled(is_upload)
        if is_upload:
            self.lo_file_input.setPlaceholderText("Click Browse... to select PDF")
        else:
            self.lo_file_input.setPlaceholderText("Paste Legal Opinion URL (e.g., https://...)")

    def update_moa_input_mode(self):
        """Toggle MOA input between file upload and URL paste modes"""
        is_upload = self.moa_upload_radio.isChecked()
        # Upload mode: read-only input, browse enabled
        self.moa_file_input.setReadOnly(is_upload)
        self.moa_browse_btn.setEnabled(is_upload)
        if is_upload:
            self.moa_file_input.setPlaceholderText("Click Browse... to select PDF")
        else:
            self.moa_file_input.setPlaceholderText("Paste MOA URL (e.g., https://...)")
    
    def load_record_data(self):
        """Load record data for edit mode"""
        try:
            record_dict = self.db.get_record(self.record_id)
            self.original_record = record_dict
            if not record_dict:
                QMessageBox.warning(self, "Error", "Record not found")
                return
            
            from models import Record
            record = Record.from_dict(record_dict)
            
            # Auto-fill form fields
            self.control_number_input.setText(record.control_number)
            self.school_name_input.setEditText(record.school_name)
            self.course_input.setEditText(record.course)
            self.hours_input.setEditText(str(record.number_of_hours))
            self.date_received_input.setDate(QDate.fromString(record.date_received, 'yyyy-MM-dd'))
            
            # LO info
            lo_date = record.date_lo if record.date_lo else QDate.currentDate().toString('yyyy-MM-dd')
            self.date_lo_input.setDate(QDate.fromString(lo_date, 'yyyy-MM-dd'))
            self.lo_available_check.setChecked(record.legal_opinion)
            self.lo_scanned_check.setChecked(record.lo_scanned)
            if record.lo_file:
                self.lo_file_input.setText(record.lo_file)
                # Determine if it's a link or file
                if record.lo_file.startswith('http://') or record.lo_file.startswith('https://'):
                    self.lo_link_radio.setChecked(True)
                    self.lo_file_path = None
                else:
                    self.lo_upload_radio.setChecked(True)
                    # Keep the stored relative path but do not treat it as a new upload source
                    self.lo_file_path = None
            
            # MOA info
            moa_date = record.date_moa if record.date_moa else QDate.currentDate().toString('yyyy-MM-dd')
            self.date_moa_input.setDate(QDate.fromString(moa_date, 'yyyy-MM-dd'))
            self.moa_available_check.setChecked(record.moa_available)
            self.moa_scanned_check.setChecked(record.moa_scanned)
            if record.moa_file:
                self.moa_file_input.setText(record.moa_file)
                # Determine if it's a link or file
                if record.moa_file.startswith('http://') or record.moa_file.startswith('https://'):
                    self.moa_link_radio.setChecked(True)
                    self.moa_file_path = None
                else:
                    self.moa_upload_radio.setChecked(True)
                    # Keep the stored relative path but do not treat it as a new upload source
                    self.moa_file_path = None
            
            # Status
            self.workflow_combo.setCurrentText(record.workflow_stage)
            self.status_combo.setCurrentText(record.status)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load record: {e}")
    
    def clear_form(self):
        """Clear all form fields"""
        self.school_name_input.setEditText("")
        self.course_input.setEditText("")
        self.hours_input.setEditText("")
        self.date_received_input.setDate(QDate.currentDate())
        self.date_lo_input.setDate(QDate.currentDate())
        self.date_moa_input.setDate(QDate.currentDate())
        
        self.lo_available_check.setChecked(False)
        self.lo_scanned_check.setChecked(False)
        self.lo_file_path = None
        self.lo_file_input.clear()
        self.lo_upload_radio.setChecked(True)
        
        self.moa_available_check.setChecked(False)
        self.moa_scanned_check.setChecked(False)
        self.moa_file_path = None
        self.moa_file_input.clear()
        self.moa_upload_radio.setChecked(True)
        
        self.workflow_combo.setCurrentIndex(0)
        self.status_combo.setCurrentIndex(0)
        
        if not self.is_edit_mode:
            self.control_number_input.setText(generate_control_number(self.db))
    
    def save_record(self):
        """Save the record to database with validation"""
        # Validate required fields
        school_name = self.school_name_input.text().strip()
        course = self.course_input.text().strip()
        
        if not school_name:
            QMessageBox.warning(self, "Validation Error", "⚠️ School/University name is REQUIRED")
            self.school_name_input.setFocus()
            return
        
        if not course:
            QMessageBox.warning(self, "Validation Error", "⚠️ Course name is REQUIRED")
            self.course_input.setFocus()
            return
        
        try:
            control_number = self.control_number_input.text()
            
            # Check if control number already exists (only for new records)
            if not self.is_edit_mode and self.db.record_exists(control_number):
                QMessageBox.warning(self, "Error", f"Control number '{control_number}' already exists")
                return
            
            # Start from existing stored values in edit mode to preserve files/links
            existing_lo = None
            existing_moa = None
            if self.is_edit_mode and self.original_record:
                existing_lo = self.original_record.get('lo_file')
                existing_moa = self.original_record.get('moa_file')

            # Handle file uploads/links
            lo_file_path = existing_lo
            moa_file_path = existing_moa
            
            # Legal Opinion
            lo_input_text = self.lo_file_input.text().strip()
            if lo_input_text:
                if self.lo_link_radio.isChecked():
                    # It's a link/URL - normalize it
                    lo_file_path = lo_input_text
                    if lo_file_path and not lo_file_path.startswith('http://') and not lo_file_path.startswith('https://'):
                        lo_file_path = 'https://' + lo_file_path
                    print("Saved URL:", lo_file_path)
                elif self.lo_upload_radio.isChecked() and self.lo_file_path:
                    # It's a file to upload (new selection)
                    lo_file_path = FileHandler.upload_file(
                        self.lo_file_path, 'lo', control_number
                    )
                    if not lo_file_path:
                        QMessageBox.warning(self, "Error", "Failed to upload Legal Opinion file")
                        return
            else:
                # If user cleared the field, remove stored value
                lo_file_path = None
            
            # MOA
            moa_input_text = self.moa_file_input.text().strip()
            if moa_input_text:
                if self.moa_link_radio.isChecked():
                    # It's a link/URL - normalize it
                    moa_file_path = moa_input_text
                    if moa_file_path and not moa_file_path.startswith('http://') and not moa_file_path.startswith('https://'):
                        moa_file_path = 'https://' + moa_file_path
                    print("Saved URL:", moa_file_path)
                elif self.moa_upload_radio.isChecked() and self.moa_file_path:
                    # It's a file to upload (new selection)
                    moa_file_path = FileHandler.upload_file(
                        self.moa_file_path, 'moa', control_number
                    )
                    if not moa_file_path:
                        QMessageBox.warning(self, "Error", "Failed to upload MOA file")
                        return
            else:
                # If user cleared the field, remove stored value
                moa_file_path = None
            
            # Prepare data
            data = {
                'control_number': control_number,
                'school_name': school_name,
                'course': course,
                'number_of_hours': int(self.hours_input.text().strip() or "0"),
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
            
            # Save to database
            if self.is_edit_mode:
                # Update existing record
                success = self.db.update_record(self.record_id, data)
                if success:
                    # Save to recent inputs
                    self.school_name_input.on_input_finished()
                    self.course_input.on_input_finished()
                    self.hours_input.on_input_finished()
                    QMessageBox.information(self, "Success", "Record updated successfully!")
                    self.record_added.emit(self.record_id)
                else:
                    QMessageBox.critical(self, "Error", "Failed to update record")
            else:
                # Add new record
                record_id = self.db.add_record(data)
                # Save to recent inputs
                self.school_name_input.on_input_finished()
                self.course_input.on_input_finished()
                self.hours_input.on_input_finished()
                QMessageBox.information(
                    self, "Success",
                    f"✓ Record added successfully!\nControl Number: {control_number}"
                )
                self.clear_form()
                self.record_added.emit(record_id)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save record: {str(e)}")
