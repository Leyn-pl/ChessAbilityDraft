# Chess - Ability Draft (1.0)
# Made by LEYN1092
# Discord: leyn1092
# Github: Leyn-pl

# Requires:
# Python 3.10+
# Pygame 2.6.0+ (may work on earlier)

# Beta tester: musorshiк

from random import randint
import pygame
import math
import sys
import time

print('Loading...')

# Used by all pieces
class Piece:
    def __init__(self, team: int, name: str, x: int, y: int):
        self.team: int = team
        self.name: str = name
        self.x: int = x
        self.y: int = y
        self.color: str = 'White' if self.team == 0 else 'Black'
        self.id: int = getId(self.name)
        self.cost: int = getCost(self.name)
        self.status: list[str,int] = ['none', 0]
        self.charge: int = 0
    def __repr__(self):
        return f'Piece({self.team}, \'{self.name}\', {self.x}, {self.y})'
    def __str__(self):
        return self.color.upper()[0] + self.name.upper()[0]
    
# Use a piece's ability
def useAbility(piece: Piece, toPos: list[int]) -> None:
    fromPos = [piece.x, piece.y]
    piece.charge = 0
    if piece.name == 'rook':
        swapWith = getBoard(toPos[0], toPos[1])
        move(piece, toPos, False)
        move(swapWith, fromPos, False)
        # Reverse
        startMove(int(not playerMove))
    elif piece.name == 'king' and getAbility(piece.team, 5) == 0:
        piece.status = ['immune', 1]      
    else:
        move(piece, toPos)
        if piece.name != 'queen':
            # Reverse
            startMove(int(not playerMove))

# Move or create a piece. Returns killed piece or False
def move(piece: Piece, toPos: list[int], move: bool = True) -> Piece|bool:
    global Board
    if move:
        Board[piece.y][piece.x] = False    
    piece.x = toPos[0]
    piece.y = toPos[1]
    moveTo = getBoard(toPos[0], toPos[1])
    Board[toPos[1]][toPos[0]] = piece
    return moveTo
# Gets piece id by name
def getId(name: str) -> int:
    match name:
        case 'pawn':
            return 0
        case 'rook':
            return 1
        case 'knight':
            return 2
        case 'bishop':
            return 3
        case 'queen':
            return 4
        case 'king':
            return 5
        case 'trap':
            return 6
        case 'zombie':
            return 7
        case _:
            return -1
pieceNames: list[str] = ['pawn', 'rook', 'knight', 'bishop', 'queen', 'king', 'trap', 'zombie']
def getName(pieceId: int) -> str:
    global pieceNames
    return pieceNames[pieceId]
# Gets piece material by name
def getCost(name: str) -> int:
    if name == 'pawn':
        return 1
    elif name in ['knight', 'bishop']:
        return 3
    elif name == 'rook':
        return 5
    elif name == 'queen':
        return 9
    else:
        return 0
# Returns False or Piece object
def getBoard(x: int, y: int) -> Piece|bool:
    global Board
    return Board[y][x]

# Place pieces of one type on the board
def place(name: str, pos: int, dual: bool = True) -> None:
    global Board
    for team in range(2):
        y = 0 if team == 0 else 7
        x = pos
        Board[y][x] = Piece(team, name, x, y)
        if dual:
            x = 7 - pos
            Board[y][x] = Piece(team, name, x, y)

# Setup
Board: list[list[Piece|bool]] = [[False for _ in range(8)] for _ in range(8)]

# Pawns
for team in range(2):
    for x in range(8):
        y = 1 if team == 0 else 6
        Board[y][x] = Piece(team, 'pawn', x, y)

# Other pieces
place('rook', 0)
place('knight', 1)
place('bishop', 2)
place('queen', 3, False)
place('king', 4, False)

# Abilities. Abils[team][pieceId] to acces
Abils: list[list[int]] = [[0 for _ in range(6)], [0 for _ in range(6)]]

# For easier access inside functions
def getAbility(team: int, pieceId: int) -> int:
    global Abils
    return Abils[team][pieceId]
    
