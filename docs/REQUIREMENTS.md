# REQUIREMENTS

Goal: Implement the game of othello so a human can play against the computer or, post-MVP, 2 computer players can play.

## Phase 1: MVP

### User interface

* Use Qt6 to provide the GUI
* When the application is launched, it should display a window (the launch window) with the following buttons:
  * Play as White
    * Clicking "Play as White" should start a game where the human is playing as White and the computer as Black.
  * Play as Black
    * Clicking "Play as Black" should start a game where the human is playing as Black and the computer as White.
  * Quit
    * Clicking Quit should quit then application.
* When playing a game, a window (the game window) should be open that displays (and is big enough to show) all the following:
  * On the left hand side, a panel showing:
    * the score in the form: <W> / <B> where W is the number of white pieces and B is the number of black pieces.
    * how many turns have been played, initially 0, but increasing by 1 with each turn
  * On the right hand side, the game board, i.e. the 8x8 board showing the current state of play.
    * empty squares should be shaded light grey, unless they are legal moves for the current 
    player in which case they should be shaded light green
    * squares with pieces on should be white if the piece is currently white or black if the piece is currently black.
    * a thin (2px) dark blue grid separates each square from the others.
    * each square should be about 1 cm x 1 cm on screen, calculated using the physical DPI of the display so the size is correct regardless of display scaling or resolution
    * the horizontal axis is labeled A to H and the vertical axis is labeled 1 to 8. So squares 
    have names such as A1, H3, B2, etc. 
  * The UI must remain responsive at all times — the computer's move calculation must not freeze or block the interface.
  * The 0.5-second highlight delay must not block the UI — the interface should remain responsive during this period.
  * If it is the computer's turn:
    * the computer player should decide which square to place a piece on, this square gets highlighted in bright green
    for 0.5 seconds and then the piece is placed there.
    * the computer is not allowed to play an illegal move.
  * If it is the human player's turn:
    * the human can click on the square where they want to place a piece.
      * if the selected square is a legal move, then this square gets highlighted in bright green for 0.5 seconds and then the piece is placed there. 
      * if the selected square is an illegal move, then this square gets highlighted in red for 0.5 seconds, and the player then has to select another square.
  * After placing a piece, the board should be updated to show the new board state, i.e.:
    * the newly placed piece plus any pieces that flipped colour should be updated to reflect their
    new status.
  * Once the game is finished, this window should display, in the left panel, a button marked 'Finish'
    * Clicking this will return to the launch window from which the user can quit or start a new game again.

## The computer player

* The computer player, whether it is playing Black or White should perform a minimax search to depth 4 to decide 
its move, when it's the computer player's turn.
  * the minimax algorithm should score the board based on the following formula:
    * number of computer's pieces - number of opponent's pieces 
    + 10 * (number of corners the computer holds - number of corners the player holds)
    + 10 * (the number of squares diagonally adjacent to a corner that the opponent holds - 
    the number of squares diagonally adjacent to a corner that the computer holds)
  * tied scoring for a move should be dealt with by randomly choosing the tied moves.

## The game

* The initial state has white on D4/E5 and black on D5/E4. 
* The game ends either when the board is full or if neither player can make a legal move.
* If the current player can't make a move then this should result in a pass.
  * A pass counts as a turn.
  * In this situation:
    * if the human player is the current player a popup should appear stating that no move is possible and you need 
    to pass, with an 'OK' button to click. Clicking the button will trigger the pass, moving on to the computer's turn.
    * if the computer player is the current player, a popup should appear stating that the computer can't play a move and is thus passing. 
    Again this should have an 'OK' button, the clicking of which triggers the computer's pass, enabling the human to play their next move.
* If neither player can make a legal move, the popup should state this, and clicking 'OK' finishes the game.
* All pass and end-game popups must be fully dismissed (i.e. 'OK' clicked) before the next game action is triggered — no move, pass, or turn transition should occur while a popup is open.

## Phase 2: Smarter computer players

* There will now be 4 levels of computer player
* The levels will be defined as follows and in the following order:
  * Dumb: this level makes a legal move at random
  * Naive: this level uses minimax search to depth 2, scoring the board using only raw piece count, i.e. the first term of the MVP player's evaluation function (number of computer's pieces - number of opponent's pieces)
  * Amateur: this level is the computer player from the MVP - this is the default level
  * Experienced: this level is like the computer player from the MVP, but with minimax search depth 6, and
    additionally penalises C-squares (the edge squares immediately adjacent to each corner, e.g. A2, B1) using
    the following extra scoring term:
    * 5 * (the number of C-squares the opponent holds - the number of C-squares the computer holds)
  * Expert: this level is like Experienced level but additionally scores relative mobility:
    * 1 * (the number of legal moves the computer can make - the number of legal moves the opponent can make)
* All levels from Experienced upward must use alpha-beta pruning to keep move calculation fast enough that the
  UI remains responsive.
* Tied scoring for a move at all levels is dealt with by randomly choosing among the tied moves.
* The launch window should contain a new button displaying the current level name.
  * To its left there's a label saying "Level:".
  * This label + button will sit above the buttons from the MVP.
  * The default level is Amateur.
  * Clicking on the button will cycle through the levels in order: Dumb → Naive → Amateur → Experienced → Expert → Dumb,
    selecting each as the computer level accordingly.
  * The level should persist until changed by the user clicking the button or the program exits.
* Hovering over any button in any of the windows will show a tooltip with an explanation of the button's purpose.
  * However, hovering over the button giving the level should show a tooltip that also explains briefly how the computer
  player selects its moves, using the same strategy description text shown in the game window's left panel.
  This tooltip must update dynamically to reflect the currently selected level.
* The left hand panel in the game window should now display the level of the computer player as well as:
  * a description of the computer player's strategy (immediately below the level, with an indent of 2 chars)
  * which player is white (human or computer)
  * which player is black (human or computer)
