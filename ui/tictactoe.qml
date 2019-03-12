import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami
import "tic-tac-toe.js" as Logic

import Mycroft 1.0 as Mycroft

Mycroft.ScrollableDelegate {
    id: delegate
    //graceTime: 80000
    property bool running: true
    property var playerTurn: sessionData.playerTurn
    property var playerMove: sessionData.playerMove
    property var computerMove: sessionData.computerMove
    property var gameMessage: sessionData.gameMessage
    property var playerSymbol: sessionData.playerSymbol
    property bool boardClear: sessionData.boardClear
    property bool pturn
    //backgroundImage: "images/background.png"
    
    onBoardClearChanged: {
        Logic.clearBoard()
    }
    
    onGameMessageChanged: {
        messageBoard.text = gameMessage
    }
    
    onPlayerTurnChanged: {
        if(playerTurn.indexOf("player") !== -1){
            playerSymbol = "X"
            pturn = true
            Logic.makeMove(Logic.mapMoveToLocalGrid(playerMove), playerSymbol)
        }
        else {
            playerSymbol = "O"
            pturn = false
            Logic.makeMove(Logic.mapMoveToLocalGrid(computerMove), playerSymbol)
        }
    }
    
    Rectangle {
        id: topArea
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: -Kirigami.Units.gridUnit * 1
        anchors.right: parent.right
        anchors.rightMargin: -Kirigami.Units.gridUnit * 1
        anchors.topMargin: -Kirigami.Units.gridUnit * 1
        height: Kirigami.Units.gridUnit * 2.5
        color: Kirigami.Theme.backgroundColor
        Kirigami.Heading {
            id: messageBoard
            anchors.fill: parent
            anchors.leftMargin: Kirigami.Units.gridUnit * 1
            level: 3
        }
    }
            
    Item {
        id: game
        anchors.top: topArea.bottom
        width: display.width; 
        height: display.height + 10
        property bool running
        
        Image {
            id: boardImage
            source: "images/board.png"
            width: delegate.width
            height: delegate.height
        }
        
        Column {
            id: display
            
            Grid {
                id: board
                width: boardImage.width; height: boardImage.height
                columns: 3
                
                Repeater {
                    model: 9
                    
                    TicTac {
                        width: board.width/3
                        height: board.height/3
                        
                        onClicked: {
                        if(pturn){
                            if (Logic.canPlayAtPos(index)) {
                                Logic.makeMove(index, playerSymbol)
                                Mycroft.MycroftController.sendText(Logic.mapMoveToSkillGrid(index))
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
