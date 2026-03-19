import QtQuick 2.15
import QtQuick.Controls 6.5
import QtQuick.Layouts 1.15

Page {
    id: page
    property string pageTitle: "Dashboard"
    property var stats: ({ total: 0, ongoing: 0, completed: 0, missing_lo: 0, missing_moa: 0 })

    function reload() {
        stats = recordsService.get_dashboard_stats()
    }

    Component.onCompleted: reload()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            Label { text: "Dashboard"; font.pixelSize: 20; font.bold: true }
            Item { Layout.fillWidth: true }
            Button { text: "Refresh"; onClicked: reload() }
        }

        GridLayout {
            Layout.fillWidth: true
            columns: 3
            columnSpacing: 12
            rowSpacing: 12

            Rectangle { Layout.fillWidth: true; height: 90; radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"
                ColumnLayout { anchors.fill: parent; anchors.margins: 12
                    Label { text: "Total Records"; opacity: 0.7 }
                    Label { text: String(stats.total || 0); font.pixelSize: 28; font.bold: true }
                }
            }
            Rectangle { Layout.fillWidth: true; height: 90; radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"
                ColumnLayout { anchors.fill: parent; anchors.margins: 12
                    Label { text: "Ongoing"; opacity: 0.7 }
                    Label { text: String(stats.ongoing || 0); font.pixelSize: 28; font.bold: true }
                }
            }
            Rectangle { Layout.fillWidth: true; height: 90; radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"
                ColumnLayout { anchors.fill: parent; anchors.margins: 12
                    Label { text: "Completed"; opacity: 0.7 }
                    Label { text: String(stats.completed || 0); font.pixelSize: 28; font.bold: true }
                }
            }

            Rectangle { Layout.fillWidth: true; height: 90; radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"
                ColumnLayout { anchors.fill: parent; anchors.margins: 12
                    Label { text: "Missing Legal Opinion"; opacity: 0.7 }
                    Label { text: String(stats.missing_lo || 0); font.pixelSize: 28; font.bold: true }
                }
            }
            Rectangle { Layout.fillWidth: true; height: 90; radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"
                ColumnLayout { anchors.fill: parent; anchors.margins: 12
                    Label { text: "Missing MOA"; opacity: 0.7 }
                    Label { text: String(stats.missing_moa || 0); font.pixelSize: 28; font.bold: true }
                }
            }
            Item { Layout.fillWidth: true; height: 90 }
        }

        Rectangle {
            Layout.fillWidth: true
            Layout.fillHeight: true
            radius: 12
            color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
            border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 12
                spacing: 8

                RowLayout {
                    Layout.fillWidth: true
                    Label { text: "Recent Records"; font.pixelSize: 16; font.bold: true }
                    Item { Layout.fillWidth: true }
                    Button { text: "View All"; onClicked: page.StackView.view.replace(Qt.resolvedUrl("Records.qml")) }
                }

                Rectangle { Layout.fillWidth: true; height: 1; opacity: 0.2; color: "#888" }

                ListView {
                    id: recentList
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: recordsModel
                    delegate: ItemDelegate {
                        width: ListView.view.width
                        text: (model.pinned ? "★ " : "") + model.controlNumber + " — " + model.schoolName
                        onClicked: page.StackView.view.push(Qt.resolvedUrl("RecordDetail.qml"), { recordId: model.id })
                        visible: index < 5
                    }
                }
            }
        }
    }
}

