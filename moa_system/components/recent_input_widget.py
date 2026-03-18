"""
Recent Input Dropdown Widget
Modern searchable dropdown with recent history and delete button
Similar to TikTok search bar
"""
from PyQt5.QtWidgets import (
    QWidget, QHBoxLayout, QLineEdit, QPushButton, QCompleter, 
    QComboBox, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont
from utils.recent_inputs import RecentInputsManager


class RecentInputComboBox(QWidget):
    """
    Combo box with recent inputs, search, and delete functionality
    Shows recent items as autocomplete suggestions
    """
    
    # Signal emitted when text changes
    textChanged = pyqtSignal(str)
    
    def __init__(self, field_name: str, parent=None):
        """
        Initialize recent input combo box
        
        Args:
            field_name: Name of the field (e.g., "school", "course")
            parent: Parent widget
        """
        super().__init__(parent)
        self.field_name = field_name
        self.recent_manager = RecentInputsManager(field_name)
        self.init_ui()
    
    def init_ui(self):
        """Initialize UI"""
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(5)
        
        # Input field with autocomplete
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText(f"Type {self.field_name}...")
        self.input_field.textChanged.connect(self.on_text_changed)
        self.input_field.returnPressed.connect(self.on_input_finished)
        
        # Set up autocomplete with recent inputs
        self.update_autocomplete()
        
        # Delete button (small X button)
        self.delete_btn = QPushButton("✕")
        self.delete_btn.setFixedWidth(35)
        self.delete_btn.setFixedHeight(35)
        self.delete_btn.setToolTip(f"Remove '{self.input_field.text()}' from recent {self.field_name}")
        self.delete_btn.clicked.connect(self.delete_current)
        self.delete_btn.setStyleSheet("""
            QPushButton {
                background-color: #f3f4f6;
                border: 1px solid #d1d5db;
                border-radius: 4px;
                color: #6b7280;
                font-weight: bold;
                padding: 0px;
            }
            QPushButton:hover {
                background-color: #fee2e2;
                border: 1px solid #fca5a5;
                color: #dc2626;
            }
        """)
        
        layout.addWidget(self.input_field, 1)
        layout.addWidget(self.delete_btn)
        
        self.setLayout(layout)
    
    def update_autocomplete(self):
        """Update autocomplete suggestions from recent inputs"""
        recent = self.recent_manager.get_recent()
        
        if recent:
            completer = QCompleter(recent)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
            completer.setCompletionMode(QCompleter.PopupCompletion)
            # Match typed text anywhere in the string, not just prefix
            completer.setFilterMode(Qt.MatchContains)
            self.input_field.setCompleter(completer)
    
    def on_text_changed(self):
        """Handle text change"""
        self.textChanged.emit(self.input_field.text())
    
    def on_input_finished(self):
        """Handle when user finishes input (presses Enter)"""
        text = self.input_field.text().strip()
        if text:
            # Add to recent history
            self.recent_manager.add_input(text)
            # Update autocomplete
            self.update_autocomplete()
    
    def delete_current(self):
        """Delete current text from recent history"""
        text = self.input_field.text().strip()
        if text:
            self.recent_manager.delete_input(text)
            # Update autocomplete
            self.update_autocomplete()
            print(f"[DEBUG] Deleted '{text}' from recent {self.field_name}")
    
    def setText(self, text: str):
        """Set the text in the input field"""
        self.input_field.setText(text)
    
    def text(self) -> str:
        """Get the text from the input field"""
        return self.input_field.text()
    
    def setEditText(self, text: str):
        """Set text (for compatibility with QComboBox)"""
        self.setText(text)
    
    def setEditable(self, editable: bool):
        """Set editable (for compatibility with QComboBox)"""
        self.input_field.setReadOnly(not editable)
    
    def setPlaceholderText(self, text: str):
        """Set placeholder text"""
        self.input_field.setPlaceholderText(text)
    
    def setFocus(self):
        """Set focus to input field"""
        self.input_field.setFocus()
    
    def clear(self):
        """Clear the input field"""
        self.input_field.clear()
