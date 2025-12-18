
import turtle

# Defines sizes of the square and tile, colors of the board, line, 
# and tile as constants
SQUARE = 50
TILE = 20
BOARD_COLOR = 'forest green'
LINE_COLOR = 'black'
TILE_COLORS = ['black', 'white']

class Board:
    ''' Board class.
        Attributes: n, an integer for number of squares for a row/column
                    board, a nested list which stores the state of the board
                    (0 for no tile, 1 for black tiles and 2 for white tiles)
                    square_size, an integer for size of the squares
                    board_color, a string for color of the board
                    line_color, a string for color of the lines of the board
                    tile_size, an integer for size of the radius of the tile
                    tile_colors, a list of strings for colors of the tile
                    move, a tuple for coordinates of the player's next move
        n (integer) is required in the __init__ function
        board (list), square_size (integer), board_color (string), 
        line_color (string), tile_size (integer), tile_colors (list), 
        move (tuple) are not taken in the __init__

        Methods: draw_board, draw_lines, is_on_board, is_on_line, 
                 convert_coord, get_coord, get_tile_start_pos, draw_tile, 
                 __str__ and __eq__
    '''

    def __init__(self, n):
        ''' 
            Initilizes the attributes. 
            Only takes one required parameter; others have default values.
        '''
        self.n = n
        self.board = [[0] * n for i in range(n)]
        self.square_size = SQUARE
        self.board_color = BOARD_COLOR
        self.line_color = LINE_COLOR
        self.tile_size = TILE
        self.tile_colors = TILE_COLORS
        self.move = ()
        self.info_turtle = None
        self.highlight_turtle = None

    def draw_board(self):
        ''' Method: draw_board
            Parameters: self
            Returns: nothing
            
            Does: Draws an nxn board. Color of the board and lines are set 
                  to self.board_color and self.line_color respectively.
        '''
        # Increase height for UI area
        turtle.setup(self.n * self.square_size + self.square_size + 100, 
                    self.n * self.square_size + self.square_size + 100)
        turtle.screensize(self.n * self.square_size, self.n * self.square_size + 100)
        turtle.bgcolor('white')

        # Create the turtle to draw the board
        othello = turtle.Turtle(visible = False)
        othello.penup()
        othello.speed(0)
        othello.hideturtle()

        # Set line color and fill color
        othello.color(self.line_color, self.board_color)
        
        # Move the turtle to the upper left corner
        corner = -self.n * self.square_size / 2
        othello.setposition(corner, corner)
        
        # Draw the board background
        othello.begin_fill()
        for i in range(4):
            othello.pendown()
            othello.forward(self.square_size * self.n)
            othello.left(90)
        othello.end_fill()
        
        # Draw the horizontal lines
        for i in range(self.n + 1):
            othello.setposition(corner, self.square_size * i + corner)
            self.draw_lines(othello)
        
        # Draw the vertical lines
        othello.left(90)
        for i in range(self.n + 1):
            othello.setposition(self.square_size * i + corner, corner)
            self.draw_lines(othello)

        # Initialize UI turtles
        self.info_turtle = turtle.Turtle(visible=False)
        self.info_turtle.penup()
        self.info_turtle.hideturtle()
        self.info_turtle.speed(0)
        
        self.highlight_turtle = turtle.Turtle(visible=False)
        self.highlight_turtle.penup()
        self.highlight_turtle.hideturtle()
        self.highlight_turtle.speed(0)
        self.highlight_turtle.color('blue') # Highlight color

    def draw_lines(self, turt):
        ''' Method: draw_lines
            Parameters: self, turt (turtle object)
            Returns: nothing

            Does: Draws lines of the board.
        '''
        turt.pendown()
        turt.forward(self.square_size * self.n)
        turt.penup()

    def is_on_board(self, x, y):
        ''' Method: is_on_board
            Parameters: self, x (float), y (float)
            Returns: boolean (True if the point is on board, False otherwise)

            Does: Checks whether the given point is on the board.
                
                  About the input: (x, y) are the coordinates of a point 
                  on the screen.
        '''
        bound = self.n / 2 * self.square_size
        
        if - bound < x < bound and - bound < y < bound:
            return True
        return False

    def is_on_line(self, x, y):
        ''' Method: is_on_board
            Parameters: self, x (float), y (float)
            Returns: boolean (True if the point is on line, False otherwise)

            Does: Checks whether the given point is on the line (i.e, the 
                  boundary of a square).
                
                  About the input: (x, y) are the coordinates of a point 
                  on the screen.
        '''
        if self.is_on_board(x, y):   
            if x % self.square_size == 0 or y % self.square_size == 0:
                return True
        return False

    def convert_coord(self, x, y):
        ''' Method: convert_coord
            Parameters: self, x (float), y (float)
            Returns: a tuple of integers (row, col)

            Does: Converts the coordinates from (x, y) to (row, col).
                
                  About the input: (x, y) are the coordinates of a point 
                  on one of the squares of the board.
        '''
        if self.is_on_board(x, y):
            row = int(self.n / 2 - 1 - y // self.square_size)
            col = int(self.n / 2 + x // self.square_size)
            return (row, col)
        return ()

    def get_coord(self, x, y):
        ''' Method: get_coord
            Parameters: self, x (float), y (float)
            Returns: nothing
            
            Does: Gets and converts the (x, y) coordinates of where the user 
                  clicks. If the user clicks on the board, converts (x, y) 
                  to (row, col) and saves the result to self.move; otherwise, 
                  sets self.move to an empty tuple.
        '''
        if self.is_on_board(x, y) and not self.is_on_line(x, y):
            self.move = self.convert_coord(x, y)
        else:
            self.move = ()

    def get_tile_start_pos(self, square):
        ''' Method: get_tile_start_pos
            Parameters: self, square (tuple of integers)
            Returns: a tuple containing the (x, y) coordinates of the starting 
                     position for drawing the tile and the radius of the tile
            
            Does: Calculates the (x, y) coordinates of the starting position
                  for drawing the tile, and sets the radius of the tile to
                  draw.
                  
                  About the input: square is the (row, col) of a square
        '''
        if square == ():
            return ()
        
        for i in range(2):
            if square[i] not in range(self.n):
                return ()

        row, col = square[0], square[1]

        y = ((self.n - 1) / 2 - row) * self.square_size
        if col < self.n / 2:
            x = (col - (self.n - 1) / 2) * self.square_size - self.tile_size
            r = - self.tile_size
        else:
            x = (col - (self.n - 1) / 2) * self.square_size + self.tile_size
            r = self.tile_size
        
        return ((x, y), r)

    def draw_tile(self, square, color):
        ''' Method: draw_tile
            Parameters: self, square (tuple of integers), color (integer)
            Returns: nothing
            Does: Draws a tile of a specific color on the board 
                  using turtle graphics.
                
                  About the input: square is the (row, col) of the square in 
                  which the tile is drawn; color is an integer 0 or 1 to 
                  represent the 1st or 2nd color in the list of colors 
                  (self.colors) to use.
        '''
        # Get starting position and radius of the tile
        pos = self.get_tile_start_pos(square)
        if pos:
            coord = pos[0]
            r = pos[1]
        else:
            print('Error drawing the tile...')
            return
        
        # Create the turtle to draw the tile
        tile = turtle.Turtle(visible = False)
        tile.penup()
        tile.speed(0)
        tile.hideturtle()

        # Set color of the tile
        tile.color(self.tile_colors[color])

        # Move the turtle to the starting postion for drawing
        tile.setposition(coord)
        tile.setheading(90)
        
        # Draw the tile
        tile.begin_fill()
        tile.pendown()
        tile.circle(r)
        tile.end_fill()

    def draw_info(self, current_player, num_tiles):
        ''' Method: draw_info
            Parameters: self, current_player (int), num_tiles (list)
            Returns: nothing
            Does: Displays current player and score information.
        '''
        if not self.info_turtle:
            return
            
        self.info_turtle.clear()
        
        # Position for text (above the board)
        y_pos = self.n * self.square_size / 2 + 20
        
        self.info_turtle.setposition(0, y_pos)
        turn_text = f"Turn: {'Black' if current_player == 0 else 'White'}"
        self.info_turtle.write(turn_text, align="center", font=("Arial", 16, "bold"))
        
        self.info_turtle.setposition(0, y_pos + 25)
        score_text = f"Black: {num_tiles[0]}  |  White: {num_tiles[1]}"
        self.info_turtle.write(score_text, align="center", font=("Arial", 14, "normal"))

    def highlight_legal_moves(self, moves):
        ''' Method: highlight_legal_moves
            Parameters: self, moves (list of tuples)
            Returns: nothing
            Does: Draws a small marker on legal moves.
        '''
        if not self.highlight_turtle:
            return
            
        self.highlight_turtle.clear()
        
        for move in moves:
            pos = self.get_tile_start_pos(move)
            if pos:
                coord = pos[0]
                r = pos[1]
                
                # Calculate center of the square
                # coord is the start point for circle(), which draws from edge
                # If r is positive, circle draws to left?
                # circle(radius) draws a circle with radius r. 
                # The center is radius units left of the turtle; extent is an angle...
                # Actually, let's just go to the center of the square.
                
                row, col = move
                
                # Center x
                center_x = (col - self.n / 2 + 0.5) * self.square_size
                # Center y
                center_y = (self.n / 2 - row - 0.5) * self.square_size
                
                self.highlight_turtle.setposition(center_x, center_y - 5) # Adjust for dot size
                self.highlight_turtle.dot(10, "blue")

    def clear_highlights(self):
        if self.highlight_turtle:
            self.highlight_turtle.clear()

    def __str__(self):
        ''' 
            Returns a printable version of the board to print.
        '''
        explanation = 'State of the board:\n'
        board_str = ''
        for row in self.board:
            board_str += str(row) + '\n' 
        printable_str = explanation + board_str

        return printable_str

    def __eq__(self, other):
        '''
            Compares two instances. 
            Returns True if they have the same board attribute, 
            False otherwise.
        '''
        return self.board == other.board
