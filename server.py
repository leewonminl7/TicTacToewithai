from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import random

app = Flask(__name__)
CORS(app)

class TicTacToe:
    def __init__(self):
        self.board = [" " for _ in range(9)]
        self.current_winner = None

    def available_moves(self):
        return [i for i, spot in enumerate(self.board) if spot == " "]

    def make_move(self, position, letter):
        if self.board[position] == " ":
            self.board[position] = letter
            if self.check_winner(position, letter):
                self.current_winner = letter
            return True
        return False

    def check_winner(self, position, letter):
        row_index = position // 3
        row = self.board[row_index*3:(row_index+1)*3]
        if all([spot == letter for spot in row]):
            return True

        col_index = position % 3
        col = [self.board[col_index+i*3] for i in range(3)]
        if all([spot == letter for spot in col]):
            return True

        if position % 2 == 0:
            diagonal1 = [self.board[i] for i in [0, 4, 8]]
            diagonal2 = [self.board[i] for i in [2, 4, 6]]
            if all([spot == letter for spot in diagonal1]) or all([spot == letter for spot in diagonal2]):
                return True
        return False

    def is_draw(self):
        return " " not in self.board and self.current_winner is None

    def computer_move(self, difficulty):
        available = self.available_moves()

        if difficulty == "easy":
            return random.choice(available) if available else None

        elif difficulty == "medium":
            for move in available:
                self.board[move] = "X"
                if self.check_winner(move, "X"):
                    self.board[move] = " "
                    return move
                self.board[move] = " "

            return random.choice(available) if available else None

        elif difficulty == "hard":
            return self.get_best_move("O")

        return None

    def get_best_move(self, letter):
        best_score = -float("inf")
        best_move = None

        for move in self.available_moves():
            self.board[move] = letter
            if self.check_winner(move, letter):
                return move 
            score = self.minimax(False, letter)
            self.board[move] = " "
            self.current_winner = None
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def minimax(self, is_maximizing, letter):
        opponent = "X" if letter == "O" else "O"

        if self.current_winner == letter:
            return 1
        elif self.current_winner == opponent:
            return -1
        elif not self.available_moves():
            return 0

        if is_maximizing:
            best_score = -float("inf")
            for move in self.available_moves():
                self.board[move] = letter
                if self.check_winner(move, letter):
                    self.current_winner = letter
                score = self.minimax(False, letter)
                self.board[move] = " "
                self.current_winner = None
                best_score = max(score, best_score)
            return best_score
        else:
            best_score = float("inf")
            for move in self.available_moves():
                self.board[move] = opponent
                if self.check_winner(move, opponent):
                    self.current_winner = opponent
                score = self.minimax(True, letter)
                self.board[move] = " "
                self.current_winner = None
                best_score = min(score, best_score)
            return best_score

game = TicTacToe()

@app.route("/")
def serve_frontend():
    return send_from_directory(".", "index.html")

@app.route("/move", methods=["POST"])
def player_move():
    data = request.json
    position = data.get("position")
    difficulty = data.get("difficulty", "easy")

    if position not in game.available_moves():
        return jsonify({"error": "Invalid move"}), 400

    game.make_move(position, "X")
    if game.current_winner:
        return jsonify({"board": game.board, "winner": "Player"})

    if game.is_draw():
        return jsonify({"board": game.board, "winner": "Draw"})

    ai_move = game.computer_move(difficulty)
    if ai_move is not None:
        game.make_move(ai_move, "O")

    if game.current_winner:
        return jsonify({"board": game.board, "winner": "AI"})

    if game.is_draw():
        return jsonify({"board": game.board, "winner": "Draw"})

    return jsonify({"board": game.board, "ai_move": ai_move})

@app.route("/reset", methods=["POST"])
def reset_game():
    global game
    game = TicTacToe()
    return jsonify({"message": "Game reset!"})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5006, debug=True) 