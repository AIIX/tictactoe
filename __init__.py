"""
TicTacToe Mycroft Skill.
"""
import random
import time
from adapt.intent import IntentBuilder
from os.path import join, dirname
from string import Template
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import *
from mycroft.util import read_stripped_lines
from mycroft.util.log import getLogger
from mycroft.messagebus.message import Message

__author__ = 'aix'

LOGGER = getLogger(__name__)
theBoard = [' '] * 10
playerLetter = "X"
computerLetter = "O"
gameIsPlaying = ""
globalMove = ""
playerHasMoved = False
turn = ""

class TicTacToeSkill(MycroftSkill):
    def __init__(self):
        """
        TicTacToe Skill Class.
        """    
        super(TicTacToeSkill, self).__init__(name="TicTacToeSkill")
        turn = self.whoGoesFirst()
        #global turn

    @intent_handler(IntentBuilder("PlayerInit").require("PlayerInitKeyword").build())
    def handle_player_init_intent(self, message):
        """
        Player Init & Board Init
        """    
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(message.data.get('PlayerInitKeyword'), '')
        searchString = utterance   
        playerLetter, computerLetter = self.inputLetter(searchString)
        global gameIsPlaying
        global theBoard
        global turn
        gameIsPlaying = True
        self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe", "boardClear": True}))
        turn = self.whoGoesFirst()
        whoPlays = self.checkWhosTurn(turn)
        
    @intent_handler(IntentBuilder("PlayerTurn").require("PlayerTurnKeyword").build())
    def handle_player_turn_intent(self, message):
        global playerLetter
        global gameIsPlaying
        global playerHasMoved
        playLetter = playerLetter
        self.drawBoard(theBoard)
        self.speak('What is your next move?', expect_response=True)
        self.makePlayerMove();
        
        if self.isWinner(theBoard, playerLetter):
            self.drawBoard(theBoard)
            winMessage = 'Congrats You Won The Game'
            self.speak(winMessage)
            self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe/finished", "gameMessage": winMessage}))
            self.resetBoard()
            gameIsPlaying = False
        else:
            if self.isBoardFull(theBoard):
                self.drawBoard(theBoard)
                tieMessage = 'The game is a tie!' 
                self.speak(tieMessage)
                self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe/finished", "gameMessage": tieMessage}))
                self.resetBoard()
            else:
                turn = 'computer'
                whoPlays = self.checkWhosTurn(turn)
    
    @intent_handler(IntentBuilder("ComputerTurn").require("ComputerTurnKeyword").build())
    def handle_computer_turn_intent(self, message):
        global computerLetter
        compLetter = computerLetter
        move = self.getComputerMove(theBoard, compLetter)
        self.makeMove(theBoard, computerLetter, move)
        self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe", "playerTurn": "computer", "computerMove": move}))

        if self.isWinner(theBoard, computerLetter):
            self.drawBoard(theBoard)
            looseMessage = 'I have beaten You, You Loose'
            self.speak(looseMessage)
            self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe/finished", "gameMessage": looseMessage}))
            self.resetBoard()
            gameIsPlaying = False
        else:
            if self.isBoardFull(theBoard):
                self.drawBoard(theBoard)
                tieMessage = 'The game is a tie!' 
                self.speak(tieMessage)
                self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe/finished", "gameMessage": tieMessage}))
            else:
                turn = 'player'
                whoPlays = self.checkWhosTurn(turn)
    
    @intent_handler(IntentBuilder("GetPlayerKey").require("PlayerKey").build())
    def handle_get_player_key_intent(self, message):
        utterance = message.data.get('utterance').lower()
        utterance = utterance.replace(message.data.get('PlayerKey'), '')
        searchString = utterance.replace(" ", "")
        global globalMove
        global playerHasMoved
        self.speak(searchString)
        if searchString and searchString.strip():
            self.speak("PlayerHasMoved")
            playerHasMoved = True
        
        if searchString == "topleft":
            globalMove = 7
            searchString = ""
        elif searchString == "topright":
            globalMove = 9
            searchString = ""
        elif searchString == "topmiddle":
            globalMove = 8
            searchString = ""
        elif searchString == "topcenter":
            globalMove = 8
            searchString = ""
        elif searchString == "middleleft":
            globalMove = 4
            searchString = ""
        elif searchString == "middle":
            globalMove = 5
            searchString = ""
        elif searchString == "center":
            globalMove = 5
            searchString = ""
        elif searchString == "middleright":
            globalMove = 6
            searchString = ""
        elif searchString == "bottomleft":
            globalMove = 1
            searchString = ""
        elif searchString == "bottommiddle":
            globalMove = 2
            searchString = ""
        elif searchString == "bottomcenter":
            globalMove = 2
            searchString = ""
        elif searchString == "bottomright":
            globalMove = 3
            searchString = ""
        else:
            self.speak("No Valid Move Found")
        
    @intent_handler(IntentBuilder("EndGame").require("EndGameKey").build())
    def handle_end_game_intent(self, message):
        self.resetBoard()
        global turn
        global gameIsPlaying
        turn = "endGame"
        gameIsPlaying = False
        self.stop()
        whoPlays = self.checkWhosTurn(turn)
        
    def makePlayerMove(self):
        global theBoard
        global playerLetter
        global gameIsPlaying
        global playerHasMoved
        playLetter = playerLetter
        
        while not playerHasMoved:
            time.sleep(1)
        
        if playerHasMoved is True:
            #time.sleep(10)
            if gameIsPlaying == True:
                move = self.getPlayerMove(theBoard)
                self.makeMove(theBoard, playLetter, move)
                self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe", "playerTurn": "player", "playerMove": move}))
                playerHasMoved = False;
            else:
                LOGGER.info("Do Nothing")
        else:
            #time.sleep(30)
            if gameIsPlaying == True:
                move = self.getPlayerMove(theBoard)
                self.makeMove(theBoard, playLetter, move)
                self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe", "playerTurn": "player", "playerMove": move}))
                playerHasMoved = False;
            else:
                LOGGER.info("Do Nothing")
    
    
    def checkWhosTurn(self, turn):
        if gameIsPlaying == True:
            pturn = turn
            messageTurn = ""
            if turn == 'player':
                self.speak("It is your turn")
                messageTurn = "Player's Turn"
                self.enclosure.bus.emit(Message("recognizer_loop:utterance", {"utterances": ["player turn"], "lang": "en-us"}));
            elif turn == 'computer':
                self.speak("It is my turn")
                messageTurn = "It's Mycroft's Turn"
                self.enclosure.bus.emit(Message("recognizer_loop:utterance", {"utterances": ["computer turn"], "lang": "en-us"}));
            else:
                LOGGER.info("Do Nothing")
            self.enclosure.bus.emit(Message("metadata", {"type": "tictactoe", "playerTurn": pturn, "gameMessage": messageTurn}))
        else:
            gameIsPlaying == False
    
    def inputLetter(self, getKey):
        if getKey == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']
   
    def whoGoesFirst(self):
        if random.randint(0, 1) == 0:
            return 'computer'
        else:
            return 'player'
        self.speak('The ' + turn + ' will go first.')

    def drawBoard(self, board):
        # This function prints out the board that it was passed.
        # "board" is a list of 10 strings representing the board (ignore index 0)
        print('   |   |')
        print(' ' + board[7] + ' | ' + board[8] + ' | ' + board[9])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[4] + ' | ' + board[5] + ' | ' + board[6])
        print('   |   |')
        print('-----------')
        print('   |   |')
        print(' ' + board[1] + ' | ' + board[2] + ' | ' + board[3])
        print('   |   |')

    def isWinner(self, bo, le):
        # Given a board and a player's letter, this function returns True if that player has won.
        # We use bo instead of board and le instead of letter so we don't have to type as much.
        return ((bo[7] == le and bo[8] == le and bo[9] == le) or # across the top
        (bo[4] == le and bo[5] == le and bo[6] == le) or # across the middle
        (bo[1] == le and bo[2] == le and bo[3] == le) or # across the bottom
        (bo[7] == le and bo[4] == le and bo[1] == le) or # down the left side
        (bo[8] == le and bo[5] == le and bo[2] == le) or # down the middle
        (bo[9] == le and bo[6] == le and bo[3] == le) or # down the right side
        (bo[7] == le and bo[5] == le and bo[3] == le) or # diagonal
        (bo[9] == le and bo[5] == le and bo[1] == le)) # diagonal
    
    
    def makeMove(self, board, letter, move):
        if move != 0:
            try:
                board[move] = letter
            except Exception as e:
                LOGGER.info("error")
        else:
           LOGGER.info("No Move")
       
    def getBoardCopy(self, board):
        # Make a duplicate of the board list and return it the duplicate.
        dupeBoard = []

        for i in board:
            dupeBoard.append(i)

        return dupeBoard

    def isSpaceFree(self, board, move):
        # Return true if the passed move is free on the passed board.
        return board[move] == ' '

    def getPlayerMove(self, board):
        # Let the player type in his move.
        move = globalMove
        #while move not in '1 2 3 4 5 6 7 8 9'.split() or not self.isSpaceFree(board, int(move)):
        try:
            return int(move)
        except Exception as e:
            return int(0)

    def chooseRandomMoveFromList(self, board, movesList):
        # Returns a valid move from the passed list on the passed board.
        # Returns None if there is no valid move.
        possibleMoves = []
        for i in movesList:
            if self.isSpaceFree(board, i):
                possibleMoves.append(i)

        if len(possibleMoves) != 0:
            return random.choice(possibleMoves)
        else:
            return None

    def getComputerMove(self, board, computerLetter):
        # Given a board and the computer's letter, determine where to move and return that move.

        if computerLetter == 'X':
            playerLetter = 'O'
        else:
            playerLetter = 'X'

        # Here is our algorithm for our Tic Tac Toe AI:
        # First, check if we can win in the next move
        for i in range(1, 10):
            copy = self.getBoardCopy(board)
            if self.isSpaceFree(copy, i):
                self.makeMove(copy, computerLetter, i)
                if self.isWinner(copy, computerLetter):
                    return i

        # Check if the player could win on his next move, and block them.
        for i in range(1, 10):
            copy = self.getBoardCopy(board)
            if self.isSpaceFree(copy, i):
                self.makeMove(copy, playerLetter, i)
                if self.isWinner(copy, playerLetter):
                    return i

        # Try to take one of the corners, if they are free.
        move = self.chooseRandomMoveFromList(board, [1, 3, 7, 9])
        if move != None:
            return move

        # Try to take the center, if it is free.
        if self.isSpaceFree(board, 5):
            return 5

        # Move on one of the sides.
        return self.chooseRandomMoveFromList(board, [2, 4, 6, 8])

    def isBoardFull(self, board):
        # Return True if every space on the board has been taken. Otherwise return False.
        for i in range(1, 10):
            if self.isSpaceFree(board, i):
                return False
        return True

    def resetBoard(self):
        global theBoard
        theBoard = [' '] * 10

    def stop(self):
        """
        Mycroft Stop Function
        """
        pass
    
def create_skill():
    """
    Mycroft Create Skill Function
    """
    return TicTacToeSkill()
