from Evaluation import Evalualtion

MAX, MIN = 100000, -100000

def minimax(depth, maximizingPlayer, alpha, beta, board, firstMove):

    
    if (depth == 0) or (board.is_game_over()):

        if maximizingPlayer:
            eval = Evalualtion(board, "W")
        else:
            eval = Evalualtion(board, "B")

        return eval.result()

    
    if maximizingPlayer:

        best = MIN
        
        for i in board.legal_moves:

            board.push(i)

            if checkmate(board) and firstMove:
                return i

            val = minimax(depth - 1, False, alpha, beta, board, False)
            board.pop()

            if val > best:
                best = val
                best_move_white = i

            alpha = max(alpha, best)

            
            if beta <= alpha:
                break

        if firstMove:
            print(best_move_white)
            return best_move_white
        else:
            return best

    else:

        best = MAX
        for i in board.legal_moves:

            board.push(i)

            if checkmate(board) and firstMove:
                return i

            val = minimax(depth - 1, True, alpha, beta, board, False)
            board.pop()

            if val < best:
                best = val
                best_move_black = i

            beta = min(beta, best)

        
            if beta <= alpha:
                break

        if firstMove:
            return best_move_black
        else:
            return best

def checkmate(board):
    if board.is_checkmate():
        return True
    else:
        return False