# Ability descriptions
AbilDescr: list[list[list[str]]] = [[[], []] for _ in range(6)]
# 1st abilities (actives)
AbilDescr[0][0].append('Pawn can make double move again')
AbilDescr[0][0].append('after kills a piece.')
AbilDescr[1][0].append('Can swap with friendly piece in reach.')
AbilDescr[1][0].append('Cooldown: 3 normal rook moves.')
AbilDescr[2][0].append('Knight can move 3 squares straight')
AbilDescr[2][0].append('after 4 normal knight moves.')
AbilDescr[3][0].append('Can go 1 square in any direction.')
AbilDescr[3][0].append('Cooldown: 3 normal bishop moves.')
AbilDescr[4][0].append('Places traps every normal move in')
AbilDescr[4][0].append('previous location. Lifetime: 2 moves.')
AbilDescr[4][0].append('Can teleport to any trap once.')
AbilDescr[4][0].append('Instant.')
AbilDescr[5][0].append('Becomes invincible for 1 move.')
AbilDescr[5][0].append('Cooldown: enemy queen death.')
AbilDescr[5][0].append('Instant.')
# 2nd abilities (passives)
AbilDescr[0][1].append('King is invincible if 6+ pawns are alive.')
AbilDescr[1][1].append('WIP')
AbilDescr[2][1].append('If kills a rook or a queen, you can')
AbilDescr[2][1].append('make another move.')
AbilDescr[3][1].append('Kills the piece, which killed your bishop.')
AbilDescr[4][1].append('Summons a controllable zombie pawn every normal')
AbilDescr[4][1].append('move in previous location. Lifetime: 3 moves.')
AbilDescr[5][1].append('King can move 2 squares like a rook.')

# Full guide
Guide: list[str] = []
Guide.append('KING AND GAME CHANGES:')
Guide.append('Game ends when one of the kings dies.')
Guide.append('There are no checks, mates and stalemates.')
Guide.append('Player can skip their move.')
Guide.append('You can castle if position is correct,')
Guide.append('even if you moved the king.')
Guide.append('')
Guide.append('SPECIAL MOVES:')
Guide.append('There is no en passant.')
Guide.append('A green dot is normal a move.')
Guide.append('A dot with red outlile is a kill move.')
Guide.append('A dot with yellow outline is an ability move.')
Guide.append('Instant ability means you can make a move')
Guide.append('after it.')
Guide.append('To promote a pawn or castle, press wand button.')
Guide.append('If an ability has "Cooldown: ", it is charged')
Guide.append('when the game starts.')

# Which player's move
playerMove: int = 0

