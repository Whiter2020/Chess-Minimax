import chess

PIECE_VALUES = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0
}

def evaluate_board(board):
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -999999
        else:
            return 999999

    if board.is_stalemate():
        return 0

    if board.is_insufficient_material():
        return 0

    if board.can_claim_draw():
        return 0

    score = 0

    for square, piece in board.piece_map().items():
        value = PIECE_VALUES[piece.piece_type]

        if piece.color == chess.WHITE:
            score += value
        else:
            score -= value

    return score