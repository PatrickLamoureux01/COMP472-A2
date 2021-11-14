# Heavily edited version of skeleton-tictactoe.py (original included in project)
# original based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python


#Notes
#If program generates an illegal move, then it will automatically lose the game
#You do not need to check the validity of these input values; you can assume that they will be valid.
# 2 output files
# e1 and e2 heuristics
import time

Alphabet = ['A','B','C','D','E','F','G','H','I','J',]

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3




    def __init__(self, recommend=True):
     #   self.initialize_game()
         self.recommend = recommend

    def initialize_game(self,n,b,s):
        #should this be elsewhere? Should we send it?
        self.recommend = True
        self.n = n
        self.b = b
        self.s = s

        self.current_state = self.generate_board()

        # Player X always plays first
        self.player_turn = 'X'

    def generate_board(self):
        # Generate board based off n

        return  [['.' for i in range(self.n)] for i in range(self.n)]


    def draw_board(self):
        for row in self.current_state:
            print(row)
        print("")

    def is_valid(self, px, py):
        if px < 0 or px > (self.n-1) or py < 0 or py > (self.n-1):
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True



    def is_end(self):
        # Keeps track of how many consecutive matches we have
        count = 0
        # Current player token found
        current_tok = '0'
        # Next token
        next_tok = '1'

        # Vertical win
        for col in range(0, self.n):
            for row in range(0, self.n):
                # Get current token and next token if not empty or a bloc
                if self.current_state[row][col] not in {'.', '*'}:
                    current_tok = self.current_state[row][col]
                    if row != self.n - 1 and self.current_state[row+1][col] not in {'.', '*'}:
                        next_tok = self.current_state[row+1][col]

                        if current_tok == next_tok:
                            count += 1
                        if count == self.s - 1:
                            return self.current_state[row][col]

                    else:
                        count = 0
                else:
                    count = 0

        # Horizontal win
        for row in range(0, self.n):
            for col in range(0, self.n):
                # Get current token and next token if not empty or a bloc
                if self.current_state[row][col] not in {'.', '*'}:
                    current_tok = self.current_state[row][col]
                    if col != self.n - 1 and self.current_state[row][col + 1] not in {'.', '*'}:
                        next_tok = self.current_state[row][col + 1]

                        if current_tok == next_tok:
                            count += 1
                        if count == self.s - 1:
                            return self.current_state[row][col]

                    else:
                        count = 0
                else:
                    count = 0

        # Main diagonal win
        for index in range(0, self.n):
            if self.current_state[index][index] not in {'.', '*'}:
                current_tok = self.current_state[index][index]
                if index != self.n - 1 and self.current_state[index+1][index + 1] not in {'.', '*'}:
                    next_tok = self.current_state[index+1][index + 1]

                    if next_tok == current_tok:
                        count += 1
                    if count == self.s - 1:
                        return self.current_state[index][index]
                else:
                    count = 0
            else:
                count = 0

        # Second diagonal win
        for index in range(0, self.n):
            reversed_x = (self.n-1)-index
            if self.current_state[reversed_x][index] not in {'.', '*'}:
                current_tok = self.current_state[reversed_x][index]
                if index != self.n - 1 and self.current_state[reversed_x - 1][index + 1] not in {'.', '*'}:
                    next_tok = self.current_state[reversed_x - 1][index + 1]

                    if next_tok == current_tok:
                        count += 1
                    if count == self.s - 1:
                        return self.current_state[reversed_x][index]
                else:
                    count = 0
            else:
                count = 0

        # Is board full?
        for row in range(0, self.n):
            for col in range(0, self.n):
                if(self.current_state[row][col] == '.'):
                    return None



        # Returns '.' means it's a tie
        return '.'



    def is_end2(self):

        #Keeps track of how many consecutive matches we have
        count = 0
        #Current player token found
        current = '0'
        #Next token
        next = '1'

        # Vertical win
        for i in range(0, self.n):
            if (self.current_state[0][i] != '.' and
                    self.current_state[0][i] == self.current_state[1][i] and
                    self.current_state[1][i] == self.current_state[2][i]):
                return self.current_state[0][i]

        for col in range(0, self.n-1):
            for row in range(0, self.n-1):

                #Get current token and next token if not empty or a bloc
                if self.current_state[col][row] not in {'.','*'}:
                    current = self.current_state[col][row]
                    if row != self.n-1 and self.current_state[row][col+1] not in {'.','*'}:
                        next = self.current_state[row][col+1]
                    else:
                        count = 0
                else:
                    count = 0

                if current == next:
                    count += 1
                if count == self.s:
                    return self.current_state[row][col]



        # Horizontal win
        for i in range(0, 3):
            if (self.current_state[i] == ['X', 'X', 'X']):
                return 'X'
            elif (self.current_state[i] == ['O', 'O', 'O']):
                return 'O'
        # Main diagonal win
        if (self.current_state[0][0] != '.' and
                self.current_state[0][0] == self.current_state[1][1] and
                self.current_state[0][0] == self.current_state[2][2]):
            return self.current_state[0][0]
        # Second diagonal win
        if (self.current_state[0][2] != '.' and
                self.current_state[0][2] == self.current_state[1][1] and
                self.current_state[0][2] == self.current_state[2][0]):
            return self.current_state[0][2]
        # Is whole board full?
        for i in range(0, 3):
            for j in range(0, 3):
                # There's an empty field, we continue the game
                if (self.current_state[i][j] == '.'):
                    return None
        # It's a tie!
        return '.'

    def check_end(self):
        self.result = self.is_end()
        # Printing the appropriate message if the game has ended
        if self.result != None:
            if self.result == 'X':
                print('The winner is X!')
            elif self.result == 'O':
                print('The winner is O!')
            elif self.result == '.':
                print("It's a tie!")
            #self.initialize_game()
        return self.result

    def input_move(self):
        while True:
            print(F'Player {self.player_turn}, enter your move:')
            px = int(input('enter the x coordinate: '))
            py = int(input('enter the y coordinate: '))
            if self.is_valid(px, py):
                return (px, py)
            else:
                print('The move is not valid! Try again.')

    def switch_player(self):
        if self.player_turn == 'X':
            self.player_turn = 'O'
        elif self.player_turn == 'O':
            self.player_turn = 'X'
        return self.player_turn

    def minimax(self, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.minimax(max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.minimax(max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
        return (value, x, y)

    def alphabeta(self, alpha=-2, beta=2, max=False):
        # Minimizing for 'X' and maximizing for 'O'
        # Possible values are:
        # -1 - win for 'X'
        # 0  - a tie
        # 1  - loss for 'X'
        # We're initially setting it to 2 or -2 as worse than the worst case:
        value = 2
        if max:
            value = -2
        x = None
        y = None
        result = self.is_end()
        if result == 'X':
            return (-1, x, y)
        elif result == 'O':
            return (1, x, y)
        elif result == '.':
            return (0, x, y)
        for i in range(0, 3):
            for j in range(0, 3):
                if self.current_state[i][j] == '.':
                    if max:
                        self.current_state[i][j] = 'O'
                        (v, _, _) = self.alphabeta(alpha, beta, max=False)
                        if v > value:
                            value = v
                            x = i
                            y = j
                    else:
                        self.current_state[i][j] = 'X'
                        (v, _, _) = self.alphabeta(alpha, beta, max=True)
                        if v < value:
                            value = v
                            x = i
                            y = j
                    self.current_state[i][j] = '.'
                    if max:
                        if value >= beta:
                            return (value, x, y)
                        if value > alpha:
                            alpha = value
                    else:
                        if value <= alpha:
                            return (value, x, y)
                        if value < beta:
                            beta = value
        return (value, x, y)

    def play(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return
            start = time.time()
            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    (m, x, y) = self.alphabeta(max=False)
                else:
                    (m, x, y) = self.alphabeta(max=True)
            end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                if self.recommend:
                    print(F'Evaluation time: {round(end - start, 7)}s')
                    print(F'Recommended move: x = {x}, y = {y}')
                (x, y) = self.input_move()
            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'Evaluation time: {round(end - start, 7)}s')
                print(F'Player {self.player_turn} under AI control plays: x = {x}, y = {y}')
            self.current_state[x][y] = self.player_turn
            self.switch_player()

    # Temporary Edited version of play with limited functionality
    def play2(self, algo=None, player_x=None, player_o=None):
        if algo == None:
            algo = self.ALPHABETA
        if player_x == None:
            player_x = self.HUMAN
        if player_o == None:
            player_o = self.HUMAN
        while True:
            self.draw_board()
            if self.check_end():
                return

            #Temp, remove later
            (x, y) = 0,0

            #start = time.time()
            #end = time.time()
            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                (x, y) = self.input_move()

            self.current_state[x][y] = self.player_turn
            self.switch_player()
def some_setup():
    data = []
    n = int(input('enter the the board size n (for board n x n): '))
    while True:
        if n in range(3, 11):
            break
        n = int(input('Invalid board size (range 3-10) - re-enter size n: '))

    #s = int(input('enter the winning line-up size: '))
    #b = int(input('enter the amount of blocks on the board: '))
    # loop here b times each time asking for a UNIQUE bloc position

    # Don't know if these are console inputs are just variables we keep
    #d1 = int(input('enter the maximum depth for player 1: '))
    #d2 = int(input('enter the maximum depth for player 2: '))
    #a = int(input('enter:  minimax (FALSE) or alphabeta (TRUE)'))

    data.append(n)
    return data

def main():
    g = Game(recommend=True)
    data = some_setup()
    g.initialize_game(data[0], 1, 3)
    #g.draw_board()
    #g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
    #g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)

    # CHANGE TO g.play once functionality of program is further along
    g.play2(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN)


if __name__ == "__main__":
    main()
    #generate_board(5)

# Disabled for now
# MinMax
# Alpha
# is_end
# check_end