import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami

import Mycroft 1.0 as Mycroft

Mycroft.DelegateBase {
    property var gameMessage
    backgroundImage: "../images/background.png"

    
        Flickable {
        anchors.fill: parent
        contentHeight: layout.height
        topMargin: Math.max(0, (height - contentHeight)/2)

        GridLayout {
            id: layout
            width: parent
            columns: 1
            
        Kirigami.Heading{
            id: messageHeader
            Layout.fillWidth: true
            wrapMode: Text.WordWrap
            text: gameMessage
            }
        }
    }
}
