# 🎮 Tic Tac Toe

A modern, colorful web-based Tic-Tac-Toe game featuring an unbeatable AI opponent powered by the minimax algorithm. Built with Flask backend and vanilla JavaScript frontend.

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-3.0.0-green)
![License](https://img.shields.io/badge/license-MIT-blue)

## ✨ Features

- 🤖 **Unbeatable AI** - Minimax algorithm ensures perfect play
- 🎯 **Player Choice** - Choose to play as X or O
- 📊 **Statistics Tracking** - Win/loss/draw record with win rate
- 📱 **Responsive Design** - Works on desktop and mobile devices
- 🔄 **Quick Restart** - Multiple restart options after game ends

## 🚀 Quick Start

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/steve-jr/tic-tac-toe-ai.git
   cd tic-tac-toe-ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**
   ```bash
   python app.py
   ```

5. **Open in browser**
   ```
   http://localhost:5000
   ```

## 🔧 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Serve main game page |
| `/state` | GET | Get current game state |
| `/select-player` | POST | Choose X or O |
| `/move` | POST | Make a move |
| `/reset` | POST | Reset game |

### Sample API Response

```json
{
  "board": [["X", null, "O"], [null, "X", null], ["O", null, null]],
  "currentPlayer": "X",
  "humanPlayer": "X",
  "isHumanTurn": true,
  "isTerminal": false,
  "winner": null,
  "isDraw": false,
  "needsPlayerSelection": false
}
```

## 🧠 Technical 

### Minimax Algorithm

The AI uses the minimax algorithm with alpha-beta pruning to evaluate all possible game states and choose the optimal move. This makes the AI unbeatable - the best you can do is draw! 
Game state stored in Flask sessions (cookies). 
Each player gets their own game instance


## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Minimax algorithm implementation inspired by CS50 AI course at UMich
- UI design inspired by modern glassmorphism trends
- Built with Flask and pure JavaScript for simplicity

## 📞 Support

- Create an issue for bug reports
- Start a discussion for feature requests
- Email: steve.junior1230@gmail.com
- Visit URL https://tic-tac-toe-ai-production-faf0.up.railway.app
---

Made with ❤️ and ☕ by Steve Junior