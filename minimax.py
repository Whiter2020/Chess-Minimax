import chess
from evaluation import evaluate_board

def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return evaluate_board(board)

    legal_moves = list(board.legal_moves)

    if maximizing_player:
        max_eval = -float("inf")

        for move in legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, False)
            board.pop()

            if eval_score > max_eval:
                max_eval = eval_score

            if eval_score > alpha:
                alpha = eval_score

            if beta <= alpha:
                break

        return max_eval

    else:
        min_eval = float("inf")

        for move in legal_moves:
            board.push(move)
            eval_score = minimax(board, depth - 1, alpha, beta, True)
            board.pop()

            if eval_score < min_eval:
                min_eval = eval_score

            if eval_score < beta:
                beta = eval_score

            if beta <= alpha:
                break

        return min_eval


def find_best_move(board, depth = 5):
    legal_moves = list(board.legal_moves)

    if not legal_moves:
        return None

    best_move = None

    if board.turn == chess.WHITE:
        best_score = -float("inf")

        for move in legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, -float("inf"), float("inf"), False)
            board.pop()

            if score > best_score:
                best_score = score
                best_move = move

    else:
        best_score = float("inf")

        for move in legal_moves:
            board.push(move)
            score = minimax(board, depth - 1, -float("inf"), float("inf"), True)
            board.pop()

            if score < best_score:
                best_score = score
                best_move = move

    return best_move