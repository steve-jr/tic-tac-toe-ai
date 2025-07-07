from flask import Flask, render_template, jsonify, request, session
import secrets
from tictactoe import initial_state, minimax, result, terminal, winner, player

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management


# Store game states in session
def get_board():
    """Get current board from session, or create new one"""
    if 'board' not in session:
        session['board'] = initial_state()
    return session['board']


def set_board(board):
    """Update board in session"""
    session['board'] = board


def get_human_player():
    """Get human player symbol from session"""
    return session.get('human_player', None)


def set_human_player(symbol):
    """Set human player symbol in session"""
    session['human_player'] = symbol


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/state', methods=['GET'])
def get_state():
    """Get current game state"""
    board = get_board()
    human_symbol = get_human_player()

    # Check if game is over
    is_terminal = terminal(board)
    game_winner = winner(board) if is_terminal else None
    current_player = player(board) if not is_terminal else None

    # Determine if it's human's turn
    is_human_turn = (human_symbol == current_player) if human_symbol else None

    return jsonify({
        'board': board,
        'currentPlayer': current_player,
        'humanPlayer': human_symbol,
        'isHumanTurn': is_human_turn,
        'isTerminal': is_terminal,
        'winner': game_winner,
        'isDraw': is_terminal and game_winner is None,
        'needsPlayerSelection': human_symbol is None
    })


@app.route('/select-player', methods=['POST'])
def select_player():
    """Let human select X or O"""
    try:
        data = request.get_json()
        symbol = data.get('symbol')

        if symbol not in ['X', 'O']:
            return jsonify({'error': 'Invalid symbol. Must be X or O'}), 400

        # Reset game and set player
        session['board'] = initial_state()
        set_human_player(symbol)

        # If human chose O, AI (X) goes first
        if symbol == 'O':
            board = get_board()
            ai_action = minimax(board)
            board = result(board, ai_action)
            set_board(board)

        return get_state()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/move', methods=['POST'])
def make_move():
    """Handle player move and trigger AI response if needed"""
    try:
        data = request.get_json()
        row = data.get('row')
        col = data.get('col')

        if row is None or col is None:
            return jsonify({'error': 'Missing row or col'}), 400

        board = get_board()
        human_symbol = get_human_player()

        if not human_symbol:
            return jsonify({'error': 'Player not selected'}), 400

        # Validate move
        if board[row][col] is not None:
            return jsonify({'error': 'Cell already occupied'}), 400

        if terminal(board):
            return jsonify({'error': 'Game already over'}), 400

        # Check if it's human's turn
        current = player(board)
        if current != human_symbol:
            return jsonify({'error': 'Not your turn'}), 400

        # Apply human move
        action = (row, col)
        board = result(board, action)
        set_board(board)

        # Check if game ended after human move
        if terminal(board):
            return get_state()

        # AI move
        ai_action = minimax(board)
        board = result(board, ai_action)
        set_board(board)

        # Return updated state
        return get_state()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/ai-move', methods=['POST'])
def ai_move():
    """Trigger AI move when AI goes first or in single-player mode"""
    try:
        board = get_board()
        human_symbol = get_human_player()

        if not human_symbol:
            return jsonify({'error': 'Player not selected'}), 400

        if terminal(board):
            return jsonify({'error': 'Game already over'}), 400

        # Check if it's AI's turn
        current = player(board)
        if current == human_symbol:
            return jsonify({'error': 'Not AI turn'}), 400

        # AI move
        ai_action = minimax(board)
        board = result(board, ai_action)
        set_board(board)

        return get_state()

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/reset', methods=['POST'])
def reset_game():
    """Reset the game to initial state"""
    data = request.get_json() or {}
    keep_player = data.get('keepPlayer', False)

    session['board'] = initial_state()

    if not keep_player:
        session['human_player'] = None  # Clear player selection
    else:
        # If keeping player selection and human is O, AI goes first
        human_symbol = get_human_player()
        if human_symbol == 'O':
            board = get_board()
            ai_action = minimax(board)
            board = result(board, ai_action)
            set_board(board)

    return get_state()


if __name__ == '__main__':
    app.run(debug=True, port=5002)

# For production, app is run by gunicorn