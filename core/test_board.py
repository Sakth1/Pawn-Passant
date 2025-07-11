import chess

def print_board(board):
    print(board.unicode(borders=True))

def main():
    board = chess.Board()
    move_history = []

    while not board.is_game_over():
        print_board(board)
        print(f"\nTurn: {'White' if board.turn == chess.WHITE else 'Black'}")
        move_input = input("Enter your move (e.g., e2e4 or type 'undo' to revert): ").strip()

        if move_input.lower() == "undo":
            if move_history:
                board.pop()
                move_history.pop()
                print("Undid last move.")
            else:
                print("No moves to undo.")
            continue

        try:
            move = chess.Move.from_uci(move_input)
            if move in board.legal_moves:
                san = board.san(move)  # 🔧 Get SAN before pushing
                board.push(move)
                move_history.append(move)
                print(f"Played move: {san}")
            else:
                print("Illegal move.")
        except ValueError:
            print("Invalid input format. Use UCI format like 'e2e4'.")

    print_board(board)
    result = board.result()
    print(f"\nGame Over. Result: {result}")

if __name__ == "__main__":
    main()
