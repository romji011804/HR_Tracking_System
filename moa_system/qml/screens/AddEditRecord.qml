import QtQuick 2.15
import QtQuick.Controls 6.5
import QtQuick.Layouts 1.15
import "../components"

Page {
    id: page
    property string pageTitle: mode === "edit" ? "Edit Record" : "Add Record"

    // passed in from navigation
    property string mode: "add"     // "add" | "edit"
    property int recordId: -1

    // Form state
    property string controlNumber: ""
    property string loMode: "upload"     // upload|link
    property string moaMode: "upload"    // upload|link

    // Loaded record
    property var record: ({})

    function normalizeUrl(v) {
        var s = (v || "").trim()
        if (s.length === 0) return ""
        if (s.startsWith("http://") || s.startsWith("https://")) return s
        return "https://" + s
    }

    Component.onCompleted: {
        if (mode !== "edit") {
            controlNumber = recordsService.next_control_number()
        }
        if (mode === "edit" && recordId > 0) {
            record = recordsService.get_record(recordId)
            if (record && record.control_number) {
                controlNumber = record.control_number
                school.text = record.school_name || ""
                course.text = record.course || ""
                hoursField.text = String(record.number_of_hours || "")
                statusBox.currentIndex = statusBox.indexOfValue(record.status || "Ongoing")
                workflowBox.currentIndex = workflowBox.indexOfValue(record.workflow_stage || "Received")
                loAvailable.checked = !!record.legal_opinion
                moaAvailable.checked = !!record.moa_available

                loValue.text = record.lo_file || ""
                moaValue.text = record.moa_file || ""
                loMode = (loValue.text.startsWith("http://") || loValue.text.startsWith("https://")) ? "link" : "upload"
                moaMode = (moaValue.text.startsWith("http://") || moaValue.text.startsWith("https://")) ? "link" : "upload"

                loUpload.checked = loMode === "upload"
                loLink.checked = loMode === "link"
                moaUpload.checked = moaMode === "upload"
                moaLink.checked = moaMode === "link"
            }
        }
    }

    ScrollView {
        anchors.fill: parent
        contentWidth: width

        ColumnLayout {
            width: parent.width
            spacing: 14
            padding: 16

            Rectangle {
                Layout.fillWidth: true
                radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 14
                    spacing: 10

                    Label { text: page.pageTitle; font.pixelSize: 18; font.bold: true }
                    Label { text: "Fill in the details below."; opacity: 0.7 }
                }
            }

            // Basic information
            Rectangle {
                Layout.fillWidth: true
                radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"

                GridLayout {
                    anchors.fill: parent
                    anchors.margins: 14
                    columns: 2
                    columnSpacing: 12
                    rowSpacing: 10

                    Label { text: "School/University"; }
                    RecentCombo {
                        id: school
                        Layout.fillWidth: true
                        placeholderText: "Type school/university..."
                        recentModel: recentSchoolModel
                    }

                    Label { text: "Course"; }
                    RecentCombo {
                        id: course
                        Layout.fillWidth: true
                        placeholderText: "Type course..."
                        recentModel: recentCourseModel
                    }

                    Label { text: "Hours"; }
                    RecentCombo {
                        id: hoursField
                        Layout.fillWidth: true
                        placeholderText: "Type hours..."
                        recentModel: recentHoursModel
                    }

                    Label { text: "Status"; }
                    ComboBox {
                        id: statusBox
                        Layout.fillWidth: true
                        textRole: ""
                        model: [
                            { label: "Ongoing", value: "Ongoing" },
                            { label: "Completed", value: "Completed" }
                        ]
                        valueRole: "value"
                        delegate: ItemDelegate { text: modelData.label; width: ListView.view.width }
                        contentItem: Text { text: statusBox.currentValue; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
                    }

                    Label { text: "Workflow Stage"; }
                    ComboBox {
                        id: workflowBox
                        Layout.fillWidth: true
                        model: [
                            { label: "Received", value: "Received" },
                            { label: "For Legal Review", value: "For Legal Review" },
                            { label: "Legal Opinion Issued", value: "Legal Opinion Issued" },
                            { label: "MOA Preparation", value: "MOA Preparation" },
                            { label: "For Signing", value: "For Signing" },
                            { label: "Completed", value: "Completed" }
                        ]
                        valueRole: "value"
                        delegate: ItemDelegate { text: modelData.label; width: ListView.view.width }
                        contentItem: Text { text: workflowBox.currentValue; verticalAlignment: Text.AlignVCenter; elide: Text.ElideRight }
                    }

                    Label { text: "Control #"; opacity: 0.8 }
                    TextField {
                        Layout.fillWidth: true
                        readOnly: true
                        text: controlNumber
                    }
                }
            }

            // LO / MOA
            Rectangle {
                Layout.fillWidth: true
                radius: 12
                color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
                border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"

                ColumnLayout {
                    anchors.fill: parent
                    anchors.margins: 14
                    spacing: 12

                    Label { text: "Legal Opinion"; font.bold: true }
                    RowLayout {
                        Layout.fillWidth: true
                        CheckBox { id: loAvailable; text: "Available" }
                        Item { Layout.fillWidth: true }
                        RadioButton { id: loUpload; text: "Upload"; checked: true; onClicked: loMode = "upload" }
                        RadioButton { id: loLink; text: "Paste Link"; onClicked: loMode = "link" }
                    }
                    TextField {
                        id: loValue
                        Layout.fillWidth: true
                        placeholderText: loMode === "link" ? "Paste LO URL..." : "Path to LO file (uploads handled later)"
                        readOnly: loMode !== "link"
                    }

                    Rectangle { Layout.fillWidth: true; height: 1; opacity: 0.2; color: "#888" }

                    Label { text: "Memorandum of Agreement"; font.bold: true }
                    RowLayout {
                        Layout.fillWidth: true
                        CheckBox { id: moaAvailable; text: "Available" }
                        Item { Layout.fillWidth: true }
                        RadioButton { id: moaUpload; text: "Upload"; checked: true; onClicked: moaMode = "upload" }
                        RadioButton { id: moaLink; text: "Paste Link"; onClicked: moaMode = "link" }
                    }
                    TextField {
                        id: moaValue
                        Layout.fillWidth: true
                        placeholderText: moaMode === "link" ? "Paste MOA URL..." : "Path to MOA file (uploads handled later)"
                        readOnly: moaMode !== "link"
                    }
                }
            }

            // Save actions
            RowLayout {
                Layout.fillWidth: true
                spacing: 10
                Item { Layout.fillWidth: true }

                Button {
                    text: "Save"
                    onClicked: {
                        var schoolV = school.text.trim()
                        var courseV = course.text.trim()
                        if (schoolV.length === 0 || courseV.length === 0) {
                            errorDialog.text = "School and Course are required."
                            errorDialog.open()
                            return
                        }

                        var hoursV = parseInt(hoursField.text.trim())
                        if (isNaN(hoursV)) hoursV = 0

                        var loFileV = loValue.text.trim()
                        var moaFileV = moaValue.text.trim()
                        if (loMode === "link") loFileV = normalizeUrl(loFileV)
                        if (moaMode === "link") moaFileV = normalizeUrl(moaFileV)

                        var payload = {
                            control_number: controlNumber,
                            school_name: schoolV,
                            course: courseV,
                            number_of_hours: hoursV,
                            date_received: (record.date_received || new Date().toISOString().slice(0,10)),
                            date_lo: (record.date_lo || new Date().toISOString().slice(0,10)),
                            legal_opinion: loAvailable.checked,
                            lo_scanned: (record.lo_scanned || false),
                            lo_file: loFileV.length === 0 ? null : loFileV,
                            date_moa: (record.date_moa || new Date().toISOString().slice(0,10)),
                            moa_available: moaAvailable.checked,
                            moa_scanned: (record.moa_scanned || false),
                            moa_file: moaFileV.length === 0 ? null : moaFileV,
                            workflow_stage: workflowBox.currentValue,
                            status: statusBox.currentValue
                        }

                        // Add recents
                        recentSchoolModel.addValue(schoolV)
                        recentCourseModel.addValue(courseV)
                        recentHoursModel.addValue(String(hoursV))

                        if (mode === "edit" && recordId > 0) {
                            recordsService.update_record(recordId, payload)
                        } else {
                            recordsService.add_record(payload)
                        }
                        page.StackView.view.pop()
                    }
                }

                Button {
                    text: "Cancel"
                    onClicked: page.StackView.view.pop()
                }
            }
        }
    }

    Dialog {
        id: errorDialog
        property string text: ""
        title: "Validation"
        modal: true
        standardButtons: Dialog.Ok
        contentItem: Text { text: errorDialog.text; wrapMode: Text.Wrap }
    }
}

