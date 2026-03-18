"""
Records Table Window for MOA Tracking System
Displays all records with search, filter, and action buttons
"""
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QComboBox, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QHeaderView, QAbstractItemView
)
from PyQt5.QtCore import Qt, pyqtSignal, QSize
from PyQt5.QtGui import QFont, QColor, QIcon, QBrush
from database import Database
from models import Record
from utils.file_handler import FileHandler

class RecordsTableWindow(QMainWindow):
    """Window for displaying and managing records"""
    
    edit_record_signa = pyqtSignal(int)  # Emit record ID when edit is requested
    refresh_requested = pyqtSignal()
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_filters = {}
        self.setWindowTitle("Records - MOA & Legal Opinion Tracking System")
        self.setGeometry(100, 100, 1400, 700)
        self.init_ui()
        self.load_records()
    
    def init_ui(self):
        """Initialize the records table UI"""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main layout
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Records Management")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        main_layout.addWidget(title)
        
        # Search and Filter Layout
        filter_layout = QHBoxLayout()
        filter_layout.setSpacing(10)
        
        # Search bar
        filter_layout.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search by Control #, School, or Course...")
        self.search_input.textChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.search_input, 1)
        
        # Filter dropdown
        filter_layout.addWidget(QLabel("Filter:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems([
            'All',
            'Ongoing',
            'Completed',
            'Missing LO',
            'Missing MOA'
        ])
        self.filter_combo.currentTextChanged.connect(self.apply_filters)
        filter_layout.addWidget(self.filter_combo)
        
        # Refresh button
        refresh_btn = QPushButton("Refresh")
        refresh_btn.clicked.connect(self.load_records)
        filter_layout.addWidget(refresh_btn)
        
        main_layout.addLayout(filter_layout)
        
        # Records Table
        self.table = QTableWidget()
        self.table.setColumnCount(9)
        self.table.setHorizontalHeaderLabels([
            'Control Number', 'School/University', 'Course', 'Hours',
            'Date Received', 'LO Status', 'MOA Status', 'Workflow', 'Status'
        ])
        
        # Set column widths
        self.table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.table.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        
        main_layout.addWidget(self.table)
        
        # Action Buttons Layout
        action_layout = QHBoxLayout()
        action_layout.addStretch()
        
        view_btn = QPushButton("View")
        view_btn.clicked.connect(self.view_record)
        view_btn.setFixedWidth(100)
        
        edit_btn = QPushButton("Edit")
        edit_btn.clicked.connect(self.edit_record)
        edit_btn.setFixedWidth(100)
        
        delete_btn = QPushButton("Delete")
        delete_btn.clicked.connect(self.delete_record)
        delete_btn.setFixedWidth(100)
        
        action_layout.addWidget(view_btn)
        action_layout.addWidget(edit_btn)
        action_layout.addWidget(delete_btn)
        
        main_layout.addLayout(action_layout)
    
    def load_records(self):
        """Load records from database"""
        try:
            records = self.db.get_all_records()
            self.display_records(records)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load records: {str(e)}")
    
    def apply_filters(self):
        """Apply search and filter to records"""
        search_text = self.search_input.text()
        filter_type = self.filter_combo.currentText()
        
        filters = {}
        if search_text:
            filters['search'] = search_text
        
        if filter_type != 'All':
            filters['filter_type'] = filter_type
        
        try:
            records = self.db.get_all_records(filters)
            self.display_records(records)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to filter records: {str(e)}")
    
    def display_records(self, records):
        """Populate table with records"""
        self.table.setRowCount(0)
        
        for row, record in enumerate(records):
            self.table.insertRow(row)
            
            # Control Number
            control_item = QTableWidgetItem(record['control_number'])
            self.table.setItem(row, 0, control_item)
            
            # School/University
            school_item = QTableWidgetItem(record['school_name'])
            self.table.setItem(row, 1, school_item)
            
            # Course
            course_item = QTableWidgetItem(record['course'])
            self.table.setItem(row, 2, course_item)
            
            # Hours
            hours_item = QTableWidgetItem(str(record['number_of_hours']))
            hours_item.setTextAlignment(Qt.AlignCenter)
            self.table.setItem(row, 3, hours_item)
            
            # Date Received
            date_item = QTableWidgetItem(str(record['date_received']))
            self.table.setItem(row, 4, date_item)
            
            # LO Status
            lo_status = 'Yes' if record['legal_opinion'] else 'Missing'
            lo_item = QTableWidgetItem(lo_status)
            lo_item.setTextAlignment(Qt.AlignCenter)
            if record['legal_opinion']:
                lo_item.setBackground(QBrush(QColor('#27ae60')))
                lo_item.setForeground(QBrush(QColor('white')))
            else:
                lo_item.setBackground(QBrush(QColor('#e67e22')))
                lo_item.setForeground(QBrush(QColor('white')))
            self.table.setItem(row, 5, lo_item)
            
            # MOA Status
            moa_status = 'Yes' if record['moa_available'] else 'Missing'
            moa_item = QTableWidgetItem(moa_status)
            moa_item.setTextAlignment(Qt.AlignCenter)
            if record['moa_available']:
                moa_item.setBackground(QBrush(QColor('#27ae60')))
                moa_item.setForeground(QBrush(QColor('white')))
            else:
                moa_item.setBackground(QBrush(QColor('#e74c3c')))
                moa_item.setForeground(QBrush(QColor('white')))
            self.table.setItem(row, 6, moa_item)
            
            # Workflow Stage
            workflow_item = QTableWidgetItem(record['workflow_stage'])
            self.table.setItem(row, 7, workflow_item)
            
            # Status
            status = record['status']
            status_item = QTableWidgetItem(status)
            status_item.setTextAlignment(Qt.AlignCenter)
            if status == 'Completed':
                status_item.setBackground(QBrush(QColor('#27ae60')))
                status_item.setForeground(QBrush(QColor('white')))
            else:
                status_item.setBackground(QBrush(QColor('#f39c12')))
                status_item.setForeground(QBrush(QColor('white')))
            self.table.setItem(row, 8, status_item)
            
            # Store record ID in first item for reference
            control_item.record_id = record['id']
    
    def get_selected_record_id(self) -> int:
        """Get selected record ID"""
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "No Selection", "Please select a record")
            return None
        
        control_item = self.table.item(current_row, 0)
        return control_item.record_id
    
    def view_record(self):
        """View selected record"""
        record_id = self.get_selected_record_id()
        if not record_id:
            return
        
        try:
            record_data = self.db.get_record(record_id)
            if not record_data:
                QMessageBox.warning(self, "Error", "Record not found")
                return
            
            record = Record.from_dict(record_data)
            
            # Build information text
            info_text = f"""
Control Number: {record.control_number}
School/University: {record.school_name}
Course: {record.course}
Number of Hours: {record.number_of_hours}
Date Received: {record.date_received}

Legal Opinion Section:
  Date: {record.date_lo or 'N/A'}
  Available: {'Yes' if record.legal_opinion else 'No'}
  Scanned: {'Yes' if record.lo_scanned else 'No'}
  File: {record.lo_file or 'None'}

MOA Section:
  Date: {record.date_moa or 'N/A'}
  Available: {'Yes' if record.moa_available else 'No'}
  Scanned: {'Yes' if record.moa_scanned else 'No'}
  File: {record.moa_file or 'None'}

Workflow Stage: {record.workflow_stage}
Status: {record.status}
Created: {record.created_at}
Updated: {record.updated_at}
            """
            
            QMessageBox.information(self, f"Record: {record.control_number}", info_text)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to view record: {str(e)}")
    
    def edit_record(self):
        """Edit selected record"""
        record_id = self.get_selected_record_id()
        if record_id:
            self.edit_record_signa.emit(record_id)
    
    def delete_record(self):
        """Delete selected record"""
        record_id = self.get_selected_record_id()
        if not record_id:
            return
        
        reply = QMessageBox.question(
            self, 'Confirm Delete',
            'Are you sure you want to delete this record?',
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            try:
                record_data = self.db.get_record(record_id)
                
                # Delete associated files
                if record_data['lo_file']:
                    FileHandler.delete_file(record_data['lo_file'])
                if record_data['moa_file']:
                    FileHandler.delete_file(record_data['moa_file'])
                
                # Delete record
                if self.db.delete_record(record_id):
                    QMessageBox.information(self, "Success", "Record deleted successfully")
                    self.load_records()
                else:
                    QMessageBox.warning(self, "Error", "Failed to delete record")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to delete record: {str(e)}")
