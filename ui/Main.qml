import QtQuick.Layouts 1.4
import QtQuick 2.4
import QtQuick.Controls 2.0
import org.kde.kirigami 2.4 as Kirigami
import "tic-tac-toe.js" as Logic

import Mycroft 1.0 as Mycroft

Mycroft.ScrollableDelegate {
    id: delegate
    graceTime: 80000
    property bool running: true
    property var playerTurn
    property var playerMove
    property var computerMove
    property alias gameMessage: messageBoard.text
    property var playerSymbol
    property bool boardClear
    
    onBoardClearChanged: {
        if(boardClear){
            Logic.clearBoard()
        }
    }
    
    onPlayerTurnChanged: {
        console.log("fromMainQML Player Turn:" + playerTurn)
        console.log("fromMainQML Player Move:" + playerMove)
        console.log("fromMainQML Computer Move:" + computerMove)
        if(playerTurn.indexOf("player") !== -1){
            playerSymbol = "X"
            Logic.makeMove(mapMoveToGrid(playerMove), playerSymbol)
        }
        else {
            playerSymbol = "O"
            Logic.makeMove(mapMoveToGrid(computerMove), playerSymbol)
        }
    }
    
    function mapMoveToGrid(move){
        switch(move) {
            case 1:
                return 6
                break
            case 2:
                return 7
                break
            case 3:
                return 8
                break
            case 4:
                return 3
                break
            case 5:
                return 4
                break
            case 6:
                return 5
                break
            case 7:
                return 0
                break
            case 8:
                return 1
                break
            case 9:
                return 2
                break
        }
    }
        
    Rectangle {
        id: game
        
        width: display.width; height: display.height + 10
        
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
                            if (Logic.canPlayAtPos(index)) {
                                Logic.makeMove(index, "O")
                                console.log(index)
                            }
                        }
                    }
                }
            }
        }
    }
    Label {
        id: messageBoard
        Layout.fillWidth: true
    }
}
