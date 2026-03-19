import QtQuick 2.15
import QtQuick.Controls 6.5
import QtQuick.Layouts 1.15

Page {
    id: page
    property int recordId: -1
    property var record: ({})
    property string pageTitle: record && record.control_number ? record.control_number : "Record"

    function reload() {
        if (recordId > 0) {
            record = recordsService.get_record(recordId) || ({})
        }
    }

    Component.onCompleted: reload()

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            Button {
                text: "Back"
                onClicked: page.StackView.view.pop()
            }

            Item { Layout.fillWidth: true }

            Button {
                text: "Edit"
                onClicked: page.StackView.view.push(Qt.resolvedUrl("AddEditRecord.qml"), { mode: "edit", recordId: recordId })
            }
        }

        Rectangle {
            Layout.fillWidth: true
            radius: 12
            color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
            border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 14
                spacing: 10

                Label { text: "Record Details"; font.pixelSize: 18; font.bold: true }
                Label { text: "Control #: " + (record.control_number || ""); opacity: 0.8 }

                Rectangle { Layout.fillWidth: true; height: 1; opacity: 0.2; color: "#888" }

                GridLayout {
                    Layout.fillWidth: true
                    columns: 2
                    columnSpacing: 12
                    rowSpacing: 8

                    Label { text: "School/University"; opacity: 0.8 }
                    Label { text: record.school_name || ""; Layout.fillWidth: true; elide: Label.ElideRight }

                    Label { text: "Course"; opacity: 0.8 }
                    Label { text: record.course || ""; Layout.fillWidth: true; elide: Label.ElideRight }

                    Label { text: "Hours"; opacity: 0.8 }
                    Label { text: String(record.number_of_hours || ""); }

                    Label { text: "Date Received"; opacity: 0.8 }
                    Label { text: record.date_received || ""; }

                    Label { text: "Workflow"; opacity: 0.8 }
                    Label { text: record.workflow_stage || ""; }

                    Label { text: "Status"; opacity: 0.8 }
                    Label { text: record.status || ""; }
                }

                Rectangle { Layout.fillWidth: true; height: 1; opacity: 0.2; color: "#888" }

                RowLayout {
                    Layout.fillWidth: true
                    spacing: 12

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        Label { text: "Legal Opinion"; font.bold: true }
                        Label { text: record.lo_file || "No file available"; opacity: record.lo_file ? 1.0 : 0.6; wrapMode: Text.Wrap }
                        Button {
                            text: "Open LO"
                            enabled: !!record.lo_file
                            onClicked: fileService.openPathOrUrl(record.lo_file)
                        }
                    }

                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 6
                        Label { text: "MOA"; font.bold: true }
                        Label { text: record.moa_file || "No file available"; opacity: record.moa_file ? 1.0 : 0.6; wrapMode: Text.Wrap }
                        Button {
                            text: "Open MOA"
                            enabled: !!record.moa_file
                            onClicked: fileService.openPathOrUrl(record.moa_file)
                        }
                    }
                }
            }
        }
    }
}

