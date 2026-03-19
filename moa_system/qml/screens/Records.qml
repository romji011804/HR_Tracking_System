import QtQuick 2.15
import QtQuick.Controls 6.5
import QtQuick.Layouts 1.15

Page {
    id: page
    property string pageTitle: "View Records"

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 16
        spacing: 12

        // Filters
        RowLayout {
            Layout.fillWidth: true
            spacing: 12

            TextField {
                id: searchField
                Layout.fillWidth: true
                placeholderText: "Search by Control #, School, or Course..."
                onTextChanged: recordsModel.setSearch(text)
            }

            ComboBox {
                id: filterBox
                Layout.preferredWidth: 180
                model: ["All", "Ongoing", "Completed", "Missing LO", "Missing MOA"]
                onCurrentTextChanged: recordsModel.setFilterType(currentText)
            }
        }

        // Bulk actions
        RowLayout {
            Layout.fillWidth: true
            spacing: 10

            CheckBox {
                id: selectAll
                text: "Select All"
                onToggled: recordsModel.setAllChecked(checked)
            }

            Button {
                text: "Pin Selected"
                onClicked: recordsService.set_pinned(recordsModel.checkedIds(), true)
            }
            Button {
                text: "Unpin Selected"
                onClicked: recordsService.set_pinned(recordsModel.checkedIds(), false)
            }

            Item { Layout.fillWidth: true }

            Button {
                text: "Delete Selected"
                onClicked: confirmDelete.open()
            }
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

                // Header row (simple table header)
                RowLayout {
                    Layout.fillWidth: true
                    spacing: 10

                    Label { text: ""; Layout.preferredWidth: 34; opacity: 0.7 }
                    Label { text: "Control #"; Layout.preferredWidth: 160; font.bold: true; opacity: 0.8 }
                    Label { text: "School/University"; Layout.fillWidth: true; font.bold: true; opacity: 0.8 }
                    Label { text: "Course"; Layout.preferredWidth: 220; font.bold: true; opacity: 0.8 }
                    Label { text: "Hours"; Layout.preferredWidth: 70; horizontalAlignment: Text.AlignRight; font.bold: true; opacity: 0.8 }
                    Label { text: "Status"; Layout.preferredWidth: 120; font.bold: true; opacity: 0.8 }
                }

                Rectangle { Layout.fillWidth: true; height: 1; opacity: 0.2; color: "#888" }

                ListView {
                    id: list
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    clip: true
                    model: recordsModel
                    spacing: 6

                    delegate: Rectangle {
                        width: list.width
                        height: 46
                        radius: 10
                        color: Material.theme === Material.Dark ? "#0b1220" : "#f9fafb"
                        border.color: Material.theme === Material.Dark ? "#111827" : "#e5e7eb"

                        RowLayout {
                            anchors.fill: parent
                            anchors.margins: 10
                            spacing: 10

                            CheckBox {
                                Layout.preferredWidth: 34
                                checked: model.checked
                                onClicked: recordsModel.toggleChecked(model.id)
                            }

                            Label {
                                Layout.preferredWidth: 160
                                text: (model.pinned ? "★ " : "") + model.controlNumber
                                elide: Label.ElideRight
                                font.bold: model.pinned
                            }

                            Label {
                                Layout.fillWidth: true
                                text: model.schoolName
                                elide: Label.ElideRight
                            }

                            Label {
                                Layout.preferredWidth: 220
                                text: model.course
                                elide: Label.ElideRight
                            }

                            Label {
                                Layout.preferredWidth: 70
                                text: model.hours
                                horizontalAlignment: Text.AlignRight
                                opacity: 0.9
                            }

                            Label {
                                Layout.preferredWidth: 120
                                text: model.status
                                opacity: 0.9
                            }
                        }

                        MouseArea {
                            anchors.fill: parent
                            acceptedButtons: Qt.LeftButton
                            onClicked: {
                                // Avoid conflict when clicking checkbox area
                                if (mouse.x < 44) return;
                                page.StackView.view.push(Qt.resolvedUrl("RecordDetail.qml"), { recordId: model.id })
                            }
                        }
                    }

                    ScrollBar.vertical: ScrollBar { }
                }
            }
        }
    }

    Dialog {
        id: confirmDelete
        title: "Delete selected records?"
        modal: true
        standardButtons: Dialog.Ok | Dialog.Cancel
        onAccepted: {
            var ids = recordsModel.checkedIds()
            if (ids.length > 0) {
                recordsService.delete_records(ids)
                recordsModel.setAllChecked(false)
            }
        }
    }
}