# Get all moves a piece can currently make
def getMoves(piece: Piece) -> list[list[int,int,str]]:
    moves: list[list[int,int,str]] = []
    # Will return moves as soon as possible to otimise
    # Warning: possible heart attack
    if piece.name in ['pawn', 'zombie']:
        # No en passant not because im lazy, but because its stupid
        # This move so rare that it is almost useless
        if piece.y != int(not piece.team) * 7:
            # White pawn
            if piece.team == 0:
                # Normal move
                if not getBoard(piece.x, piece.y + 1):
                    moves.append([0,1,''])
                    # Double move (not for zombies)
                    if piece.y <= 5 and ((piece.y in [0, 1]) or (getAbility(piece.team, 0) == 0 and piece.charge == 2)) and piece.name != 'zombie':
                        if not getBoard(piece.x, piece.y + 2):
                            moves.append([0,2,'a'])
                # Kill left
                if piece.x > 0:
                    if target := getBoard(piece.x - 1, piece.y + 1):
                        if target.team != piece.team and target.status[0] != 'immune':
                            moves.append([-1,1,'k'])
                # Kill right
                if piece.x < 7:
                    if target := getBoard(piece.x + 1, piece.y + 1):
                        if target.team != piece.team and target.status[0] != 'immune':
                            moves.append([1,1,'k'])
            # Black pawn
            else:
                # Normal move
                if not getBoard(piece.x, piece.y-1):
                    moves.append([0,-1,''])
                    # Double move (not for zombies)
                    if piece.y >= 2 and ((piece.y in [6, 7]) or (getAbility(piece.team, 0) == 0 and piece.charge == 2)) and piece.name != 'zombie':
                        if not getBoard(piece.x, piece.y - 2):
                            moves.append([0,-2,'a'])
                # Kill left
                if piece.x > 0:
                    if target := getBoard(piece.x - 1, piece.y - 1):
                        if target.team != piece.team and target.status[0] != 'immune':
                            moves.append([-1,-1,'k'])
                # Kill right
                if piece.x < 7:
                    if target := getBoard(piece.x + 1, piece.y - 1):
                        if target.team != piece.team and target.status[0] != 'immune':
                            moves.append([1,-1,'k'])        
        return moves
    if piece.name in ['rook', 'queen']:
        for direction in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            for scale in range(1, 8):
                xMovement: int = direction[0] * scale
                yMovement: int = direction[1] * scale
                moveToX: int = piece.x + xMovement
                moveToY: int = piece.y + yMovement
                # Check if not out of board
                if moveToX in range(8) and moveToY in range(8):
                    # Check if there is no friendly piece
                    if target := getBoard(moveToX, moveToY):
                        if target.team != piece.team and target.status[0] != 'immune':
                            # Kill and block further movement
                            moves.append([xMovement, yMovement, 'k'])
                        # If there is a friendly piece, check for rook's ability
                        elif piece.name == 'rook' and getAbility(piece.team, 1) == 0 and piece.charge == 3:
                            moves.append([xMovement, yMovement, 'a'])
                        # A piece is in the way
                        break                        
                    else:
                        # Normal move
                        moves.append([xMovement, yMovement, ''])
                else:
                    break
        # Queen also gets bishop moves
        if piece.name != 'queen': return moves
    if piece.name == 'knight':
        # Left or right
        for xMovement in [-2, 2]:
            for yMovement in [-1, 1]:
                moveToX = piece.x + xMovement
                moveToY = piece.y + yMovement
                # Check if not out of board
                if moveToX in range(8) and moveToY in range(8):
                    # Check if there is no friendly piece
                    if target := getBoard(moveToX, moveToY):
                        if target.team != piece.team and target.status[0] != 'immune':
                            # Kill
                            moves.append([xMovement, yMovement, 'k'])
                    else:
                        # Normal move
                        moves.append([xMovement, yMovement, ''])
        # Down or up
        for yMovement in [-2, 2]:
            for xMovement in [-1, 1]:
                moveToX: int = piece.x + xMovement
                moveToY: int = piece.y + yMovement
                # Check if not out of board
                if moveToX in range(8) and moveToY in range(8):
                    # Check if there is no friendly piece
                    if target := getBoard(moveToX, moveToY):
                        if target.team != piece.team and target.status[0] != 'immune':
                            # Kill
                            moves.append([xMovement, yMovement, 'k'])
                    else:
                        # Normal move
                        moves.append([xMovement, yMovement, ''])
        # Ability jumps
        if getAbility(piece.team, 2) == 0 and piece.charge == 4:
            for coords in [[-3, 0], [3, 0], [0, -3], [0, 3]]:
                moveToX: int = piece.x + coords[0]
                moveToY: int = piece.y + coords[1]
                # Check if not out of board
                if moveToX in range(0, 7) and moveToY in range(0, 7):
                    # Check if there is no
                    if not getBoard(moveToX, moveToY):
                        # Ability jump
                        moves.append([coords[0], coords[1], 'a'])
        return moves
    if piece.name in ['bishop', 'queen']:
        # Ability moves
        if getAbility(piece.team, 3) == 0 and piece.charge == 3 and piece.name == 'bishop':
            # Check if not out of board first, then if square is empty
            if piece.x > 0: 
                if not getBoard(piece.x-1, piece.y): moves.append([-1, 0, 'a'])
            if piece.x < 7:
                if not getBoard(piece.x+1, piece.y): moves.append([1, 0, 'a'])
            if piece.y > 0:
                if not getBoard(piece.x, piece.y-1): moves.append([0, -1, 'a'])
            if piece.y < 7:
                if not getBoard(piece.x, piece.y+1): moves.append([0, 1, 'a'])
        # Normal moves
        for direction in [[-1, -1], [-1, 1], [1, 1], [1, -1]]:
            for scale in range(1, 8):
                xMovement: int = direction[0] * scale
                yMovement: int = direction[1] * scale
                moveToX: int = piece.x + xMovement
                moveToY: int = piece.y + yMovement
                # Check if not out of board
                if moveToX in range(8) and moveToY in range(8):
                    # Check if there is no friendly piece
                    if target := getBoard(moveToX, moveToY):
                        if target.team != piece.team and target.status[0] != 'immune':
                            # Kill and block further movement
                            moves.append([xMovement, yMovement, 'k'])
                        # A piece is in the way
                        break                        
                    else:
                        # Normal move
                        moves.append([xMovement, yMovement, ''])
                else:
                    break
        if piece.name != 'queen': return moves
    if piece.name == 'king':
        # THERE WILL BE NO MOVE RESTRICTIONS UNDER CHECK
        # Not because im lazy, i just think this is stupid. Game should end with king being dead
        # If you can blunder a mate in 1, why not allow blundering a mate in 0?
        # Ability move
        if getAbility(piece.team, 5) == 0 and piece.charge == 1:
            moves.append([0, 0, 'a'])
        # 1 square like a bishop
        for direction in [[-1, -1], [-1, 1], [1, 1], [1, -1]]:
            xMovement: int = direction[0]
            yMovement: int = direction[1]
            moveToX: int = piece.x + xMovement
            moveToY: int = piece.y + yMovement            
            # Check if not out of board
            if moveToX in range(8) and moveToY in range(8):
                # Check if there is no friendly piece
                if target := getBoard(moveToX, moveToY):
                    if target.team != piece.team and target.status[0] != 'immune':
                        # Kill
                        moves.append([xMovement, yMovement, 'k'])
                # No need to block movement here
                else:
                    # Normal move
                    moves.append([xMovement, yMovement, ''])
        # 1 or 2 squares like a rook
        for direction in [[-1, 0], [1, 0], [0, -1], [0, 1]]:
            scaleRange = [1, 2] if getAbility(piece.team, 5) == 1 else [1]
            for scale in scaleRange:
                xMovement: int = direction[0] * scale
                yMovement: int = direction[1] * scale
                moveToX: int = piece.x + xMovement
                moveToY: int = piece.y + yMovement
                # Check if not out of board
                if moveToX in range(8) and moveToY in range(8):
                    # Check if there is no friendly piece
                    if target := getBoard(moveToX, moveToY):
                        if target.team != piece.team and target.status[0] != 'immune':
                            # Kill and block further movement
                            moves.append([xMovement, yMovement, 'k'])
                        # A piece is in the way
                        break
                    else:
                        # Normal move
                        if scale == 1:
                            moves.append([xMovement, yMovement, ''])
                        elif not getBoard(moveToX, moveToY):
                            moves.append([xMovement, yMovement, 'a'])
                else:
                    break
        return moves
    if piece.name == 'queen':
        # Queen's ability
        if getAbility(piece.team, 4) == 0 and piece.charge == 1:
            for trap in findPieces(piece.team, 'trap'):
                xMovement = trap.x - piece.x
                yMovement = trap.y - piece.y
                moves.append([xMovement, yMovement, 'a'])
        return moves
    return moves

