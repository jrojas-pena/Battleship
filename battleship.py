#   program:         battleship.txt
#   submit date:     dec. 8, 2020 (date submitted)
#   due date:        nov. 6, 2020
#   student name:    Juan Rojas
#   student number:  143349181
#   section:         prg550A 
#   purpose:         solution to assignment#1
# STUDENT OATH:
# -------------
#
# "I declare that the attached project is wholly my own work in accordance
# with Seneca Academic Policy. No part of this project has been copied
# manually or electronically from any other source (including web sites) or
# distributed to other students."
#
# Name   Juan Rojas  Student ID  143349181
import random
from os import system, name
from time import sleep

def playBattleship():
    visibleBoard = []
    hiddenBoard = []
    missilesLeft = 50
    score = 0
    previousMove = ()
    listOfMoves = []
    NoOfPlayers = input("How many players? (1 or 0): ")
    initGame(hiddenBoard, visibleBoard)
    if NoOfPlayers == "1":
        while missilesLeft > 0 and score < 160:
            clearScreen()
            (missilesLeft, score) = updateData(hiddenBoard, visibleBoard, missilesLeft, score, previousMove)
            coord = input("Enter Target Coordinates => ")
            previousMove = checkMove(coord, visibleBoard, listOfMoves)
            encodedLastMove = encodeMove(previousMove, visibleBoard)
            listOfMoves.append(encodedLastMove)
            if previousMove == -1:
                previousMove = ()
                input("Error! %s is not a valid coordinate, or has been played already"%coord)
        if score == 160:
            print("Congratulations! You Win!")
        else:
            print("You Lose!")
            drawGame(hiddenBoard, score, missilesLeft, previousMove)
    elif(NoOfPlayers == "0"):
        direction = 1
        while missilesLeft > 0 and score < 160:
            clearScreen()
            (missilesLeft, score) = updateData(hiddenBoard, visibleBoard, missilesLeft, score, previousMove)
            (row, col, direction) = autoplay(visibleBoard, previousMove, direction, listOfMoves)
            previousMove = checkMove(characters[row] + characters[col], visibleBoard, listOfMoves)
            print("Target Coordinates => %s%s"%(characters[row], characters[col]))
            encodedLastMove = encodeMove(previousMove, visibleBoard)
            listOfMoves.append(encodedLastMove)
            sleep(0.1)
        if score == 160:
            print("Congratulations! You Win!")
        else:
            print("You Lose!")
            drawGame(hiddenBoard, score, missilesLeft, previousMove)
    else:
        print("Invalid input.")
    
def updateData(hiddenBoard, visibleBoard, missilesLeft, score, previousMove):
    if previousMove and previousMove != -1:
        row = previousMove[0]
        col = previousMove[1]
        if(hiddenBoard[row][col] != "~" and visibleBoard[row][col] != "X"):
            visibleBoard[row][col] = hiddenBoard[row][col]
            score += 5
        else:
            visibleBoard[row][col] = "X"
        missilesLeft -= 1
        drawGame(visibleBoard, score, missilesLeft, previousMove)        

    elif previousMove != -1:
        drawGame(visibleBoard, score, missilesLeft, previousMove)

    return (missilesLeft, score)

def drawGame(board, score, missilesLeft, previousMove):    
    print("   ", end="")
    for i in range(len(board[0])):
        print(characters[i], end="")
    print()
    for i, row in enumerate(board):
        print(characters[i],"|", end="")
        for j in row:
            print(j, end="")
        print("|")
    print("Missiles Away: %02d"%(50 - missilesLeft), end="")
    print("   Missiles Left: %02d"%missilesLeft)
    print("Current Score: %03d"%score, end="")
    if previousMove:
        print("  Last Move: %s%s"%(characters[previousMove[0]],characters[previousMove[1]]))
    else:
        print("  Last Move: N/A")
    
    

