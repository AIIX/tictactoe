import QtQuick 2.9

Item {
    signal clicked

    states: [
        State { name: "X"; PropertyChanges { target: image; source: "images/x.png" } },
        State { name: "O"; PropertyChanges { target: image; source: "images/o.png" } }
    ]

    Image {
        id: image
        anchors.centerIn: parent
    }

    MouseArea {
        anchors.fill: parent
        onClicked: parent.clicked()
    }
}
