from __future__ import annotations

from PySide6.QtCore import QObject, Property, Signal, Slot


class ThemeService(QObject):
    themeChanged = Signal()

    def __init__(self):
        super().__init__()
        self._theme = "light"

    def getTheme(self) -> str:
        return self._theme

    @Slot(str)
    def setTheme(self, theme: str):
        theme = (theme or "").strip().lower()
        if theme not in ("light", "dark"):
            return
        if theme == self._theme:
            return
        self._theme = theme
        self.themeChanged.emit()

    @Slot()
    def toggle(self):
        self.setTheme("dark" if self._theme == "light" else "light")

    theme = Property(str, getTheme, setTheme, notify=themeChanged)