# Find every piece of selected team and type
def findPieces(team: int, name: str) -> list[Piece]:
    found = []
    for y in range(8):
        for x in range(8):
            # Check if there is a piece
            if cell := getBoard(x, y):
                # Check if its a piece we are looking for
                if cell.team == team and cell.name == name:
                    found.append(cell)
    return found

# Draws a move on the board
def drawMove(x, y, moveType):
    global screen
    if flipBoard:
        drawX: int = 7 - x
        drawY: int = y
    else:
        drawX: int = x
        drawY: int = 7 - y
    if moveType == 'k':
        filename = 'kill'
    elif moveType == 'a':
        filename = 'ability'
    else:
        filename = 'normal'
    screen.blit(pygame.image.load(f'sprites/moves/{filename}.png'), (160 + drawX * 80, drawY * 80))

# Called if player clicks on board
selected: Piece|bool = False
possibleMoves: list[list[int,int,str]] = []
def boardClick(screenX: int, screenY: int) -> None:
    global selected, possibleMoves, playerMove, material, movesToDraw, Board, buttons, buttonIds
    if flipBoard:
        boardX: int = 7 - math.floor(screenX / 80)
        boardY: int = math.floor(screenY / 80)
    else:
        boardX: int = math.floor(screenX / 80)
        boardY: int = 7 - math.floor(screenY / 80)
    # Try to select a piece
    if not selected:
        selected = getBoard(boardX, boardY)
        if selected:
            # Traps and enemy pieces are uncontrollable
            if selected.team == playerMove and selected.name != 'trap':
                moves = getMoves(selected)
                for moveData in moves:
                    moveToX = selected.x + moveData[0]
                    moveToY = selected.y + moveData[1]
                    possibleMoves.append([moveToX, moveToY, moveData[2]])
                buttons.clear()
                buttonIds.clear()
    # Try to move a piece
    else:
        if [boardX, boardY, ''] in possibleMoves:
            fromPos = [selected.x, selected.y]
            move(selected, [boardX, boardY])
            # Queen's abilities
            if selected.name == 'queen':
                toSpawn: str = 'trap' if getAbility(playerMove, 4) == 0 else 'zombie'
                lifetime: int = 2 if getAbility(playerMove, 4) == 0 else 3
                summoned = Piece(playerMove, toSpawn, -1, -1)
                move(summoned, fromPos, False)
                summoned.status = ['summoned', lifetime]
            # Charge move based cooldown abilities
            if selected.name in ['rook', 'bishop']:
                for piece in findPieces(selected.team, selected.name):
                    if piece.charge < 3: piece.charge += 1
            if selected.name == 'knight':
                for knight in findPieces(selected.team, 'knight'):
                    if knight.charge < 4: knight.charge += 1
            # Reverse
            startMove(int(not playerMove))                    
            deselect()
        elif [boardX, boardY, 'k'] in possibleMoves:
            target = getBoard(boardX, boardY)
            move(selected, [boardX, boardY])
            if target.name != 'king':
                # Change material and kill list
                if not target.name in ['trap', 'zombie']:
                    material[target.team] -= target.cost
                    kills[playerMove].append(target.name)
                # King's active
                if target.name == 'queen' and getAbility(playerMove, 5) == 0:
                    findPieces(playerMove, 'king')[0].charge = 1
                # Bishop's passive
                if target.name == 'bishop' and getAbility(target.team, 3) == 1 and selected.status[0] != 'immune':
                    material[playerMove] -= selected.cost
                    kills[target.team].append(selected.name)
                    Board[boardY][boardX] = False
                # Pawn's active
                if selected.name == 'pawn' and getAbility(playerMove, 0) == 0:
                    if selected.charge < 2: selected.charge += 2
                # Knight's passive
                if selected.name == 'knight' and getAbility(playerMove, 2) == 1 and target.cost >= 5:
                    pass
                else:
                    # Reverse
                    startMove(int(not playerMove))
            else:
                gameOver(playerMove)
            deselect()
            # TODO boshop's passive
        elif [boardX, boardY, 'a'] in possibleMoves:
            useAbility(selected, [boardX, boardY])
            deselect()
        else:         
            # If there is a piece, try to select it
            deselect()
            selected = getBoard(boardX, boardY)
            if selected:
                # Traps and enemy pieces are uncontrollable
                if selected.team == playerMove and selected.name != 'trap':
                    moves = getMoves(selected)
                    for moveData in moves:
                        moveToX = selected.x + moveData[0]
                        moveToY = selected.y + moveData[1]
                        possibleMoves.append([moveToX, moveToY, moveData[2]])
                else:
                    deselect()

