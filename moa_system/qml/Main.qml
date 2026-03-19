import QtQuick 2.15
import QtQuick.Controls 6.5
import QtQuick.Layouts 1.15

ApplicationWindow {
    id: root
    visible: true
    width: 1400
    height: 800
    title: "MOA & Legal Opinion Tracking System"

    Material.theme: themeService.theme === "dark" ? Material.Dark : Material.Light
    Material.accent: Material.Indigo

    header: ToolBar {
        RowLayout {
            anchors.fill: parent
            spacing: 12

            ToolButton {
                text: "\u2630"
                onClicked: drawer.open()
            }

            Label {
                text: stack.currentItem && stack.currentItem.pageTitle ? stack.currentItem.pageTitle : root.title
                font.pixelSize: 16
                Layout.fillWidth: true
                elide: Label.ElideRight
            }

            ToolButton {
                text: themeService.theme === "dark" ? "Light" : "Dark"
                onClicked: themeService.toggle()
            }
        }
    }

    Drawer {
        id: drawer
        width: 260
        height: parent.height

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 16
            spacing: 12

            Label {
                text: "MOA & LO\nTracking System"
                font.pixelSize: 18
                font.bold: true
            }

            Rectangle { Layout.fillWidth: true; height: 1; opacity: 0.2; color: "#888" }

            Button {
                text: "Dashboard"
                Layout.fillWidth: true
                onClicked: {
                    stack.replace(Qt.resolvedUrl("screens/Dashboard.qml"))
                    drawer.close()
                }
            }

            Button {
                text: "View Records"
                Layout.fillWidth: true
                onClicked: {
                    stack.replace(Qt.resolvedUrl("screens/Records.qml"))
                    drawer.close()
                }
            }

            Button {
                text: "Add Record"
                Layout.fillWidth: true
                onClicked: {
                    stack.replace(Qt.resolvedUrl("screens/AddEditRecord.qml"), { mode: "add", recordId: -1 })
                    drawer.close()
                }
            }

            Item { Layout.fillHeight: true }

            Label {
                text: "Theme"
                opacity: 0.8
            }

            RowLayout {
                Layout.fillWidth: true
                spacing: 8

                Button {
                    text: "Light"
                    Layout.fillWidth: true
                    enabled: themeService.theme !== "light"
                    onClicked: themeService.setTheme("light")
                }
                Button {
                    text: "Dark"
                    Layout.fillWidth: true
                    enabled: themeService.theme !== "dark"
                    onClicked: themeService.setTheme("dark")
                }
            }
        }
    }

    StackView {
        id: stack
        anchors.fill: parent
        initialItem: Qt.resolvedUrl("screens/Dashboard.qml")
    }
}

