import QtQuick 2.15
import QtQuick.Controls 6.5
import QtQuick.Layouts 1.15

Item {
    id: root
    property alias text: field.text
    property string placeholderText: ""
    property var recentModel
    signal committed(string value)
    signal removed(string value)

    implicitHeight: field.implicitHeight
    implicitWidth: field.implicitWidth

    RowLayout {
        anchors.fill: parent
        spacing: 6

        TextField {
            id: field
            Layout.fillWidth: true
            placeholderText: root.placeholderText
            onAccepted: {
                if (text.trim().length > 0 && root.recentModel) {
                    root.recentModel.addValue(text.trim())
                }
                root.committed(text.trim())
            }
        }

        ToolButton {
            text: "✕"
            enabled: field.text.trim().length > 0
            onClicked: {
                var v = field.text.trim()
                if (v.length > 0 && root.recentModel) {
                    root.recentModel.deleteValue(v)
                }
                root.removed(v)
            }
        }
    }

    // Simple dropdown popup suggestions
    Popup {
        id: popup
        width: root.width
        y: root.height + 4
        modal: false
        focus: true
        closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutsideParent

        Rectangle {
            anchors.fill: parent
            radius: 10
            color: Material.theme === Material.Dark ? "#111827" : "#ffffff"
            border.color: Material.theme === Material.Dark ? "#1f2937" : "#e5e7eb"
        }

        ListView {
            anchors.fill: parent
            anchors.margins: 6
            clip: true
            model: root.recentModel
            delegate: ItemDelegate {
                width: ListView.view.width
                text: model.value
                onClicked: {
                    field.text = model.value
                    popup.close()
                }
            }
        }
    }

    Timer {
        id: openTimer
        interval: 0
        running: false
        repeat: false
        onTriggered: {
            if (!root.recentModel) return
            if (field.activeFocus && field.text.length >= 0) {
                popup.open()
            }
        }
    }

    Connections {
        target: field
        function onTextEdited() {
            // Keep it simple: show popup while typing
            if (!popup.opened) openTimer.start()
        }
        function onActiveFocusChanged() {
            if (!field.activeFocus) popup.close()
        }
    }
}

