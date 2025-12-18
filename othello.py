
import score, turtle, random
from board import Board

# Define all the possible directions in which a player's move can flip 
# their adversary's tiles as constant (0 – the current row/column, 
# +1 – the next row/column, -1 – the previous row/column)
MOVE_DIRS = [(-1, -1), (-1, 0), (-1, +1),
             (0, -1),           (0, +1),
             (+1, -1), (+1, 0), (+1, +1)]

# UI Constants
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50
BUTTON_COLOR = 'black' # Othello tile color
BUTTON_TEXT_COLOR = 'white'
BG_COLOR = 'forest green' # Board color

class Othello(Board):
    ''' Othello class.
        Attributes: current_player, an integer 0 or 1 to represent two 
                    different players (the user and the computer)
                    num_tiles, a list of integers for number of tiles each 
                    player has
                    n, an integer for nxn board
                    all other attributes inherited from class Board
        n (integer) is optional in the __init__ function
        current_player, num_tiles and all other inherited attributes 
        are not taken in the __init__

        Methods: initialize_board, make_move, flip_tiles, has_tile_to_flip, 
                 has_legal_move, get_legal_moves, is_legal_move, 
                 is_valid_coord, run, play, make_random_move, 
                 report_result, __str__ , __eq__ and all other methods 
                 inherited from class Board
    '''

    def __init__(self, n = 8):
        '''
            Initilizes the attributes. 
            Only takes one optional parameter; others have default values.
        '''
        Board.__init__(self, n)
        self.current_player = 0
        self.num_tiles = [2, 2]
        self.game_mode = '1' # '1' for PvE, '2' for PvP
        self.human_color = 0 # 0 for Black, 1 for White (only used in PvE)
        self.menu_state = 'MAIN' # MAIN, MODE, COLOR, SETTINGS
        self.buttons = [] # Store button coordinates for click detection

    def initialize_board(self):
        ''' Method: initialize_board
            Parameters: self
            Returns: nothing
            Does: Draws the first 4 tiles in the middle of the board
                  (the size of the board must be at least 2x2).
        '''
        if self.n < 2:
            return

        coord1 = int(self.n / 2 - 1)
        coord2 = int(self.n / 2)
        initial_squares = [(coord1, coord2), (coord1, coord1),
                           (coord2, coord1), (coord2, coord2)]
        
        for i in range(len(initial_squares)):
            color = i % 2
            row = initial_squares[i][0]
            col = initial_squares[i][1]
            self.board[row][col] = color + 1
            self.draw_tile(initial_squares[i], color)
    
    def make_move(self):
        ''' Method: make_move
            Parameters: self
            Returns: nothing
            Does: Draws a tile for the player's next legal move on the 
                  board and flips the adversary's tiles. Also, updates the 
                  state of the board (1 for black tiles and 2 for white 
                  tiles), and increases the number of tiles of the current 
                  player by 1.
        '''
        if self.is_legal_move(self.move):
            self.board[self.move[0]][self.move[1]] = self.current_player + 1
            self.num_tiles[self.current_player] += 1
            self.draw_tile(self.move, self.current_player)
            self.flip_tiles()
    
    def flip_tiles(self):
        ''' Method: flip_tiles
            Parameters: self
            Returns: nothing
            Does: Flips the adversary's tiles for current move. Also, 
                  updates the state of the board (1 for black tiles and 
                  2 for white tiles), increases the number of tiles of 
                  the current player by 1, and decreases the number of 
                  tiles of the adversary by 1.
        '''
        curr_tile = self.current_player + 1 
        for direction in MOVE_DIRS:
            if self.has_tile_to_flip(self.move, direction):
                i = 1
                while True:
                    row = self.move[0] + direction[0] * i
                    col = self.move[1] + direction[1] * i
                    if self.board[row][col] == curr_tile:
                        break
                    else:
                        self.board[row][col] = curr_tile
                        self.num_tiles[self.current_player] += 1
                        self.num_tiles[(self.current_player + 1) % 2] -= 1
                        self.draw_tile((row, col), self.current_player)
                        i += 1

    def has_tile_to_flip(self, move, direction):
        ''' Method: has_tile_to_flip
            Parameters: self, move (tuple), direction (tuple)
            Returns: boolean 
                     (True if there is any tile to flip, False otherwise)
            Does: Checks whether the player has any adversary's tile to flip
                  with the move they make.

                  About input: move is the (row, col) coordinate of where the 
                  player makes a move; direction is the direction in which the 
                  adversary's tile is to be flipped (direction is any tuple 
                  defined in MOVE_DIRS).
        '''
        i = 1
        if self.current_player in (0, 1) and \
           self.is_valid_coord(move[0], move[1]):
            curr_tile = self.current_player + 1
            while True:
                row = move[0] + direction[0] * i
                col = move[1] + direction[1] * i
                if not self.is_valid_coord(row, col) or \
                    self.board[row][col] == 0:
                    return False
                elif self.board[row][col] == curr_tile:
                    break
                else:
                    i += 1
        return i > 1

    def has_legal_move(self):
        ''' Method: has_legal_move
            Parameters: self
            Returns: boolean 
                     (True if the player has legal move, False otherwise)
            Does: Checks whether the current player has any legal move 
                  to make.
        '''
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    return True
        return False
    
    def get_legal_moves(self):
        ''' Method: get_legal_moves
            Parameters: self
            Returns: a list of legal moves that can be made
            Does: Finds all the legal moves the current player can make.
                  Every move is a tuple of coordinates (row, col).
        '''
        moves = []
        for row in range(self.n):
            for col in range(self.n):
                move = (row, col)
                if self.is_legal_move(move):
                    moves.append(move)
        return moves

    def is_legal_move(self, move):
        ''' Method: is_legal_move
            Parameters: self, move (tuple)
            Returns: boolean (True if move is legal, False otherwise)
            Does: Checks whether the player's move is legal.

                  About input: move is a tuple of coordinates (row, col).
        '''
        if move != () and self.is_valid_coord(move[0], move[1]) \
           and self.board[move[0]][move[1]] == 0:
            for direction in MOVE_DIRS:
                if self.has_tile_to_flip(move, direction):
                    return True
        return False

    def is_valid_coord(self, row, col):
        ''' Method: is_valid_coord
            Parameters: self, row (integer), col (integer)
            Returns: boolean (True if row and col is valid, False otherwise)
            Does: Checks whether the given coordinate (row, col) is valid.
                  A valid coordinate must be in the range of the board.
        '''
        if 0 <= row < self.n and 0 <= col < self.n:
            return True
        return False

    def draw_button(self, x, y, width, height, text, action):
        ''' Method: draw_button
            Parameters: self, x, y, width, height, text, action
            Returns: nothing
            Does: Draws a button and registers its clickable area.
        '''
        # Draw button background
        btn = turtle.Turtle()
        btn.hideturtle()
        btn.speed(0)
        btn.penup()
        btn.goto(x - width/2, y + height/2)
        btn.color('black', BUTTON_COLOR)
        btn.begin_fill()
        for _ in range(2):
            btn.forward(width)
            btn.right(90)
            btn.forward(height)
            btn.right(90)
        btn.end_fill()
        
        # Draw text
        btn.goto(x, y - height/4)
        btn.color(BUTTON_TEXT_COLOR)
        btn.write(text, align="center", font=("Arial", 16, "bold"))
        
        # Store button area for click detection: (x_min, x_max, y_min, y_max, action)
        self.buttons.append((x - width/2, x + width/2, y - height/2, y + height/2, action))

    def clear_screen(self):
        turtle.clearscreen()
        turtle.bgcolor(BG_COLOR)
        self.buttons = []

    def show_main_menu(self):
        self.clear_screen()
        turtle.title("Othello - Main Menu")
        
        # Title
        title = turtle.Turtle()
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.goto(0, 150)
        title.color('white')
        title.write("OTHELLO", align="center", font=("Arial", 40, "bold"))
        
        self.draw_button(0, 50, BUTTON_WIDTH, BUTTON_HEIGHT, "Play", "PLAY_MENU")
        self.draw_button(0, -50, BUTTON_WIDTH, BUTTON_HEIGHT, "Settings", "SETTINGS")
        self.draw_button(0, -150, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit", "QUIT")
        
        turtle.onscreenclick(self.handle_menu_click)

    def show_mode_select(self):
        self.clear_screen()
        
        title = turtle.Turtle()
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.goto(0, 150)
        title.color('white')
        title.write("SELECT MODE", align="center", font=("Arial", 30, "bold"))
        
        self.draw_button(0, 50, BUTTON_WIDTH + 50, BUTTON_HEIGHT, "Vs Computer", "MODE_PVE")
        self.draw_button(0, -50, BUTTON_WIDTH + 50, BUTTON_HEIGHT, "Vs Player", "MODE_PVP")
        self.draw_button(0, -150, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", "MAIN_MENU")
        
        turtle.onscreenclick(self.handle_menu_click)

    def show_color_select(self):
        self.clear_screen()
        
        title = turtle.Turtle()
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.goto(0, 150)
        title.color('white')
        title.write("CHOOSE COLOR", align="center", font=("Arial", 30, "bold"))
        
        self.draw_button(0, 50, BUTTON_WIDTH + 50, BUTTON_HEIGHT, "Play as Black", "COLOR_BLACK")
        self.draw_button(0, -50, BUTTON_WIDTH + 50, BUTTON_HEIGHT, "Play as White", "COLOR_WHITE")
        self.draw_button(0, -150, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", "MODE_MENU")
        
        turtle.onscreenclick(self.handle_menu_click)

    def show_settings(self):
        self.clear_screen()
        
        title = turtle.Turtle()
        title.hideturtle()
        title.speed(0)
        title.penup()
        title.goto(0, 150)
        title.color('white')
        title.write("SETTINGS", align="center", font=("Arial", 30, "bold"))
        
        info = turtle.Turtle()
        info.hideturtle()
        info.speed(0)
        info.penup()
        info.goto(0, 0)
        info.color('white')
        info.write("Sound: ON (Mock)", align="center", font=("Arial", 14, "normal"))

        self.draw_button(0, -150, BUTTON_WIDTH, BUTTON_HEIGHT, "Back", "MAIN_MENU")
        
        turtle.onscreenclick(self.handle_menu_click)

    def handle_menu_click(self, x, y):
        for btn in self.buttons:
            x_min, x_max, y_min, y_max, action = btn
            if x_min <= x <= x_max and y_min <= y <= y_max:
                if action == "PLAY_MENU":
                    self.show_mode_select()
                elif action == "SETTINGS":
                    self.show_settings()
                elif action == "QUIT":
                    turtle.bye()
                elif action == "MODE_PVE":
                    self.game_mode = '1'
                    self.show_color_select()
                elif action == "MODE_PVP":
                    self.game_mode = '2'
                    self.start_game()
                elif action == "COLOR_BLACK":
                    self.human_color = 0
                    self.start_game()
                elif action == "COLOR_WHITE":
                    self.human_color = 1
                    self.start_game()
                elif action == "MAIN_MENU":
                    self.show_main_menu()
                elif action == "MODE_MENU":
                    self.show_mode_select()
                return

    def start_game(self):
        self.clear_screen()
        turtle.tracer(0, 0) # Turn off animation for fast drawing
        self.draw_board()
        self.initialize_board()
        turtle.update()
        turtle.tracer(1, 10) # Turn on animation
        
        if self.current_player not in (0, 1):
            print('Error: unknown player. Quit...')
            return
        
        self.current_player = 0
        self.draw_info(self.current_player, self.num_tiles)
        
        # Only highlight if it's human's turn (or PvP)
        if self.game_mode == '2' or self.current_player == self.human_color:
            self.highlight_legal_moves(self.get_legal_moves())

        if self.game_mode == '1' and self.human_color == 1:
             # Computer is black (0), human is white (1)
             # Trigger computer move immediately
             turtle.ontimer(self.computer_turn_logic, 1000)
             turtle.onscreenclick(self.play) 
        else:
            print('Your turn.')
            turtle.onscreenclick(self.play)

    def run(self):
        ''' Method: run
            Parameters: self
            Returns: nothing
            Does: Starts the game with the main menu.
        '''
        self.show_main_menu()
        turtle.mainloop()

    def play(self, x, y):
        ''' Method: play
            Parameters: self, x (float), y (float)
            Returns: nothing
            Does: Plays alternately between the user's turn and the computer's
                  turn or between two users.
        '''
        # Prevent multiple clicks
        turtle.onscreenclick(None)

        if self.game_mode == '2':
            self.play_pvp(x, y)
        else:
            self.play_pve(x, y)

    def play_pvp(self, x, y):
        if self.has_legal_move():
            self.get_coord(x, y)
            if self.is_legal_move(self.move):
                self.make_move()
                self.clear_highlights()
                self.current_player = 1 - self.current_player
                self.draw_info(self.current_player, self.num_tiles)
                
                if self.has_legal_move():
                    self.highlight_legal_moves(self.get_legal_moves())
                    turtle.onscreenclick(self.play)
                else:
                    # Current player has no moves, check if other player has moves
                    print(f"No moves for player {self.current_player + 1}")
                    self.current_player = 1 - self.current_player
                    self.draw_info(self.current_player, self.num_tiles)
                    
                    if self.has_legal_move():
                         print(f"Switching back to player {self.current_player + 1}")
                         self.highlight_legal_moves(self.get_legal_moves())
                         turtle.onscreenclick(self.play)
                    else:
                        self.handle_game_over()
            else:
                # Invalid move, let them try again
                turtle.onscreenclick(self.play)
        else:
             # Should not be reachable if we check moves before binding
             self.handle_game_over()

    def play_pve(self, x, y):
        # Human turn logic
        # If it's not human's turn, ignore click (though we shouldn't be here if we unbound click)
        if self.current_player != self.human_color:
             return

        if self.has_legal_move():
            self.get_coord(x, y)
            if self.is_legal_move(self.move):
                self.make_move()
                self.clear_highlights()
                self.current_player = 1 - self.current_player # Switch to computer
                self.draw_info(self.current_player, self.num_tiles)
                
                # Schedule computer turn
                turtle.ontimer(self.computer_turn_logic, 500)
            else:
                turtle.onscreenclick(self.play)
        else:
            # Human has no moves
            print("No moves for human.")
            self.current_player = 1 - self.current_player
            self.draw_info(self.current_player, self.num_tiles)
            turtle.ontimer(self.computer_turn_logic, 1000)

    def computer_turn_logic(self):
        # Computer turn
        # Loop until computer has no moves or passes turn back to human
        
        passed = False
        while self.current_player != self.human_color:
            if self.has_legal_move():
                print('Computer\'s turn.')
                self.make_random_move()
                self.current_player = 1 - self.current_player # Switch to human
                self.draw_info(self.current_player, self.num_tiles)
                passed = True
                break # Exit loop to let human play
            else:
                print("Computer has no moves.")
                self.current_player = 1 - self.current_player # Switch to human
                self.draw_info(self.current_player, self.num_tiles)
                
                # Check if human has moves. If not, game over.
                if not self.has_legal_move():
                    self.handle_game_over()
                    return
                # If human has moves, break to let them play
                break
        
        # Now it's human's turn (or game over handled)
        if self.has_legal_move():
             self.highlight_legal_moves(self.get_legal_moves())
             turtle.onscreenclick(self.play)
        else:
             if not passed: # If we didn't just come from a move
                 # Human has no moves, but computer just passed to human?
                 # This means computer had no moves. Human has no moves. Game over.
                 self.handle_game_over()
             else:
                 # Human has no moves. Pass back to computer.
                 print("Human has no moves. Passing back to computer.")
                 self.current_player = 1 - self.current_player
                 self.draw_info(self.current_player, self.num_tiles)
                 turtle.ontimer(self.computer_turn_logic, 1000)

    def make_random_move(self):
        ''' Method: make_random_move
            Parameters: self
            Returns: nothing
            Does: Makes a random legal move on the board.
        '''
        moves = self.get_legal_moves()
        if moves:
            self.move = random.choice(moves)
            self.make_move()

    def handle_game_over(self):
        print('-----------')
        self.report_result()
        name = turtle.textinput('High Score', 'Enter your name for posterity')
        if name and not score.update_scores(name, self.num_tiles[0]):
            print('Your score has not been saved.')
        print('Thanks for playing Othello!')
        close = turtle.textinput('Game Over', 'Close the game screen? Y/N')
        if close and close.upper() == 'Y':
            turtle.bye()
        elif close != 'N':
            print('Quit in 3s...')
            turtle.ontimer(turtle.bye, 3000)

    def report_result(self):
        ''' Method: report_result
            Parameters: self
            Returns: nothing
            Does: Announces the winner and reports the final number of
                  tiles each play has.
        '''
        print('GAME OVER!!')
        if self.num_tiles[0] > self.num_tiles[1]:
            print('YOU WIN!!',
                  'You have %d tiles, but the computer only has %d!' 
                  % (self.num_tiles[0], self.num_tiles[1]))
        elif self.num_tiles[0] < self.num_tiles[1]:
            print('YOU LOSE...',
                  'The computer has %d tiles, but you only have %d :(' 
                  % (self.num_tiles[1], self.num_tiles[0]))
        else:
            print("IT'S A TIE!! There are %d of each!" % self.num_tiles[0])
    
    def __str__(self):
        ''' 
            Returns a printable version of the current status of the 
            game to print.
        '''
        player_str = 'Current player: ' + str(self.current_player + 1) + '\n'
        num_tiles_str = '# of black tiles -- 1: ' + str(self.num_tiles[0]) + \
                        '\n' + '# of white tiles -- 2: ' + \
                        str(self.num_tiles[1]) + '\n'
        board_str = Board.__str__(self)
        printable_str = player_str + num_tiles_str + board_str

        return printable_str

    def __eq__(self, other):
        '''
            Compares two instances. 
            Returns True if they have both the same board attribute and 
            current player, False otherwise.
        '''
        return Board.__eq__(self, other) and self.current_player == \
        other.current_player
