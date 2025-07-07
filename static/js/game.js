// Game state management
let gameState = {
    board: null,
    humanPlayer: null,
    currentPlayer: null,
    isHumanTurn: false,
    isTerminal: false,
    winner: null,
    isDraw: false
};

// Statistics tracking (stored in localStorage)
let stats = {
    wins: 0,
    losses: 0,
    draws: 0
};

// DOM elements
const playerSelection = document.getElementById('player-selection');
const gameContainer = document.getElementById('game-container');
const boardElement = document.getElementById('board');
const statusElement = document.getElementById('status');
const aiThinkingElement = document.getElementById('ai-thinking');
const restartBtn = document.getElementById('restart-btn');
const gameOverModal = document.getElementById('game-over-modal');
const gameOverTitle = document.getElementById('game-over-title');
const gameOverMessage = document.getElementById('game-over-message');

// Initialize the game
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    initializeBoard();
    fetchGameState();
    setupEventListeners();
});

// Load statistics from localStorage
function loadStats() {
    const savedStats = localStorage.getItem('tictactoeStats');
    if (savedStats) {
        stats = JSON.parse(savedStats);
    }
}

// Save statistics to localStorage
function saveStats() {
    localStorage.setItem('tictactoeStats', JSON.stringify(stats));
}

// Set up event listeners
function setupEventListeners() {
    // Player selection buttons
    document.querySelectorAll('.symbol-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const symbol = e.target.dataset.symbol;
            selectPlayer(symbol);
        });
    });

    // Restart button
    restartBtn.addEventListener('click', () => resetGame(false));
    
    // Game over modal buttons
    document.getElementById('play-again-same').addEventListener('click', () => {
        hideGameOverModal();
        resetGame(true);
    });
    
    document.getElementById('play-again-switch').addEventListener('click', () => {
        hideGameOverModal();
        resetGame(false);
    });
}

// Initialize empty board cells
function initializeBoard() {
    boardElement.innerHTML = '';
    for (let row = 0; row < 3; row++) {
        for (let col = 0; col < 3; col++) {
            const cell = document.createElement('button');
            cell.className = 'cell';
            cell.dataset.row = row;
            cell.dataset.col = col;
            cell.addEventListener('click', handleCellClick);
            boardElement.appendChild(cell);
        }
    }
}

// Fetch current game state from server
async function fetchGameState() {
    try {
        const response = await fetch('/state');
        if (!response.ok) throw new Error('Failed to fetch game state');
        
        const state = await response.json();
        updateGameState(state);
        renderGame();
    } catch (error) {
        console.error('Error fetching game state:', error);
        showError('Failed to load game. Please refresh the page.');
    }
}

// Update local game state
function updateGameState(state) {
    gameState = { ...state };
}

// Render the game based on current state
function renderGame() {
    // Show player selection or game board
    if (gameState.needsPlayerSelection) {
        playerSelection.classList.remove('hidden');
        gameContainer.classList.add('hidden');
    } else {
        playerSelection.classList.add('hidden');
        gameContainer.classList.remove('hidden');
        renderBoard();
        updateStatus();
        
        // Check if game just ended
        if (gameState.isTerminal && !gameOverModal.classList.contains('shown')) {
            setTimeout(() => showGameOverModal(), 500);
        }
    }
}

// Render the board
function renderBoard() {
    const cells = boardElement.querySelectorAll('.cell');
    
    gameState.board.forEach((row, rowIndex) => {
        row.forEach((value, colIndex) => {
            const cellIndex = rowIndex * 3 + colIndex;
            const cell = cells[cellIndex];
            
            // Clear previous classes
            cell.className = 'cell';
            
            // Set cell content and styling
            if (value) {
                cell.textContent = value;
                cell.classList.add('occupied', value.toLowerCase());
            } else {
                cell.textContent = '';
            }
            
            // Disable cells if game is over or not human's turn
            if (gameState.isTerminal || !gameState.isHumanTurn) {
                cell.classList.add('disabled');
            }
        });
    });
    
    // Highlight winning cells if game is won
    if (gameState.winner) {
        highlightWinningCells();
    }
}

// Update status message
function updateStatus() {
    let message = '';
    
    if (gameState.isTerminal) {
        if (gameState.winner) {
            const winnerName = gameState.winner === gameState.humanPlayer ? 'You win!' : 'AI wins!';
            message = winnerName;
            statusElement.className = `status winner-${gameState.winner.toLowerCase()}`;
        } else {
            message = "It's a draw!";
            statusElement.className = 'status draw';
        }
    } else {
        if (gameState.isHumanTurn) {
            message = `Your turn (${gameState.humanPlayer})`;
        } else {
            message = `AI's turn (${gameState.humanPlayer === 'X' ? 'O' : 'X'})`;
        }
        statusElement.className = 'status';
    }
    
    statusElement.textContent = message;
}

