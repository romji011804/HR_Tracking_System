from __future__ import annotations

from typing import Optional

from PySide6.QtCore import QObject, Slot


class FileService(QObject):
    """
    File/link operations for QML.

    Uses existing utils where possible.
    """

    @Slot(str, result=bool)
    def openPathOrUrl(self, value: str) -> bool:
        # Reuse existing PyQt-based opener for now; it works on Windows via QDesktopServices.
        # During full cutover we can replace this with a pure Qt6 implementation.
        try:
            from utils.file_opener import open_file
            return bool(open_file(value))
        except Exception as e:
            print(f"[ERROR] openPathOrUrl failed: {e}")
            return False