# Deselect a piece
def deselect() -> None:
    global selected, possibleMoves, buttons, buttonIds
    selected = False
    possibleMoves = []
    buttons.clear()
    buttonIds.clear()

# Block controls and shown the winner
def gameOver(team) -> None:
    global run, isGameOver, winner
    isGameOver = True
    buttons.clear()
    buttonIds.clear()    
    winner = team

# Making text on the screen easier
def scrText(x: int, y: int, msg: str, color: tuple, mini: bool = False) -> None:
    global FONT, FONT_MINI, screen
    font = FONT_MINI if mini else FONT
    text = font.render(msg, False, color)
    textBox = text.get_rect(center=(x, y))
    screen.blit(text, textBox)
    
# Making rects easier
def scrRect(x: int, y: int, w: int, h: int, color: tuple) -> pygame.rect.Rect:
    global screen
    rect = pygame.Rect(x, y, w, h)
    drawnRect = pygame.draw.rect(screen, color, rect)
    return drawnRect

# Make a button
def button(bid: int, area: pygame.rect.Rect, func: callable, arg: str='') -> None:
    global buttons, buttonIds
    if not bid in buttonIds:
        buttons.append([area, func, arg])
        buttonIds.add(bid)

# All things that should be done every move
def startMove(team: int, skipped: int = False):
    global Board, playerMove, moveCount, skipChain, moveStartTime
    cancelSpecialMove('')
    deselect()
    playerMove = team
    # Status duration countdown
    for trap in findPieces(team, 'trap'):
        trap.status[1] -= 1
        if trap.status[1] == 0:
            Board[trap.y][trap.x] = False
    for zombie in findPieces(team, 'zombie'):
        zombie.status[1] -= 1
        if zombie.status[1] == 0:
            Board[zombie.y][zombie.x] = False
    findPieces(team, 'king')[0].status = ['none', 0]
    if getAbility(team, 0) == 1 and len(findPieces(team, 'pawn')) >= 6:
        findPieces(team, 'king')[0].status = ['immune', 1]
    moveCount += 1
    # Tie on skip chain
    if skipped:
        skipChain += 1
        if skipChain >= 6:
            gameOver(-1)
    else:
        skipChain = 0
    # Timer
    if moveCount > 2:
        if moveCount > 3:
            timer[int(not team)] += int(time.time()) - moveStartTime
        currentTime = int(time.time())
        moveStartTime = currentTime

# Checks if player can castle left
def canLeftCastle(team: int) -> bool:
    if getBoard(0, team * 7).name != 'rook' or getBoard(0, team * 7).team != team:
        return False
    elif getBoard(1, team * 7) or getBoard(2, team * 7) or getBoard(3, team * 7):
        return False
    else:
        return True

# Checks if player can castle right
def canRightCastle(team: int) -> bool:
    if getBoard(7, team * 7).name != 'rook' or getBoard(7, team * 7).team != team:
        return False
    elif getBoard(5, team * 7) or getBoard(6, team * 7):
        return False
    else:
        return True
    
# All in-game buttons
def randomiseAbilities(team: str) -> None:
    #for piece in range(6): - no rook passive for now
    for piece in [0, 2, 3, 4, 5]:
        selectAbility(f'{team}{piece}', randint(0,1)) 
def bugReport(_) -> None:
    global mainMenuText
    mainMenuText = []
    mainMenuText.append('To report a bug, contact me on discord:')
    mainMenuText.append('leyn1092')
    mainMenuText.append('')
    mainMenuText.append('Please, say that you are reporting a bug!')
    mainMenuText.append('(or high chance you will get blocked)')
def showGuide(_) -> None:
    global mainMenuText, Guide
    mainMenuText = Guide
def selectAbility(team_piece: str, abil: int = -1) -> None:
    global Abils, mainMenuText
    team = int(team_piece[0])
    pieceId = int(team_piece[1])
    if abil == -1:
        abil = int(not getAbility(team, pieceId))
        word = 'active' if abil == 0 else 'passive'
        mainMenuText = [f'{getName(pieceId).upper()}\'s {word}']
        mainMenuText += AbilDescr[pieceId][abil]
    Abils[team][pieceId] = abil
