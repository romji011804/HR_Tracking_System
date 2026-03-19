from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from PySide6.QtCore import QAbstractListModel, QModelIndex, Qt, Signal, Slot

from backend.services.records_service import RecordsService


@dataclass
class _RecordRow:
    id: int
    control_number: str
    school_name: str
    course: str
    number_of_hours: int
    date_received: str
    workflow_stage: str
    status: str
    pinned: bool
    legal_opinion: bool
    moa_available: bool
    lo_file: Optional[str]
    moa_file: Optional[str]


class RecordsModel(QAbstractListModel):
    """
    QML-friendly records list model.

    Use with ListView/Repeater. For a table, render each row as a delegate.
    """

    Roles = {
        Qt.UserRole + 1: b"id",
        Qt.UserRole + 2: b"controlNumber",
        Qt.UserRole + 3: b"schoolName",
        Qt.UserRole + 4: b"course",
        Qt.UserRole + 5: b"hours",
        Qt.UserRole + 6: b"dateReceived",
        Qt.UserRole + 7: b"workflowStage",
        Qt.UserRole + 8: b"status",
        Qt.UserRole + 9: b"pinned",
        Qt.UserRole + 10: b"legalOpinion",
        Qt.UserRole + 11: b"moaAvailable",
        Qt.UserRole + 12: b"loFile",
        Qt.UserRole + 13: b"moaFile",
        Qt.UserRole + 14: b"checked",
    }

    checkedChanged = Signal()

    def __init__(self, service: RecordsService):
        super().__init__()
        self._service = service
        self._rows: List[_RecordRow] = []
        self._checked: set[int] = set()
        self._filters: Dict[str, Any] = {}

        self._service.records_changed.connect(self.reload)
        self.reload()

    def roleNames(self):
        return self.Roles

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid():
            return 0
        return len(self._rows)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        row = self._rows[index.row()]

        if role == Qt.UserRole + 1:
            return row.id
        if role == Qt.UserRole + 2:
            return row.control_number
        if role == Qt.UserRole + 3:
            return row.school_name
        if role == Qt.UserRole + 4:
            return row.course
        if role == Qt.UserRole + 5:
            return row.number_of_hours
        if role == Qt.UserRole + 6:
            return row.date_received
        if role == Qt.UserRole + 7:
            return row.workflow_stage
        if role == Qt.UserRole + 8:
            return row.status
        if role == Qt.UserRole + 9:
            return row.pinned
        if role == Qt.UserRole + 10:
            return row.legal_opinion
        if role == Qt.UserRole + 11:
            return row.moa_available
        if role == Qt.UserRole + 12:
            return row.lo_file
        if role == Qt.UserRole + 13:
            return row.moa_file
        if role == Qt.UserRole + 14:
            return row.id in self._checked

        return None

    @Slot()
    def reload(self):
        records = self._service.get_records(self._filters)
        rows: List[_RecordRow] = []
        for rec in records:
            rows.append(
                _RecordRow(
                    id=int(rec["id"]),
                    control_number=str(rec.get("control_number") or ""),
                    school_name=str(rec.get("school_name") or ""),
                    course=str(rec.get("course") or ""),
                    number_of_hours=int(rec.get("number_of_hours") or 0),
                    date_received=str(rec.get("date_received") or ""),
                    workflow_stage=str(rec.get("workflow_stage") or ""),
                    status=str(rec.get("status") or ""),
                    pinned=bool(rec.get("pinned") or 0),
                    legal_opinion=bool(rec.get("legal_opinion") or 0),
                    moa_available=bool(rec.get("moa_available") or 0),
                    lo_file=rec.get("lo_file"),
                    moa_file=rec.get("moa_file"),
                )
            )

        self.beginResetModel()
        self._rows = rows
        # Prune checked ids that no longer exist
        existing = {r.id for r in rows}
        self._checked = {rid for rid in self._checked if rid in existing}
        self.endResetModel()
        self.checkedChanged.emit()

    @Slot(str)
    def setSearch(self, text: str):
        text = (text or "").strip()
        if text:
            self._filters["search"] = text
        else:
            self._filters.pop("search", None)
        self.reload()

    @Slot(str)
    def setFilterType(self, filter_type: str):
        filter_type = (filter_type or "").strip()
        if filter_type and filter_type != "All":
            self._filters["filter_type"] = filter_type
        else:
            self._filters.pop("filter_type", None)
        self.reload()

    @Slot(int)
    def toggleChecked(self, record_id: int):
        rid = int(record_id)
        if rid in self._checked:
            self._checked.remove(rid)
        else:
            self._checked.add(rid)
        self.checkedChanged.emit()
        # Notify views: easiest is to refresh whole model data for checked role
        self.dataChanged.emit(self.index(0, 0), self.index(max(0, self.rowCount() - 1), 0), [Qt.UserRole + 14])

    @Slot(bool)
    def setAllChecked(self, checked: bool):
        if checked:
            self._checked = {r.id for r in self._rows}
        else:
            self._checked.clear()
        self.checkedChanged.emit()
        self.dataChanged.emit(self.index(0, 0), self.index(max(0, self.rowCount() - 1), 0), [Qt.UserRole + 14])

    @Slot(result="QVariantList")
    def checkedIds(self) -> List[int]:
        return list(self._checked)

