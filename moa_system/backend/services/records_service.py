from __future__ import annotations

from typing import Any, Dict, List, Optional

from PySide6.QtCore import QObject, Signal, Slot

from database import Database
from utils.control_number_generator import generate_control_number
from utils.file_handler import FileHandler


class RecordsService(QObject):
    """
    Thin wrapper around `Database` to expose record operations to QML.
    """

    records_changed = Signal()

    def __init__(self, db: Database):
        super().__init__()
        self._db = db

    def get_records(self, filters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        return self._db.get_all_records(filters or {})

    def get_record(self, record_id: int) -> Optional[Dict[str, Any]]:
        return self._db.get_record(record_id)

    @Slot("QVariantMap", result=int)
    def add_record(self, data: Dict[str, Any]) -> int:
        # Ensure control number exists for new records
        if not data.get("control_number"):
            data["control_number"] = generate_control_number(self._db)
        record_id = self._db.add_record(data)
        self.records_changed.emit()
        return record_id

    @Slot(int, "QVariantMap", result=bool)
    def update_record(self, record_id: int, data: Dict[str, Any]) -> bool:
        ok = self._db.update_record(record_id, data)
        if ok:
            self.records_changed.emit()
        return ok

    @Slot("QVariantList", result=bool)
    def delete_records(self, record_ids: List[int]) -> bool:
        ok = self._db.delete_records(list(record_ids))
        if ok:
            self.records_changed.emit()
        return ok

    @Slot("QVariantList", bool, result=bool)
    def set_pinned(self, record_ids: List[int], pinned: bool) -> bool:
        ok = self._db.set_pinned(list(record_ids), pinned)
        if ok:
            self.records_changed.emit()
        return ok

    @Slot(result="QVariantMap")
    def get_dashboard_stats(self) -> Dict[str, Any]:
        return self._db.get_dashboard_stats()

    @Slot(result=str)
    def next_control_number(self) -> str:
        return generate_control_number(self._db)

    @Slot(str, str, str, result=str)
    def upload_pdf(self, source_path: str, file_type: str, control_number: str) -> str:
        """
        Upload a PDF to uploads/ and return stored relative path.
        file_type: 'lo' or 'moa'
        """
        if not source_path:
            return ""
        stored = FileHandler.upload_file(source_path, file_type, control_number)
        return stored or ""

