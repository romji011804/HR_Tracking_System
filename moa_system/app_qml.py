"""
Qt Quick (QML) entry point.

This runs alongside the existing widgets app (`main.py`) during migration.
"""
import os
import sys

from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from database import Database


def main() -> int:
    app = QApplication(sys.argv)

    # App icon (reuse existing)
    base_dir = os.path.dirname(os.path.abspath(__file__))
    icon_path = os.path.join(base_dir, "assets", "app_icon.png")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    db = Database()

    # Import backend bridge objects lazily (keeps startup simple)
    from backend.services.records_service import RecordsService
    from backend.services.file_service import FileService
    from backend.models.records_model import RecordsModel
    from backend.models.recent_inputs_model import RecentInputsModel
    from backend.theme.theme_service import ThemeService

    theme_service = ThemeService()
    records_service = RecordsService(db)
    file_service = FileService()
    records_model = RecordsModel(records_service)

    # Recent inputs (School/Course/Hours)
    recent_school = RecentInputsModel("school")
    recent_course = RecentInputsModel("course")
    recent_hours = RecentInputsModel("hours")

    engine = QQmlApplicationEngine()
    ctx = engine.rootContext()
    ctx.setContextProperty("themeService", theme_service)
    ctx.setContextProperty("recordsService", records_service)
    ctx.setContextProperty("fileService", file_service)
    ctx.setContextProperty("recordsModel", records_model)
    ctx.setContextProperty("recentSchoolModel", recent_school)
    ctx.setContextProperty("recentCourseModel", recent_course)
    ctx.setContextProperty("recentHoursModel", recent_hours)

    qml_path = os.path.join(base_dir, "qml", "Main.qml")
    engine.load(QUrl.fromLocalFile(qml_path))

    if not engine.rootObjects():
        return 1

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())

