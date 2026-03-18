"""
View Records Page
Displays all records in a clean table with search/filter, rows are clickable
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox,
    QTableWidgetItem, QAbstractItemView, QLabel, QStackedWidget, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QBrush
from components.table_widget import TableContainer
from components.record_view import RecordViewComponent
from database import Database
from models import Record

class ViewRecordsPage(QWidget):
    """Page for viewing and managing records"""
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.record_views_cache = {}  # Cache for opened record views
        self.init_ui()
        self.load_records()
    
    def init_ui(self):
        """Initialize page UI"""
        # Use QStackedWidget to manage table and record views
        self.stacked_widget = QStackedWidget()
        
        # Create main table view
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Page Title
        title = QLabel("All Records")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a1a1a;")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Click on any row to view record details")
        subtitle_font = QFont()
        subtitle_font.setPointSize(9)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #999; margin-top: -10px;")
        main_layout.addWidget(subtitle)

        # Bulk actions (checkbox multi-select)
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(10)

        self.select_all_checkbox = QCheckBox("Select All")
        self.select_all_checkbox.stateChanged.connect(self.on_select_all_changed)

        self.pin_selected_btn = QPushButton("📌 Pin Selected")
        self.unpin_selected_btn = QPushButton("📌 Unpin Selected")
        self.delete_selected_btn = QPushButton("🗑️ Delete Selected")

        self.pin_selected_btn.clicked.connect(lambda: self.set_pinned_for_selected(True))
        self.unpin_selected_btn.clicked.connect(lambda: self.set_pinned_for_selected(False))
        self.delete_selected_btn.clicked.connect(self.delete_selected_records)

        actions_layout.addWidget(self.select_all_checkbox)
        actions_layout.addSpacing(10)
        actions_layout.addWidget(self.pin_selected_btn)
        actions_layout.addWidget(self.unpin_selected_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(self.delete_selected_btn)

        main_layout.addLayout(actions_layout)
        
        # Table Container (without buttons)
        self.table_container = TableContainer("Records", show_filters=True)
        self.table_container.search_changed.connect(self.apply_filters)
        self.table_container.filter_changed.connect(self.apply_filters)
        
        # Remove the "View All Records" button from table container
        self.table_container.view_all_btn.hide()
        
        # Set columns (NO Actions column!)
        columns = ["", "Control #", "School/University", "Course", "Hours",
                   "Date Received", "LO", "MOA", "Workflow", "Status"]
        self.table_container.set_columns(columns)
        
        # Make table selectable and clickable
        self.table_container.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # Selection is via checkboxes; keep single selection for row highlight only
        self.table_container.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table_container.table.cellClicked.connect(self.on_row_clicked)
        self.table_container.table.itemDoubleClicked.connect(self.on_row_double_clicked)

        # Make checkbox column narrow
        self.table_container.table.setColumnWidth(0, 40)
        
        main_layout.addWidget(self.table_container)
        
        # Add main widget to stacked widget
        self.stacked_widget.addWidget(self.main_widget)
        
        # Set page layout
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)
        page_layout.addWidget(self.stacked_widget)
        
        self.setLayout(page_layout)
        self.setStyleSheet("""
            ViewRecordsPage {
                background-color: #f5f5f5;
            }
        """)
    
    def load_records(self):
        """Load all records from database"""
        try:
            records = self.db.get_all_records()
            self.display_records(records)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load records: {str(e)}")
    
    def apply_filters(self):
        """Apply search and filter to records"""
        search_text = self.table_container.get_search_text()
        filter_type = self.table_container.get_filter_text()
        
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
        self.table_container.clear_table()
        # Reset select-all checkbox state when reloading
        self.select_all_checkbox.blockSignals(True)
        self.select_all_checkbox.setChecked(False)
        self.select_all_checkbox.blockSignals(False)
        
        for record in records:
            lo_status = "✓" if record['legal_opinion'] else "✗"
            moa_status = "✓" if record['moa_available'] else "✗"

            # Visual pin indicator without changing the column layout
            control_number_display = record['control_number']
            if record.get("pinned"):
                control_number_display = f"★ {control_number_display}"
            
            row_data = [
                "",  # checkbox column placeholder
                control_number_display,
                record['school_name'],
                record['course'],
                str(record['number_of_hours']),
                str(record['date_received']),
                lo_status,
                moa_status,
                record['workflow_stage'],
                record['status']
            ]
            
            self.table_container.add_row(row_data)
            
            # Color code the status cells
            row = self.table_container.table.rowCount() - 1

            # Add checkbox item (Column 0)
            select_item = QTableWidgetItem("")
            select_item.setFlags(Qt.ItemIsEnabled | Qt.ItemIsUserCheckable)
            select_item.setCheckState(Qt.Unchecked)
            self.table_container.table.setItem(row, 0, select_item)
            
            # LO Status (Column 5)
            lo_item = self.table_container.table.item(row, 6)
            if record['legal_opinion']:
                lo_item.setBackground(QBrush(QColor("#dcfce7")))
                lo_item.setForeground(QBrush(QColor("#166534")))
            else:
                lo_item.setBackground(QBrush(QColor("#fecaca")))
                lo_item.setForeground(QBrush(QColor("#991b1b")))
            
            # MOA Status (Column 6)
            moa_item = self.table_container.table.item(row, 7)
            if record['moa_available']:
                moa_item.setBackground(QBrush(QColor("#dcfce7")))
                moa_item.setForeground(QBrush(QColor("#166534")))
            else:
                moa_item.setBackground(QBrush(QColor("#fecaca")))
                moa_item.setForeground(QBrush(QColor("#991b1b")))
            
            # Status column (Column 8)
            status_item = self.table_container.table.item(row, 9)
            if record['status'] == 'Completed':
                status_item.setBackground(QBrush(QColor("#dcfce7")))
                status_item.setForeground(QBrush(QColor("#166534")))
            else:
                status_item.setBackground(QBrush(QColor("#fef3c7")))
                status_item.setForeground(QBrush(QColor("#92400e")))
            
            # Store record ID on the Control # column item for reference (Column 1)
            self.table_container.table.item(row, 1).record_id = record['id']

    def get_checked_record_ids(self):
        """Get record IDs for rows where the checkbox is checked"""
        record_ids = []
        for row in range(self.table_container.table.rowCount()):
            select_item = self.table_container.table.item(row, 0)
            if not select_item or select_item.checkState() != Qt.Checked:
                continue
            control_item = self.table_container.table.item(row, 1)
            rid = getattr(control_item, "record_id", None) if control_item else None
            if rid is not None:
                record_ids.append(rid)
        # Deduplicate while preserving order
        seen = set()
        unique = []
        for rid in record_ids:
            if rid not in seen:
                seen.add(rid)
                unique.append(rid)
        return unique

    def on_select_all_changed(self, state: int):
        """Check/uncheck all row checkboxes"""
        check = Qt.Checked if state == Qt.Checked else Qt.Unchecked
        for row in range(self.table_container.table.rowCount()):
            item = self.table_container.table.item(row, 0)
            if item:
                item.setCheckState(check)

    def set_pinned_for_selected(self, pinned: bool):
        """Pin/unpin selected records"""
        record_ids = self.get_checked_record_ids()
        if not record_ids:
            QMessageBox.information(self, "No selection", "Select one or more records first.")
            return

        if self.db.set_pinned(record_ids, pinned):
            self.load_records()
        else:
            QMessageBox.warning(self, "Error", "Failed to update pinned records.")

    def delete_selected_records(self):
        """Delete selected records (and their files)"""
        record_ids = self.get_checked_record_ids()
        if not record_ids:
            QMessageBox.information(self, "No selection", "Select one or more records first.")
            return

        reply = QMessageBox.question(
            self,
            "Delete Records",
            f"Delete {len(record_ids)} selected record(s)? This cannot be undone.",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        # Delete associated files before deleting DB rows
        from utils.file_handler import FileHandler
        for rid in record_ids:
            rec = self.db.get_record(rid)
            if not rec:
                continue
            if rec.get("lo_file"):
                FileHandler.delete_file(rec.get("lo_file"))
            if rec.get("moa_file"):
                FileHandler.delete_file(rec.get("moa_file"))

        if self.db.delete_records(record_ids):
            self.load_records()
        else:
            QMessageBox.warning(self, "Error", "Failed to delete selected records.")
    
    def on_row_clicked(self, row: int, column: int):
        """Handle row click to show record detail"""
        # Clicking the checkbox column should not open the record
        if column == 0:
            return
        record_id = self.table_container.table.item(row, 1).record_id
        self.show_record_detail(record_id)
    
    def on_row_double_clicked(self, item: QTableWidgetItem):
        """Handle row double-click to show record detail"""
        row = item.row()
        record_id = self.table_container.table.item(row, 1).record_id
        self.show_record_detail(record_id)
    
    def show_record_detail(self, record_id: int):
        """Show detailed view of a record"""
        # Check if we already have this record view cached
        if record_id not in self.record_views_cache:
            # Create new record view
            record_view = RecordViewComponent(record_id, self.db, self)
            record_view.back_clicked.connect(self.show_table_view)
            self.record_views_cache[record_id] = record_view
            self.stacked_widget.addWidget(record_view)
        
        # Switch to the record view
        record_view = self.record_views_cache[record_id]
        self.stacked_widget.setCurrentWidget(record_view)
    
    def show_table_view(self):
        """Return to table view"""
        # Just switch back to the main widget
        self.stacked_widget.setCurrentWidget(self.main_widget)
        # Refresh records in case any were deleted
        self.load_records()

