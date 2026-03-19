"""
View Records Page
Displays all records in a clean table with search/filter, rows are clickable
"""
from qt_compat import QtCore, QtGui, QtWidgets
from components.table_widget import TableContainer
from components.record_view import RecordViewComponent
from database import Database
from models import Record

class ViewRecordsPage(QtWidgets.QWidget):
    """Page for viewing and managing records"""
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.record_views_cache = {}  # Cache for opened record views (embedded)
        self.current_record_id = None
        self.init_ui()
        self.load_records()
    
    def init_ui(self):
        """Initialize page UI"""
        # Modern master-detail layout (table + details drawer)
        root_layout = QtWidgets.QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.setSpacing(0)

        self.splitter = QtWidgets.QSplitter(QtCore.Qt.Horizontal)
        self.splitter.setChildrenCollapsible(False)
        root_layout.addWidget(self.splitter, 1)

        # ============== LEFT (TABLE) ==============
        left = QtWidgets.QWidget()
        left_layout = QtWidgets.QVBoxLayout(left)
        left_layout.setContentsMargins(20, 20, 20, 20)
        left_layout.setSpacing(14)
        
        # Page Title
        title = QtWidgets.QLabel("All Records")
        title_font = QtGui.QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a1a1a;")
        left_layout.addWidget(title)
        
        subtitle = QtWidgets.QLabel("Click on any row to view record details")
        subtitle_font = QtGui.QFont()
        subtitle_font.setPointSize(9)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #999; margin-top: -10px;")
        left_layout.addWidget(subtitle)

        # Bulk actions (checkbox multi-select)
        actions_layout = QtWidgets.QHBoxLayout()
        actions_layout.setSpacing(10)

        self.select_all_checkbox = QtWidgets.QCheckBox("Select All")
        self.select_all_checkbox.stateChanged.connect(self.on_select_all_changed)

        self.pin_selected_btn = QtWidgets.QPushButton("📌 Pin Selected")
        self.unpin_selected_btn = QtWidgets.QPushButton("📌 Unpin Selected")
        self.delete_selected_btn = QtWidgets.QPushButton("🗑️ Delete Selected")

        self.pin_selected_btn.clicked.connect(lambda: self.set_pinned_for_selected(True))
        self.unpin_selected_btn.clicked.connect(lambda: self.set_pinned_for_selected(False))
        self.delete_selected_btn.clicked.connect(self.delete_selected_records)

        actions_layout.addWidget(self.select_all_checkbox)
        actions_layout.addSpacing(10)
        actions_layout.addWidget(self.pin_selected_btn)
        actions_layout.addWidget(self.unpin_selected_btn)
        actions_layout.addStretch()
        actions_layout.addWidget(self.delete_selected_btn)

        left_layout.addLayout(actions_layout)
        
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
        self.table_container.table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        # Selection is via checkboxes; keep single selection for row highlight only
        self.table_container.table.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.table_container.table.cellClicked.connect(self.on_row_clicked)
        self.table_container.table.itemDoubleClicked.connect(self.on_row_double_clicked)

        # Make checkbox column narrow
        self.table_container.table.setColumnWidth(0, 40)
        
        left_layout.addWidget(self.table_container, 1)

        # ============== RIGHT (DETAILS) ==============
        self.details_container = QtWidgets.QWidget()
        self.details_container.setMinimumWidth(420)
        details_layout = QtWidgets.QVBoxLayout(self.details_container)
        details_layout.setContentsMargins(16, 16, 16, 16)
        details_layout.setSpacing(10)

        details_header = QtWidgets.QHBoxLayout()
        self.details_title = QtWidgets.QLabel("Record details")
        dt_font = QtGui.QFont()
        dt_font.setPointSize(12)
        dt_font.setBold(True)
        self.details_title.setFont(dt_font)
        details_header.addWidget(self.details_title)
        details_header.addStretch()

        self.close_details_btn = QtWidgets.QPushButton("✕")
        self.close_details_btn.setFixedSize(32, 32)
        self.close_details_btn.clicked.connect(self.close_details)
        details_header.addWidget(self.close_details_btn)
        details_layout.addLayout(details_header)

        self.details_stack = QtWidgets.QStackedWidget()
        details_layout.addWidget(self.details_stack, 1)

        # Empty state
        empty = QtWidgets.QWidget()
        empty_layout = QtWidgets.QVBoxLayout(empty)
        empty_layout.addStretch()
        empty_title = QtWidgets.QLabel("Select a record")
        empty_title_font = QtGui.QFont()
        empty_title_font.setPointSize(14)
        empty_title_font.setBold(True)
        empty_title.setFont(empty_title_font)
        empty_title.setAlignment(QtCore.Qt.AlignCenter)
        empty_sub = QtWidgets.QLabel("Pick a row from the table to view details here.")
        empty_sub.setAlignment(QtCore.Qt.AlignCenter)
        empty_sub.setStyleSheet("color: #777;")
        empty_layout.addWidget(empty_title)
        empty_layout.addWidget(empty_sub)
        empty_layout.addStretch()
        self.details_stack.addWidget(empty)

        # Add panes to splitter
        self.splitter.addWidget(left)
        self.splitter.addWidget(self.details_container)
        self.splitter.setStretchFactor(0, 3)
        self.splitter.setStretchFactor(1, 2)

        # Start with details hidden (collapsed)
        self.close_details()

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
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to load records: {str(e)}")
    
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
            QtWidgets.QMessageBox.critical(self, "Error", f"Failed to filter records: {str(e)}")
    
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
            select_item = QtWidgets.QTableWidgetItem("")
            select_item.setFlags(QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsUserCheckable)
            select_item.setCheckState(QtCore.Qt.Unchecked)
            self.table_container.table.setItem(row, 0, select_item)
            
            # LO Status (Column 5)
            lo_item = self.table_container.table.item(row, 6)
            if record['legal_opinion']:
                lo_item.setBackground(QtGui.QBrush(QtGui.QColor("#dcfce7")))
                lo_item.setForeground(QtGui.QBrush(QtGui.QColor("#166534")))
            else:
                lo_item.setBackground(QtGui.QBrush(QtGui.QColor("#fecaca")))
                lo_item.setForeground(QtGui.QBrush(QtGui.QColor("#991b1b")))
            
            # MOA Status (Column 6)
            moa_item = self.table_container.table.item(row, 7)
            if record['moa_available']:
                moa_item.setBackground(QtGui.QBrush(QtGui.QColor("#dcfce7")))
                moa_item.setForeground(QtGui.QBrush(QtGui.QColor("#166534")))
            else:
                moa_item.setBackground(QtGui.QBrush(QtGui.QColor("#fecaca")))
                moa_item.setForeground(QtGui.QBrush(QtGui.QColor("#991b1b")))
            
            # Status column (Column 8)
            status_item = self.table_container.table.item(row, 9)
            if record['status'] == 'Completed':
                status_item.setBackground(QtGui.QBrush(QtGui.QColor("#dcfce7")))
                status_item.setForeground(QtGui.QBrush(QtGui.QColor("#166534")))
            else:
                status_item.setBackground(QtGui.QBrush(QtGui.QColor("#fef3c7")))
                status_item.setForeground(QtGui.QBrush(QtGui.QColor("#92400e")))
            
            # Store record ID on the Control # column item for reference (Column 1)
            self.table_container.table.item(row, 1).record_id = record['id']

    def get_checked_record_ids(self):
        """Get record IDs for rows where the checkbox is checked"""
        record_ids = []
        for row in range(self.table_container.table.rowCount()):
            select_item = self.table_container.table.item(row, 0)
            if not select_item or select_item.checkState() != QtCore.Qt.Checked:
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
        check = QtCore.Qt.Checked if state == QtCore.Qt.Checked else QtCore.Qt.Unchecked
        for row in range(self.table_container.table.rowCount()):
            item = self.table_container.table.item(row, 0)
            if item:
                item.setCheckState(check)

    def set_pinned_for_selected(self, pinned: bool):
        """Pin/unpin selected records"""
        record_ids = self.get_checked_record_ids()
        if not record_ids:
            QtWidgets.QMessageBox.information(self, "No selection", "Select one or more records first.")
            return

        if self.db.set_pinned(record_ids, pinned):
            self.load_records()
        else:
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to update pinned records.")

    def delete_selected_records(self):
        """Delete selected records (and their files)"""
        record_ids = self.get_checked_record_ids()
        if not record_ids:
            QtWidgets.QMessageBox.information(self, "No selection", "Select one or more records first.")
            return

        reply = QtWidgets.QMessageBox.question(
            self,
            "Delete Records",
            f"Delete {len(record_ids)} selected record(s)? This cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply != QtWidgets.QMessageBox.Yes:
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
            QtWidgets.QMessageBox.warning(self, "Error", "Failed to delete selected records.")
    
    def on_row_clicked(self, row: int, column: int):
        """Handle row click to show record detail"""
        # Clicking the checkbox column should not open the record
        if column == 0:
            return
        record_id = self.table_container.table.item(row, 1).record_id
        self.show_record_detail(record_id)
    
    def on_row_double_clicked(self, item: QtWidgets.QTableWidgetItem):
        """Handle row double-click to show record detail"""
        row = item.row()
        record_id = self.table_container.table.item(row, 1).record_id
        self.show_record_detail(record_id)
    
    def show_record_detail(self, record_id: int):
        """Show detailed view of a record"""
        self.current_record_id = record_id

        if record_id not in self.record_views_cache:
            record_view = RecordViewComponent(record_id, self.db, self, show_back=False)
            record_view.record_updated.connect(lambda _rid: self.load_records())
            self.record_views_cache[record_id] = record_view
            self.details_stack.addWidget(record_view)

        self.details_stack.setCurrentWidget(self.record_views_cache[record_id])
        self.open_details()
    
    def open_details(self):
        """Open the details drawer/panel"""
        # Ensure right pane visible
        total = max(1, self.width())
        left_w = int(total * 0.62)
        right_w = max(420, total - left_w)
        self.details_container.setVisible(True)
        self.splitter.setSizes([left_w, right_w])

    def close_details(self):
        """Close the details drawer/panel"""
        self.current_record_id = None
        self.details_stack.setCurrentIndex(0)
        # Collapse right pane
        total = max(1, self.width())
        self.details_container.setVisible(False)
        self.splitter.setSizes([total, 0])

