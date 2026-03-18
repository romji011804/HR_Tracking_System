"""
Table Container Component
Styled container for displaying records in a table
"""
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QLineEdit, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QColor, QBrush

class TableContainer(QWidget):
    """Container for displaying records in a styled table"""
    
    # Signals
    search_changed = pyqtSignal(str)
    filter_changed = pyqtSignal(str)
    view_all_clicked = pyqtSignal()
    
    def __init__(self, title: str = "Records", show_filters: bool = True):
        super().__init__()
        self.title_text = title
        self.show_filters = show_filters
        self.columns = []  # Track column names
        self.init_ui()
    
    def init_ui(self):
        """Initialize table container UI"""
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)
        
        # Header section with title and button
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(20, 15, 20, 10)
        
        title_label = QLabel(self.title_text)
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.setStyleSheet("color: #1a1a1a;")
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        self.view_all_btn = QPushButton("View All Records")
        self.view_all_btn.setFixedWidth(140)
        self.view_all_btn.setFixedHeight(35)
        self.view_all_btn.setStyleSheet("""
            QPushButton {
                background-color: #6366f1;
                color: white;
                border: none;
                border-radius: 5px;
                font-weight: 500;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #4f46e5;
            }
            QPushButton:pressed {
                background-color: #4338ca;
            }
        """)
        self.view_all_btn.clicked.connect(self.view_all_clicked.emit)
        header_layout.addWidget(self.view_all_btn)
        
        # Container for header and table
        container = QWidget()
        container.setStyleSheet("""
            QWidget {
                background-color: white;
                border: 1px solid #e8e8e8;
                border-radius: 8px;
            }
        """)
        container_layout = QVBoxLayout()
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Add header to container
        container_layout.addLayout(header_layout)
        
        # Filter section (if enabled)
        if self.show_filters:
            filter_layout = QHBoxLayout()
            filter_layout.setContentsMargins(20, 10, 20, 15)
            filter_layout.setSpacing(10)
            
            # Search box
            search_label = QLabel("Search:")
            search_label.setStyleSheet("color: #666; font-size: 11px; font-weight: 500;")
            filter_layout.addWidget(search_label)
            
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("Search by Control #, School, or Course...")
            self.search_input.setFixedHeight(35)
            self.search_input.setStyleSheet("""
                QLineEdit {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 8px;
                    background-color: #f9f9f9;
                    color: #333;
                    font-size: 11px;
                }
                QLineEdit:focus {
                    border: 1px solid #6366f1;
                    background-color: white;
                }
            """)
            self.search_input.textChanged.connect(lambda text: self.search_changed.emit(text))
            filter_layout.addWidget(self.search_input, 1)
            
            # Filter dropdown
            filter_label = QLabel("Filter:")
            filter_label.setStyleSheet("color: #666; font-size: 11px; font-weight: 500;")
            filter_layout.addWidget(filter_label)
            
            self.filter_combo = QComboBox()
            self.filter_combo.addItems(["All", "Ongoing", "Completed", "Missing LO", "Missing MOA"])
            self.filter_combo.setFixedWidth(150)
            self.filter_combo.setFixedHeight(35)
            self.filter_combo.setStyleSheet("""
                QComboBox {
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    padding: 8px;
                    background-color: #f9f9f9;
                    color: #333;
                    font-size: 11px;
                }
                QComboBox:focus {
                    border: 1px solid #6366f1;
                }
                QComboBox::drop-down {
                    border: none;
                }
            """)
            self.filter_combo.currentTextChanged.connect(lambda text: self.filter_changed.emit(text))
            filter_layout.addWidget(self.filter_combo)
            
            container_layout.addLayout(filter_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(0)
        self.table.setRowCount(0)
        self.table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: white;
                alternate-background-color: #f9f9f9;
            }
            QTableWidget::item {
                padding: 8px;
                border-bottom: 1px solid #f0f0f0;
            }
            QTableWidget::item:selected {
                background-color: #e8eaf6;
            }
            QHeaderView::section {
                background-color: #f5f5f5;
                color: #666;
                padding: 8px;
                border: none;
                border-bottom: 1px solid #ddd;
                font-weight: 500;
                font-size: 11px;
            }
        """)
        self.table.horizontalHeader().setMinimumHeight(40)
        self.table.setAlternatingRowColors(True)
        container_layout.addWidget(self.table)
        
        container.setLayout(container_layout)
        main_layout.addWidget(container)
        
        self.setLayout(main_layout)
    
    def set_columns(self, columns: list):
        """Set table columns"""
        self.columns = columns
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels(columns)
    
    def add_row(self, data: list) -> int:
        """Add a row to the table - returns row index"""
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)
        
        for col, value in enumerate(data):
            item = QTableWidgetItem(str(value))
            item.setFlags(item.flags() & ~Qt.ItemIsEditable)
            self.table.setItem(row_position, col, item)
        
        return row_position
    
    def clear_table(self):
        """Clear all rows from table"""
        self.table.setRowCount(0)
    
    def get_search_text(self) -> str:
        """Get current search text"""
        return self.search_input.text() if self.show_filters else ""
    
    def get_filter_text(self) -> str:
        """Get current filter selection"""
        return self.filter_combo.currentText() if self.show_filters else "All"
