function  clearBoard()
{
    game.running = true

    for (var i=0; i<9; ++i)
        board.children[i].state = ""
}

function mapMoveToLocalGrid(move){
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

function mapMoveToSkillGrid(move){
    switch(move) {
        case 6:
            return "select bottom left"
            break
        case 7:
            return "select bottom center"
            break
        case 8:
            return "select bottom right"
            break
        case 3:
            return "select middle left"
            break
        case 4:
            return "select middle"
            break
        case 5:
            return "select middle right"
            break
        case 0:
            return "select top left"
            break
        case 1:
            return "select top center"
            break
        case 2:
            return "select top right"
            break
    }
}

function makeMove(pos, player)
{
    board.children[pos].state = player
}

function canPlayAtPos(pos)
{
    return board.children[pos].state == ""
    console.log(pos)
}


function gameFinished()
{
    game.running = false
}
