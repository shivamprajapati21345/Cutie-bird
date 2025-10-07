Cutie Birds Sky 🐦✨

A fun Flappy Bird–style game built using Python + Pygame with extra features like:
Coins collection 🪙
Level progression 🚀
Scoreboard saved in a database 📊
Responsive design (resizes with window) 🖥️

🎮 Gameplay

Press SPACE or UP Arrow to flap the bird.
Avoid hitting pipes or the ground.
Collect coins for extra score.
Game gets faster & harder as you level up.
Your name and score are saved in the leaderboard.

Project Structure
.
├── main.py # Main game logic
├── model.py # Database functions (init, save_score, get_top_scores)
├── settings.py # Settings & database path
├── assets/ # Sprites and sounds
│ ├── sprites/ # Bird, pipes, ground, backgrounds, coins
│ └── audio/ # wing.wav, hit.wav, point.wav
└── README.md

📦 Requirements

Make sure you have:
Python 3.8+ installed

> > > > > > > pip install pygame

▶️ How to Run

Clone the repo and run the main game file:https://github.com/shivamprajapati21345/Cutie-bird

> > > > > python game.py

🏆 Scoring
Jump action: +1
Collecting a coin: +1
Higher levels increase game speed and difficulty.

📊 Leaderboard
Top scores are saved locally using SQLite3 database (scores.db).
You can see your name and best scores on the home screen
