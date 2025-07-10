# Pawn-Passant
A chess application to play (computer and others) , learn and analyse game even at times without connecting to internet.


This is an application written in python to play and learn chess. The objective is to make chess accessable offline to play against chess engines to learn and analyse the game. Here are the goals:
- play games against computer at different difficulty
- ability to analyse any game
- ability to learn openings offline
- ability to play locally with others
- intutive gui
- ability to play online

Roadmap for the project:
🧭 Month 1: Foundations & Core Chess Logic
Goal: Build a working console-based chess app and learn essential tools.
Week 1: Setup & Planning
- Learn basics of project structure and Git.
- Choose GUI library (recommended: PyQt5 or Tkinter).
- Create folder structure and initialize GitHub repo.
- Install python-chess and test a basic board with legal moves.

Week 2: Learn & Implement Chess Logic
- Practice using python-chess: board setup, move validation.
- Build a terminal version of the game (text-based).
- Implement move input, turns, and game-over conditions.


Week 3: Learn GUI Basics
- Learn PyQt5 basics (widgets, layout, events) or Tkinter if you prefer.
- Start GUI layout: empty board with squares and coordinate labels.
- Load piece images and place them on the board.


Week 4: Build a Click-to-Move GUI
- Enable click-to-select and move pieces on the board.
- Integrate python-chess logic with GUI.
- Show current player turn and legal move highlights.



♟️ Month 2: Game Modes & AI Integration
Goal: Add play modes – player vs player and vs computer (Stockfish).
Week 5: Local Multiplayer Mode
- Complete hotseat play (2 players on same device).
- Add move history and a restart button.


Week 6: Learn Stockfish Integration
- Learn how to interface with Stockfish using python-chess.uci.
- Run Stockfish in terminal and test position analysis.


Week 7: Add Play vs Computer
- Integrate Stockfish in your app.
- Add basic difficulty setting (depth/time control).
- Display engine’s move and evaluation.


Week 8: Polish and Test
- Add undo button and simple move timer.
- Test all modes (PvP, PvE) thoroughly.
- Start saving PGN of played games.



📚 Month 3: Learning Tools & PGN Analysis
Goal: Help users learn from games and openings.
Week 9: PGN Save/Load
- Learn PGN format.
- Implement game save/load feature using python-chess.


Week 10: Opening Explorer Basics
- Download ECO opening PGN file (publicly available).
- Parse and visualize openings in your app.
- Show name and common replies for each opening.


Week 11: Add Game Analysis
- Let engine analyze past games.
- Highlight best moves, mistakes, blunders.
- Show evaluation graph (simplified, textual if needed).


Week 12: Review and Polish
- Fix bugs and refine UI.
- Make buttons/icons intuitive.
- Backup everything to GitHub.



🌐 Month 4: Online Play & Finishing Touches
Goal: Try basic online play and wrap up project.
Week 13: Learn Sockets (for Online Play)
- Learn Python socket basics.
- Create a simple two-player connection test (terminal first).


Week 14: Online Chess Prototype
- Allow remote players to connect and play.
- Sync moves and turns across devices (basic LAN or IP-based).


Week 15: Polish GUI & Add Settings
- Add themes (e.g., dark mode).
- Add settings page: difficulty, time, player name, etc.
- Add sound effects (optional).


Week 16: Final Touches & Packaging
- Final test: all features working (PvP, AI, Analysis, Online).
- Package the app using PyInstaller or cx_Freeze.
- Create README, short demo video, and share!

📌 Total Feature Checklist (By End of Month 4)
 ✅ Play against computer
 ✅ Local multiplayer
 ✅ Game analysis
 ✅ Offline opening learning
 ✅ PGN load/save
 ✅ Simple online play
 ✅ Intuitive GUI
 ✅ Cross-platform packaging

