from __future__ import annotations

from typing import List

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Signal, Slot

from utils.recent_inputs import RecentInputsManager


class RecentInputsModel(QAbstractListModel):
    """
    Simple list model for QML autocomplete suggestions.
    Backed by `RecentInputsManager` (JSON persistence).
    """

    changed = Signal()

    Roles = {
        Qt.UserRole + 1: b"value",
    }

    def __init__(self, field_name: str):
        super().__init__()
        self._manager = RecentInputsManager(field_name)
        self._items: List[str] = self._manager.get_recent()

    def roleNames(self):
        return self.Roles

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._items)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        if role == Qt.UserRole + 1:
            return self._items[index.row()]
        return None

    @Slot()
    def reload(self):
        self.beginResetModel()
        self._items = self._manager.get_recent()
        self.endResetModel()
        self.changed.emit()

    @Slot(str)
    def addValue(self, value: str):
        value = (value or "").strip()
        if not value:
            return
        self._manager.add_input(value)
        self.reload()

    @Slot(str)
    def deleteValue(self, value: str):
        value = (value or "").strip()
        if not value:
            return
        self._manager.delete_input(value)
        self.reload()

    @Slot(result="QStringList")
    def values(self) -> List[str]:
        return list(self._items)

