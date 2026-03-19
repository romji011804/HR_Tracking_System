"""
Qt compatibility layer.

Goal: keep the codebase runnable while migrating from PyQt5 to PySide6.
Prefer PySide6 when available (Qt6), otherwise fall back to PyQt5 (Qt5).
"""

from __future__ import annotations

from typing import Any, Optional, Type

QT_API: str

try:  # Prefer Qt6
    from PySide6 import QtCore, QtGui, QtWidgets  # type: ignore

    Signal = QtCore.Signal
    Slot = QtCore.Slot
    Property = QtCore.Property

    def qapplication_exec(app: QtWidgets.QApplication) -> int:
        return app.exec()

    QT_API = "pyside6"
except Exception:  # Fall back to Qt5
    from PyQt5 import QtCore, QtGui, QtWidgets  # type: ignore

    Signal = QtCore.pyqtSignal
    Slot = QtCore.pyqtSlot
    Property = QtCore.pyqtProperty

    def qapplication_exec(app: QtWidgets.QApplication) -> int:
        return app.exec_()

    QT_API = "pyqt5"


def load_web_engine_view() -> tuple[bool, Optional[Type[Any]]]:
    """
    Optional WebEngine support for embedded PDF viewing.

    Returns (has_web_engine, QWebEngineViewClass)
    """
    try:
        if QT_API == "pyside6":
            from PySide6.QtWebEngineWidgets import QWebEngineView  # type: ignore
        else:
            from PyQt5.QtWebEngineWidgets import QWebEngineView  # type: ignore
        return True, QWebEngineView
    except Exception:
        return False, None


def load_qurl() -> Any:
    if QT_API == "pyside6":
        from PySide6.QtCore import QUrl  # type: ignore
    else:
        from PyQt5.QtCore import QUrl  # type: ignore
    return QUrl

