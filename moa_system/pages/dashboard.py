"""
Dashboard Page
Displays statistics and recent records
"""
from qt_compat import QtCore, QtGui, QtWidgets, Signal
from components.card_widget import CardWidget
from components.table_widget import TableContainer
from components.record_view import RecordViewComponent
from database import Database

Qt = QtCore.Qt
QFont = QtGui.QFont
QColor = QtGui.QColor

QWidget = QtWidgets.QWidget
QVBoxLayout = QtWidgets.QVBoxLayout
QHBoxLayout = QtWidgets.QHBoxLayout
QLabel = QtWidgets.QLabel
QGridLayout = QtWidgets.QGridLayout
QTableWidgetItem = QtWidgets.QTableWidgetItem
QStackedWidget = QtWidgets.QStackedWidget


class DashboardPage(QWidget):
    """Dashboard page with statistics and recent records"""
    
    view_records_requested = Signal()  # Signal to navigate to View Records page
    
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.record_views_cache = {}  # Cache for opened record views
        self.init_ui()
        self.load_statistics()
    
    def init_ui(self):
        """Initialize dashboard UI"""
        # Use QStackedWidget to manage dashboard and record views
        self.stacked_widget = QStackedWidget()
        
        # Create main dashboard view
        self.main_widget = QWidget()
        main_layout = QVBoxLayout(self.main_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Page Title
        title = QLabel("Dashboard Statistics")
        title_font = QFont()
        title_font.setPointSize(18)
        title_font.setBold(True)
        title.setFont(title_font)
        title.setStyleSheet("color: #1a1a1a;")
        main_layout.addWidget(title)
        
        subtitle = QLabel("Memorandum of Agreement and Legal Opinion Overview")
        subtitle_font = QFont()
        subtitle_font.setPointSize(10)
        subtitle.setFont(subtitle_font)
        subtitle.setStyleSheet("color: #999; margin-top: -10px;")
        main_layout.addWidget(subtitle)
        
        # Statistics Grid
        stats_grid = QGridLayout()
        stats_grid.setSpacing(15)
        
        self.total_card = CardWidget("Total Records", "0", "👥", "#ffffff")
        self.ongoing_card = CardWidget("Ongoing Records", "0", "⏳", "#ffffff")
        self.completed_card = CardWidget("Completed Records", "0", "✓", "#ffffff")
        
        stats_grid.addWidget(self.total_card, 0, 0)
        stats_grid.addWidget(self.ongoing_card, 0, 1)
        stats_grid.addWidget(self.completed_card, 0, 2)
        
        self.missing_lo_card = CardWidget("Missing Legal Opinion", "0", "⚠️", "#ffffff")
        self.missing_moa_card = CardWidget("Missing Memorandum of Agreement", "0", "⚠️", "#ffffff")
        
        stats_grid.addWidget(self.missing_lo_card, 1, 0)
        stats_grid.addWidget(self.missing_moa_card, 1, 1)
        
        main_layout.addLayout(stats_grid)
        
        # Recent Records Table
        self.table_container = TableContainer("Records", show_filters=False)
        self.table_container.view_all_clicked.connect(self.on_view_all_clicked)
        
        # Set table columns
        columns = ["Control #", "School/University", "Course", "Status", "Workflow"]
        self.table_container.set_columns(columns)
        
        # Connect row click to show record detail
        self.table_container.table.cellClicked.connect(self.on_table_row_clicked)
        
        main_layout.addWidget(self.table_container)
        
        main_layout.addStretch()
        
        # Add main widget to stacked widget
        self.stacked_widget.addWidget(self.main_widget)
        
        # Set main layout
        page_layout = QVBoxLayout(self)
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(0)
        page_layout.addWidget(self.stacked_widget)
        
        self.setLayout(page_layout)
        self.setStyleSheet("""
            DashboardPage {
                background-color: #ffffff;
            }
        """)
    
    def load_statistics(self):
        """Load statistics from database"""
        try:
            stats = self.db.get_dashboard_stats()
            
            self.total_card.set_value(str(stats['total']))
            self.ongoing_card.set_value(str(stats['ongoing']))
            self.completed_card.set_value(str(stats['completed']))
            self.missing_lo_card.set_value(str(stats['missing_lo']))
            self.missing_moa_card.set_value(str(stats['missing_moa']))
            
            # Load recent records
            self.load_recent_records()
            
        except Exception as e:
            print(f"Error loading statistics: {e}")
    
    def load_recent_records(self):
        """Load recent records for display"""
        try:
            records = self.db.get_all_records()
            self.table_container.clear_table()

            # Show last 5 records only
            for record in records[:5]:
                control_number_display = record['control_number']
                if record.get("pinned"):
                    control_number_display = f"★ {control_number_display}"
                row_data = [
                    control_number_display,
                    record['school_name'],
                    record['course'],
                    record['status'],
                    record['workflow_stage']
                ]
                row_index = self.table_container.add_row(row_data)

                # Store record_id in the first column item for later retrieval
                if row_index >= 0:
                    control_item = self.table_container.table.item(row_index, 0)
                    if control_item is not None:
                        control_item.record_id = record['id']
            
        except Exception as e:
            print(f"Error loading records: {e}")
    
    def on_table_row_clicked(self, row: int, column: int):
        """Handle table row click to show record detail"""
        try:
            # Prefer record_id stored on the first column item
            first_item = self.table_container.table.item(row, 0)
            if not first_item:
                return

            record_id = getattr(first_item, "record_id", None)

            if record_id is not None:
                self.show_record_detail(record_id)
                return

            # Fallback: match by control number if record_id is missing
            control_number = first_item.text()
            if control_number:
                records = self.db.get_all_records()
                for record in records:
                    if record.get("control_number") == control_number:
                        self.show_record_detail(record["id"])
                        break
        except Exception as e:
            print(f"Error handling row click: {e}")
    
    def show_record_detail(self, record_id: int):
        """Show detailed view of a record"""
        # Check if we already have this record view cached
        if record_id not in self.record_views_cache:
            # Create new record view
            record_view = RecordViewComponent(record_id, self.db, self)
            record_view.back_clicked.connect(self.show_dashboard_view)
            self.record_views_cache[record_id] = record_view
            self.stacked_widget.addWidget(record_view)
        
        # Switch to the record view
        record_view = self.record_views_cache[record_id]
        self.stacked_widget.setCurrentWidget(record_view)
    
    def show_dashboard_view(self):
        """Return to dashboard view"""
        # Just switch back to the main widget
        self.stacked_widget.setCurrentWidget(self.main_widget)
        # Refresh statistics
        self.load_statistics()
    
    def on_view_all_clicked(self):
        """Handle view all records click - navigate to View Records page"""
        self.view_records_requested.emit()

