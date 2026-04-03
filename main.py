import pygame
import chess
import time
from gui import draw_board, draw_pieces, draw_moves, SQ_SIZE
from minimax import find_best_move

pygame.init()

WIDTH = 640

screen = pygame.display.set_mode((WIDTH, WIDTH))
font = pygame.font.Font(None, 72)

board = chess.Board()

pieces = {}

names = [
    "wp","bp","wr","br","wn","bn",
    "wb","bb","wq","bq","wk","bk"
]

for name in names:
    img = pygame.image.load(f"assets/{name}.svg")
    img = pygame.transform.scale(img, (SQ_SIZE, SQ_SIZE))
    pieces[name] = img

selected = None
legal_targets = []
running = True

message = None
message_color = (255, 255, 255)
message_time = 0

promotion_square = None
promotion_from = None
promotion_color = None
clock = pygame.time.Clock()

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and message is None:

            if promotion_square is not None:
                x, y = pygame.mouse.get_pos()
                index = x // (SQ_SIZE * 2)

                if index < 4:
                    options = [chess.QUEEN, chess.ROOK, chess.BISHOP, chess.KNIGHT]
                    promo_piece = options[index]

                    move = chess.Move(
                        promotion_from,
                        promotion_square,
                        promotion=promo_piece
                    )

                    if move in board.legal_moves:
                        board.push(move)

                        
                        best_move = find_best_move(board, depth=3)  

                        if best_move:  
                            board.push(best_move)  

                            if board.is_game_over():  
                                result = board.result()  
                                if result == "1-0":  
                                    message = "WHITE WIN"  
                                    message_color = (0, 255, 0)  
                                elif result == "0-1":  
                                    message = "BLACK WIN"  
                                    message_color = (255, 0, 0)  
                                else:  
                                    message = "DRAW"  
                                    message_color = (255, 255, 255)  
                                message_time = time.time()  

                promotion_square = None
                promotion_from = None
                promotion_color = None
                continue

            x, y = pygame.mouse.get_pos()

            col = x // SQ_SIZE
            row = y // SQ_SIZE

            square = chess.square(col, 7 - row)
            piece = board.piece_at(square)

            if selected is None:
                if piece and piece.color == board.turn:
                    selected = square
                    legal_targets = [
                        move.to_square
                        for move in board.legal_moves
                        if move.from_square == selected
                    ]

            else:
                piece = board.piece_at(selected)

                w
                move = chess.Move(selected, square)

                if move in board.legal_moves:
                    board.push(move)

                    if board.is_game_over():
                        result = board.result()
                        if result == "1-0":
                            message = "WHITE WIN"
                            message_color = (0, 255, 0)
                        elif result == "0-1":
                            message = "BLACK WIN"
                            message_color = (255, 0, 0)
                        else:
                            message = "DRAW"
                            message_color = (255, 255, 255)
                        message_time = time.time()
                        selected = None
                        legal_targets = []
                        continue

                    if promotion_square is not None:
                        continue

                    best_move = find_best_move(board, depth = 3)  

                    if best_move:  
                        board.push(best_move)  

                        if board.is_game_over():
                            result = board.result()
                            if result == "1-0":
                                message = "WHITE WIN"
                                message_color = (0, 255, 0)
                            elif result == "0-1":
                                message = "BLACK WIN"
                                message_color = (255, 0, 0)
                            else:
                                message = "DRAW"
                                message_color = (255, 255, 255)
                            message_time = time.time()

                selected = None
                legal_targets = []

    draw_board(screen)
    draw_moves(screen, legal_targets)
    draw_pieces(screen, board, pieces)

    if promotion_square is not None:
        options = ["q", "r", "b", "n"]

        for i, p in enumerate(options):
            key = ("w" if promotion_color == chess.WHITE else "b") + p
            img = pieces[key]

            x = i * SQ_SIZE * 2
            y = WIDTH // 2 - SQ_SIZE

            rect = pygame.Rect(x, y, SQ_SIZE*2, SQ_SIZE*2)
            pygame.draw.rect(screen, (50, 50, 50), rect)
            screen.blit(img, (x + SQ_SIZE//2, y + SQ_SIZE//2))

    if message:
        text = font.render(message, True, message_color)
        rect = text.get_rect(center=(WIDTH // 2, WIDTH // 2))
        screen.blit(text, rect)

        if time.time() - message_time > 3:
            board = chess.Board()
            selected = None
            legal_targets = []
            message = None

    pygame.display.flip()
    clock.tick(60)