DEFAULT_FONT = 'fonts/base.ttf'
FONT_SCALE = 7
NAME = 'English'

def get(key: str) -> str:
    if key in gettable.keys():
        return gettable[key]
    return f'<{key}>'

Ability = [
    # Pawn
    [
        ['!h', 'Adrenaline',
         'Can move 2 squares forward from any square.',
         'Cooldown: 1 kill, separate for every piece.'],
        ['!h', 'Occultism',
         'King is in ghost form while 6 or more ally',
         'pawns are on the board.']
    ],
    # Rook
    [
        ['!h', 'Secret Passage',
         'Can swap with a friendly piece in reach.',
         'Cooldown: 3 normal rook moves.',
         'Charged.'],
        ['!h', 'Shackles',
         'After making a normal move, if the next piece',
         'in that direction is an enemy, it becomes',
         'Locked for 1 turn.']
    ],
    # Knight
    [
        ['!h', 'Trotting',
         'Can move 3 squares straight.',
         'Cooldown: 4 normal knight moves.'],
        ['!h', 'Momentum',
         'When kills a rook or a queen, you can make',
         'another move.']
    ],
    # Bishop
    [
        ['!h', 'Shift',
         'Can go 1 square in any direction.',
         'Cooldown: 3 normal bishop moves.'],
        ['!h', 'Poison',
         'The piece that killed this dies in 3 turns.']
    ],
    # Queen
    [
        ['!h', 'Conjuration',
         'Leaves traps for 2 turns every normal move.',
         'Can teleport to any trap.',
         'Instant. Charged. Once per game.'],
        ['!h', 'Necromancy',
         'Leaves a controllable zombie pawn that dies',
         'in 3 turns every normal move.']
    ],
    # King
    [
        ['!h', 'Divine Shield',
         'Becomes invincible for 1 turn.',
         'Instant. Charged. Once per game.'],
        ['!h', 'Rush',
         'Can move (but not take) 2 squares straight.']
    ]
]
Guide = [
    ['1/3',
     '!h', 'King and Game Changes',
     'Game ends when one of the kings dies.',
     'There are no checks, mates and stalemates.',
     'Player can skip their turn.',
     'Draw is called if both players skip 3 turns',
     'in a row.',
     'You can castle from correct posotion even if',
     'the king was moved.'],
    ['2/3',
     '!h', 'Special Moves',
     'There is no en passant.',
     'A green dot is normal a move.',
     'A dot with red outlile is a kill move.',
     'A dot with yellow outline is an ability move.',
     'To promote a pawn or castle press the wand button.',
     'To skip your turn press the red arrow button.',
     'To deselect a piece press the gray X button.'],
    ['3/3',
     '!h', 'Keywords',
     'Instant: You can make a move after using this',
     'ability.',
     'Charged: This ability is ready when the game',
     'starts.',
     'Ghost form: Piece cannot take or be taken.',
     'Locked: Cannot move this piece.']
]
BugReport = [
    'To report a bug open an issue on github:',
    'github.com/Leyn-pl/ChessAbilityDraft/issues',
    '',
    '(this link is present in feedback.txt)'
]
gettable = {
    'chess': 'CHESS',
    'active': 'active',
    'passive': 'passive',
    'play': 'PLAY',
    'credit': 'Made by LEYN1092',
    'randomise': 'Random Abils',
    'bug': 'Bug',
    'guide': 'Guide',
    'white': 'WHITE',
    'black': 'BLACK',
    'pawn': 'PAWN',
    'rook': 'ROOK',
    'knight': 'KNIGHT',
    'bishop': 'BISHOP',
    'queen': 'QUEEN',
    'king': 'KING',
    's': '\'s ',
    'turn': 'turn',
    'victory': 'victory!',
    'draw': 'DRAW!'
}