def startGame(_) -> None:
    global buttons, buttonIds, isGameStarted
    isGameStarted = True
    # Auto charge abilities
    for team in range(2):
        if getAbility(team, 1) == 0:
            for rook in findPieces(team, 'rook'):
                rook.charge = 3
        if getAbility(team, 3) == 0:
            for bishop in findPieces(team, 'bishop'):
                bishop.charge = 3
        if getAbility(team, 4) == 0:
            findPieces(team, 'queen')[0].charge = 1
        if getAbility(team, 5) == 0:
            findPieces(team, 'king')[0].charge = 1
    # Clear buttons to save memory
    buttons.clear()
    buttonIds.clear()
    startMove(0)
def deselectButton(_) -> None:
    deselect()
def skipMove(_) -> None:
    deselect()
    startMove(int(not playerMove), True)
def specialMove(_):
    global drawInsteadOfMove
    if selected.id == 0:
        drawInsteadOfMove = ['promote', selected.team, selected.x]
    elif selected.id == 5:
        drawInsteadOfMove = ['castle', selected.team]
def cancelSpecialMove(_) -> None:
    global drawInsteadOfMove, buttons, buttonIds
    drawInsteadOfMove = ['none']
    # I cant think of better solution
    buttons.clear()
    buttonIds.clear()
def promote(promoteTo: str) -> None:
    global Board, material
    Board[selected.y][selected.x] = Piece(selected.team, promoteTo, selected.x, selected.y)
    material[selected.team] -= 1
    material[selected.team] += getCost(promoteTo)
    cancelSpecialMove('')
    deselect()
def castle(direction: str) -> None:
    if direction == 'left':
        x: int = 0
        anchor: int = -1
        kingMovement: int = -2
    elif direction == 'right':
        x: int = 7
        anchor: int = 1
        kingMovement: int = 2
    move(getBoard(x, selected.team * 7), (selected.x + anchor, selected.y))
    move(selected, (selected.x + kingMovement, selected.y))
    cancelSpecialMove('')
    deselect()
    startMove(int(not playerMove))
def flipBoardButton(_) -> None:
    global flipBoard
    flipBoard = not flipBoard

# Now it's time for pygame
pygame.init()
screen = pygame.display.set_mode((960, 720))

# Presets
mainMenuText: list[str] = ['CHESS - ABILITY DRAFT', 'Made by LEYN1092']
WHITE = (255, 255, 255)
GRAY = (120, 128, 136)
DARK_GRAY = (60, 64, 68)
BLACK = (0, 0, 0)
WHITEISH = (223, 223, 223)
BLACKISH = (32, 32, 32)
FONT = pygame.font.SysFont('consolas', 24)
FONT_MINI = pygame.font.SysFont('arialblack', 16)
isGameStarted: bool = False
isGameOver: bool = False
# buttons[button[pygame.rect.Rect, function, arg]] to acces
buttons: list[list] = []
buttonIds: set = set()
kills: list[list[str]] = [[], []]
material: list[int] = [0, 0]
moveCount: int = 1
skipChain: int = 0
winner = None
drawInsteadOfMove: list = ['none']
runTimer: bool = True
timer: list[int] = [0, 0]
moveStartTime: int = 0
flipBoard: bool = False

print('Loading finished')