def initGame(hiddenBoard, visibleBoard):
    global characters
    characters = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
    noOfRows = random.randint(10, 35)
    noOfCols = random.randint(10, 35)
    for i in range(noOfRows): #Initialize the hidden board
        array = []
        for j in range(noOfCols):
            array.append("~")
        hiddenBoard.append(array)
    for i in range(noOfRows): #Initialize the visible board
        array = []
        for j in range(noOfCols):
            array.append("~")
        visibleBoard.append(array)
    loadShips(10, "A", hiddenBoard)
    loadShips(8, "C", hiddenBoard)
    loadShips(6, "F", hiddenBoard)
    loadShips(5, "U", hiddenBoard)
    loadShips(3, "S", hiddenBoard)
    return

def loadShips(sizeOfShip, letterOfShip, hiddenBoard):
    colSize = len(hiddenBoard[0])
    rowSize = len(hiddenBoard)
    firstColNo = random.randint(0, colSize- sizeOfShip)
    rowNo = random.randint(0, rowSize - 1)
    
    colNo = firstColNo
    while colNo < firstColNo + sizeOfShip: #Checks if there is not another ship already in position
        if hiddenBoard[rowNo][colNo] != "~":
            firstColNo = random.randint(0, colSize- sizeOfShip - 1)
            rowNo = random.randint(0, rowSize - 1)
            colNo = firstColNo
        colNo += 1
    
    hiddenBoard[rowNo][firstColNo] = "["
    if sizeOfShip != 3:
        for i in range(1, sizeOfShip - 2):
            hiddenBoard[rowNo][firstColNo + i] = letterOfShip
        hiddenBoard[rowNo][firstColNo + sizeOfShip - 2] = "="
        hiddenBoard[rowNo][firstColNo + sizeOfShip - 1] = ">"
    else:
        hiddenBoard[rowNo][firstColNo + 1] = letterOfShip
        hiddenBoard[rowNo][firstColNo + 2] = ">"
            

def checkMove(coordinates, visibleBoard, listOfMoves):
    if len(coordinates) == 2:
        row, col = list(coordinates)
        if col in characters and row in characters:
            tup = (characters.index(row), characters.index(col))
            if encodeMove(tup, visibleBoard) not in listOfMoves:
                colNum = characters.index(col)
                rowNum = characters.index(row)
                if rowNum < len(visibleBoard) and colNum < len(visibleBoard[0]):
                    coordNum = (rowNum, colNum)
                    return coordNum
    return -1

def clearScreen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')

def autoplay(visibleBoard, previousMove, direction, listOfMoves):
    if previousMove and previousMove != -1:
        if visibleBoard[previousMove[0]][previousMove[1]] == "X" and encodeMove(previousMove, visibleBoard) in listOfMoves:
            row = random.randint(0, len(visibleBoard) - 1)
            col = random.randint(0, len(visibleBoard[0]) - 1)
            while encodeMove(checkMove(characters[row] + characters[col], visibleBoard, listOfMoves), visibleBoard) in listOfMoves:
                row = random.randint(0, len(visibleBoard) - 1)
                col = random.randint(0, len(visibleBoard[0]) - 1)
        elif direction == -1 and visibleBoard[previousMove[0]][previousMove[1]] == "[":
            row = previousMove[0]
            col = previousMove[1]
            while visibleBoard[row][col] != "~" and visibleBoard[row][col] != ">":
                col += 1
            if visibleBoard[row][col] == ">":
                row = random.randint(0, len(visibleBoard) - 1)
                col = random.randint(0, len(visibleBoard[0]) - 1)
            direction = 1
        elif direction == 1 and visibleBoard[previousMove[0]][previousMove[1]] == ">":
            row = previousMove[0]
            col = previousMove[1]
            while visibleBoard[row][col] != "~" and visibleBoard[row][col] != "[":
                col -= 1
            if visibleBoard[row][col] == "[":
                row = random.randint(0, len(visibleBoard) - 1)
                col = random.randint(0, len(visibleBoard[0]) - 1)
            direction = -1
        else:
            row = previousMove[0]
            col = previousMove[1] + direction
    else:
        row = random.randint(0, len(visibleBoard) - 1)
        col = random.randint(0, len(visibleBoard[0]) - 1)

    return(row, col, direction)

def encodeMove(previousMove, visibleBoard):
    if previousMove and previousMove != -1:
        (row, col) = previousMove
        encMove = (row * len(visibleBoard[0])) + col
        return encMove 




playBattleship()


