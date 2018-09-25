function  clearBoard()
{
    game.running = true

    for (var i=0; i<9; ++i)
        board.children[i].state = ""
}

function makeMove(pos, player)
{
    board.children[pos].state = player
    //if (winner(board)) {
    //    gameFinished(player + " wins")
    //    return true
    //} else {
    //    return false
    //}
}

function canPlayAtPos(pos)
{
    return board.children[pos].state == ""
    console.log(pos)
}


function gameFinished(message)
{
    //messageDisplay.text = message
    //messageDisplay.visible = true
    game.running = false
}