# Main game loop
while True:
    # Limit 30 fps (you dont need more for chess trust me)
    pygame.time.Clock().tick(30)

    for event in pygame.event.get():
        # Exit without an error
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Click handler
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not isGameOver:
            mousePos = pygame.mouse.get_pos()
            for b in buttons:
                # b[0] is an area, b[1] is function
                if b[0].collidepoint(mousePos):
                    b[1](b[2])
            # Detect board click
            if isGameStarted:
                if mousePos[0] > 160 and mousePos[0] < 800 and mousePos[1] < 640:
                    boardClick(mousePos[0] - 160, mousePos[1])

    # Backgrounds
    screen.fill(DARK_GRAY)
    scrRect(0, 0, 160, 720, WHITE) # White team BG
    scrRect(800, 0, 160, 720, BLACK) # Black team BG
    scrRect(160, 640, 640, 80, GRAY) # Toolbar BG
    scrText(80, 40, 'WHITE', BLACKISH)
    scrText(880, 40, 'BLACK', WHITEISH)
    
    if not isGameStarted:
        # Randomise abilities buttons
        button(0, scrRect(160+10, 640+10, 60, 60, WHITEISH), randomiseAbilities, '0')
        button(1, scrRect(240+10, 640+10, 60, 60, BLACKISH), randomiseAbilities, '1')
        scrText(240, 640-20, 'Random Abils', GRAY, True)
        dices = [pygame.image.load(f'sprites/buttons/{team}_dice.png') for team in ['white', 'black']]
        screen.blit(dices[0], (160+10, 640+10))
        screen.blit(dices[1], (240+10, 640+10))
        # Bug report
        button(2, scrRect(640+10, 640+10, 60, 60, (128, 0, 0)), bugReport)
        scrText(640+40, 640-20, 'Bug', GRAY, True)
        screen.blit(pygame.image.load('sprites/buttons/warning.png'), (640+10, 640+10))
        # Guide
        button(3, scrRect(720+10, 640+10, 60, 60, (0, 128, 0)), showGuide)
        scrText(720+40, 640-20, 'Guide', GRAY, True)
        screen.blit(pygame.image.load('sprites/buttons/book.png'), (720+10, 640+10))
        
        # Create ability selection buttons
        for team in range(2):
            for piece in range(6):
                startX: int = team * 800
                startY: int = piece * 80 + 80
                xOffset: int = getAbility(team, piece) * 80
                # Ids from 4 to 15
                button(4 + piece + team * 6, scrRect(startX+5, startY+5, 150, 70, GRAY), selectAbility, f'{team}{piece}')
                # Sprite
                screen.blit(pygame.image.load(f'sprites/pieces/{team}/{piece}.png'), (startX+xOffset, startY))
                # Black text for white team, white text for black team
                scrText(startX+40, startY+40, '1', (255*team, 255*team, 255*team))
                scrText(startX+120, startY+40, '2', (255*team, 255*team, 255*team))
        
        # Create play button
        button(16, scrRect(320+10, 640+10, 300, 60, (0, 0, 128)), startGame)
        scrText(480, 640+40, 'PLAY', WHITEISH)
        
        # Write main menu text
        for lineId in range(len(mainMenuText)):
            # Max negative = max positive = half of length
            yOffset: int = (-len(mainMenuText)/2 + lineId) * 32
            scrText(480, 320 + yOffset, mainMenuText[lineId], WHITEISH)
    # Show board and allow moves
    else:
        if not isGameOver:
            # Material advantage
            whitePositive: bool = material[0]-material[1] >= 0
            blackPositive: bool = material[1]-material[0] >= 0
            plus = '+' if whitePositive else ''
            scrText(80, 100, f'{plus}{material[0]-material[1]}', (128-128*whitePositive, 128*whitePositive, 0))
            plus = '+' if blackPositive else ''
            scrText(880, 100, f'{plus}{material[1]-material[0]}', (255-255*blackPositive, 255*blackPositive, 0))
            # Draw board
            boardImg = pygame.image.load('sprites/board.png')
            if flipBoard:
                boardImg = pygame.transform.rotate(boardImg, 180)
            screen.blit(boardImg, (160, 0))
            # Toolbar ingame buttons
            if selected:
                # Deselect button
                button(17, scrRect(160+10, 640+10, 60, 60, DARK_GRAY), deselectButton)
                screen.blit(pygame.image.load('sprites/buttons/cancel.png'), (160+10, 640+10))
                # Special move button if not pressed, cancel special move instead
                if drawInsteadOfMove[0] == 'none':
                    # Active button if piece can use special move
                    if selected.id in [0, 5]:
                        button(18, scrRect(240+10, 640+10, 60, 60, (0, 128, 0)), specialMove)
                        screen.blit(pygame.image.load('sprites/buttons/wand.png'), (240+10, 640+10))
                    else:
                        scrRect(240+10, 640+10, 60, 60, DARK_GRAY)
                        screen.blit(pygame.image.load('sprites/buttons/wand_gray.png'), (240+10, 640+10))
                else:
                    button(21, scrRect(240+10, 640+10, 60, 60, (0, 128, 0)), cancelSpecialMove)
                    screen.blit(pygame.image.load('sprites/buttons/cancel_green.png'), (240+10, 640+10))
            else:
                # Flip board button
                flipButtonColor = WHITE if flipBoard == 0 else BLACK
                button(29, scrRect(160+10, 640+10, 60, 60, flipButtonColor), flipBoardButton)
                screen.blit(pygame.image.load(f'sprites/buttons/flip_{int(flipBoard)}.png'), (160+10, 640+10))
            # Discord button?
            # button(?, scrRect(640+10, 640+10, 60, 60, (0, 0, 128)), discord)
            # screen.blit(pygame.image.load('sprites/buttons/discord.png'), (640+10, 640+10))
            # Skip move button
            button(20, scrRect(720+10, 640+10, 60, 60, (128, 0, 0)), skipMove)
            screen.blit(pygame.image.load('sprites/buttons/skip.png'), (720+10, 640+10))
            playerMoveColor: tuple = WHITE if playerMove == 0 else BLACK
            # Last button id: 29
            
            # Promote buttons
            if drawInsteadOfMove[0] == 'promote':
                for pieceId in range(1, 5):
                    team: int = drawInsteadOfMove[1]
                    pieceImage = pygame.image.load(f'sprites/pieces/{team}/{pieceId}.png')
                    scrRect(320+80*(pieceId-1)+10, 640+10, 60, 60, DARK_GRAY)
                    if selected.y == int(not selected.team) * 7:
                        # Ids from 22 to 27
                        button(21+pieceId, screen.blit(pieceImage, (320+80*(pieceId-1), 640)), promote, getName(pieceId))
            # Castle buttons
            elif drawInsteadOfMove[0] == 'castle':
                team: int = drawInsteadOfMove[1]
                teamColor: tuple = WHITE if team == 0 else BLACK
                # Left castle
                leftCastleButton = scrRect(320+10, 640+10, 140, 60, teamColor)
                if canLeftCastle(team) and selected.x == 4 and selected.y == selected.team * 7:
                    button(28, leftCastleButton, castle, 'left')
                    screen.blit(pygame.image.load('sprites/buttons/arrow_left.png'), (320+10, 640+10))
                else:
                    screen.blit(pygame.image.load('sprites/buttons/arrow_left_gray.png'), (320+10, 640+10))
                # Right castle
                rightCastleButton = scrRect(480+10, 640+10, 140, 60, teamColor)
                if canRightCastle(team) and selected.x == 4 and selected.y == selected.team * 7:
                    button(28, rightCastleButton, castle, 'right')
                    screen.blit(pygame.image.load('sprites/buttons/arrow_right.png'), (480+10, 640+10))
                else:
                    screen.blit(pygame.image.load('sprites/buttons/arrow_right_gray.png'), (480+10, 640+10))
            # Draw which player's move instead
            else:
                scrRect(320+10, 640+10, 300, 60, playerMoveColor)
                playerMoveText: str = 'WHITE' if playerMove == 0 else 'BLACK'
                scrText(480, 680, f'{playerMoveText}\'s move {moveCount//2}', (255*playerMove, 255*playerMove, 255*playerMove))
                
        # Show game over screen
        else:
            # Draw game over
            if winner != None:
                if winner == 0:
                    winText: str = 'WHITE\'s victory!'
                    winColor: tuple = WHITE
                    winTextColor: tuple = BLACK
                elif winner == 1:
                    winText: str = 'BLACK\'s victory!'
                    winColor: tuple = BLACK
                    winTextColor: tuple = WHITE
                else:
                    winText: str = 'DRAW!'
                    winColor: tuple = DARK_GRAY
                    winTextColor: tuple = GRAY
                scrRect(320+10, 640+10, 300, 60, winColor)
                scrText(480, 680, winText, winTextColor)
                # Draw star and torn effect
                if winner >= 0:
                    screen.blit(pygame.image.load(f'sprites/star.png'), (800 * winner, 560))
                    screen.blit(pygame.image.load(f'sprites/torn.png'), (800 * (not winner), 560))
                    
        # Draw alive pieces
        for x in range(8):
            for y in range(8):
                if cell := getBoard(x, y):
                    if flipBoard:
                        drawX: int = 7 - x
                        drawY: int = y
                    else:
                        drawX: int = x
                        drawY: int = 7 - y
                    # Draw an ability circle
                    if cell.id <= 5:
                        if getAbility(cell.team, cell.id) == 0:
                            screen.blit(pygame.image.load(f'sprites/abilities/{cell.id}/{cell.charge}.png'), (160 + drawX*80+2, drawY*80+2))
                    # Draw a piece
                    screen.blit(pygame.image.load(f'sprites/pieces/{cell.team}/{cell.id}.png'), (160 + drawX*80, drawY*80))
                    # Draw an effect
                    if cell.status[0] != 'none':
                        screen.blit(pygame.image.load(f'sprites/effects/{cell.status[0]}/{cell.status[1]}.png'), (160 + drawX*80+2, drawY*80+2))
                        
        # Draw timer
        for team in range(2):
            timeToDraw: int = timer[team]
            if team == playerMove and moveCount > 2:
                timeToDraw += int(time.time()) - moveStartTime
            hrs: int = timeToDraw // 3600
            mins: int = (timeToDraw % 3600) // 60
            secs: int = timeToDraw % 60
            startX: int = 800 * team + 80
            startY: int = 140
            scrText(startX, startY, f'-{hrs:0>2}:{mins:0>2}:{secs:0>2}', GRAY)
            
        # Draw killed pieces
        for team in range(2):
            for kill in range(len(kills[team])):
                startX: int = 800 * team
                startY: int = 160
                xOffset: int = 40 * (kill%4)
                yOffset: int = 40 * (kill//4)
                screen.blit(pygame.image.load(f'sprites/pieces/{int(not team)}/mini/{getId(kills[team][kill])}.png'), (startX + xOffset, startY + yOffset))
        # Draw moves
            for moveData in possibleMoves:
                drawMove(moveData[0], moveData[1], moveData[2])
    # Draw flush
    pygame.display.flip()