// Handle cell click
async function handleCellClick(e) {
    const row = parseInt(e.target.dataset.row);
    const col = parseInt(e.target.dataset.col);
    
    // Validate click
    if (!gameState.isHumanTurn || gameState.isTerminal) return;
    if (gameState.board[row][col] !== null) return;
    
    // Make move
    await makeMove(row, col);
}

// Select player (X or O)
async function selectPlayer(symbol) {
    try {
        showAIThinking();
        
        const response = await fetch('/select-player', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ symbol })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to select player');
        }
        
        const state = await response.json();
        updateGameState(state);
        renderGame();
        hideAIThinking();
    } catch (error) {
        console.error('Error selecting player:', error);
        showError(error.message);
        hideAIThinking();
    }
}

// Make a move
async function makeMove(row, col) {
    try {
        // Disable board during request
        boardElement.classList.add('disabled');
        showAIThinking();
        
        const response = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ row, col })
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'Failed to make move');
        }
        
        const state = await response.json();
        updateGameState(state);
        renderGame();
    } catch (error) {
        console.error('Error making move:', error);
        showError(error.message);
    } finally {
        boardElement.classList.remove('disabled');
        hideAIThinking();
    }
}

// Reset the game
async function resetGame(keepPlayer = false) {
    try {
        const response = await fetch('/reset', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ keepPlayer })
        });
        
        if (!response.ok) throw new Error('Failed to reset game');
        
        const state = await response.json();
        updateGameState(state);
        renderGame();
    } catch (error) {
        console.error('Error resetting game:', error);
        showError('Failed to reset game. Please refresh the page.');
    }
}

// Show game over modal
function showGameOverModal() {
    // Update statistics
    if (gameState.winner) {
        if (gameState.winner === gameState.humanPlayer) {
            stats.wins++;
            gameOverTitle.textContent = '🎉 You Win!';
            gameOverTitle.style.color = '#4CAF50';
        } else {
            stats.losses++;
            gameOverTitle.textContent = '😔 AI Wins';
            gameOverTitle.style.color = '#f44336';
        }
    } else {
        stats.draws++;
        gameOverTitle.textContent = '🤝 Draw!';
        gameOverTitle.style.color = '#FF9800';
    }
    
    saveStats();
    
    // Show stats
    gameOverMessage.innerHTML = `
        <strong>Overall Record:</strong><br>
        Wins: ${stats.wins} | Losses: ${stats.losses} | Draws: ${stats.draws}<br>
        Win Rate: ${calculateWinRate()}%
    `;
    
    gameOverModal.classList.remove('hidden');
    gameOverModal.classList.add('shown');
}

// Hide game over modal
function hideGameOverModal() {
    gameOverModal.classList.add('hidden');
    gameOverModal.classList.remove('shown');
}

// Calculate win rate
function calculateWinRate() {
    const totalGames = stats.wins + stats.losses + stats.draws;
    if (totalGames === 0) return 0;
    return Math.round((stats.wins / totalGames) * 100);
}

// Show AI thinking indicator
function showAIThinking() {
    aiThinkingElement.classList.remove('hidden');
}

// Hide AI thinking indicator
function hideAIThinking() {
    aiThinkingElement.classList.add('hidden');
}

// Show error message
function showError(message) {
    statusElement.textContent = `Error: ${message}`;
    statusElement.className = 'status error';
}

// Highlight winning cells (basic implementation)
function highlightWinningCells() {
    // This is a simplified version - you might want to enhance this
    // to actually detect the winning line based on your game logic
    const cells = boardElement.querySelectorAll('.cell');
    
    // Check rows
    for (let row = 0; row < 3; row++) {
        if (checkLine(row * 3, row * 3 + 1, row * 3 + 2, cells)) return;
    }
    
    // Check columns
    for (let col = 0; col < 3; col++) {
        if (checkLine(col, col + 3, col + 6, cells)) return;
    }
    
    // Check diagonals
    checkLine(0, 4, 8, cells);
    checkLine(2, 4, 6, cells);
}

// Check if three cells form a winning line
function checkLine(a, b, c, cells) {
    const cellA = cells[a];
    const cellB = cells[b];
    const cellC = cells[c];
    
    if (cellA.textContent && 
        cellA.textContent === cellB.textContent && 
        cellA.textContent === cellC.textContent) {
        cellA.classList.add('winning');
        cellB.classList.add('winning');
        cellC.classList.add('winning');
        return true;
    }
    return false;
}
