# Heavily edited version of skeleton-tictactoe.py (original included in project)
# original based on code from https://stackabuse.com/minimax-and-alpha-beta-pruning-in-python


# If you are reading this and are trying to understand this code
# I pity you
import time
import sys

file = "C:\\Users\\ConnorK\\Desktop\\Game_Output\\output.txt"


# https://stackoverflow.com/questions/14906764/how-to-redirect-stdout-to-both-file-and-console-with-scripting
class Logger(object):
    def __init__(self):
        self.terminal = sys.stdout
        self.log = open(file, "w")

    def write(self, message):
        self.terminal.write(message)
        self.log.write(message)

    def flush(self):
        # this flush method is needed for python 3 compatibility.
        # this handles the flush command by doing nothing.
        # you might want to specify some extra behavior here.
        pass




Alphabet = ['A','B','C','D','E','F','G','H','I','J',]

class Game:
    MINIMAX = 0
    ALPHABETA = 1
    HUMAN = 2
    AI = 3

    def __init__(self, recommend=True):
     #   self.initialize_game()
         self.recommend = recommend
         self.X_wins = 0
         self.Y_wins = 0

    def initialize_game(self,n,b,s,d1,d2,t):
        #should this be elsewhere? Should we send it?
        self.recommend = True
        self.n = n
        self.b = b
        self.s = s

        self.d1 = d1
        self.d2 = d2
        self.depth = d1

        self.h_evaluations = 0
        self.h = "e2"
        self.t = t
        self.some_time = 0

        self.current_state = self.generate_board(self.b)

        # Player X always plays first
        self.player_turn = 'X'

    def generate_board(self,blocks):
        # Generate board based off n and b
        board = []
        board = [['.' for i in range(self.n)] for i in range(self.n)]
        for elem in blocks:
            col = Alphabet.index(elem[0])
            row = int(elem[1])
            board[row][col] = '*'
        return board

    def set_cur_depth(self,depth):
        self.depth = depth

    def draw_board(self):
        print("  ", end="")
        # Print Alphabetical Headings
        for col in range(0,self.n):
            print("  "+Alphabet[col]+"  ", end="")
        print("")

        # Print Board
        for num,row in enumerate(self.current_state):
            print(str(num)+" ", end="")
            print(row)
        print("")

    def is_valid(self, px, py):
        if px < 0 or px > (self.n-1) or py < 0 or py > (self.n-1):
            return False
        elif self.current_state[px][py] != '.':
            return False
        else:
            return True

    def convert_move(self, move):
        px = -1
        py = -1

        if len(move) != 2:
            return px,py

        for index in range(0,self.n):
            if move[0] == Alphabet[index]:
                py = index
                break

        if str.isnumeric(move[1]) and int(move[1]) in range(0,self.n):
            px = int(move[1])

        return px,py

    def transform_move(self,x,y):
        p1 = Alphabet[y]
        p2 = str(x)
        coord = p1 + p2
        return coord

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
                            #self.draw_board()
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
                            #self.draw_board()
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
                        #self.draw_board()
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
                        #self.draw_board()
                        return self.current_state[reversed_x][index]
                else:
                    count = 0
            else:
                count = 0

        # Is board full?
        for row in range(0, self.n):
            for col in range(0, self.n):
                if self.current_state[row][col] == '.':
                    return None



        # Returns '.' means it's a tie
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
            #px = int(input('enter the x coordinate: '))
            #py = int(input('enter the y coordinate: '))

            move = (input('enter the coordinates(A..)(0..): '))
            (px,py) = self.convert_move(move)


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

    def heuristic(self):
        # Note: B = X and W = 0
        x = 0
        y = 0
        #return 1,x,y
        b_count = 0
        w_count = 0
        b_score = 0
        w_score = 0
        self.h_evaluations += 1

        if self.h == "e1":
            # Vertical win : this is E1
            for col in range(0, self.n):
                for row in range(0, self.n):
                    if self.current_state[row][col] not in {'.', '*'}:
                        current_tok = self.current_state[row][col]
                        if current_tok == 'X':
                            b_score += 10
                        else:
                            w_score += 10
                        if row != self.n - 1 and self.current_state[row + 1][col] not in {'.', '*'}:
                            next_tok = self.current_state[row + 1][col]
                            if current_tok == next_tok:
                                if current_tok == 'X':
                                    b_score += 100
                                else:
                                    w_score += 100

            if self.player_turn == 'X':
                return -b_score, 1, 1  # Note the negative sign
            if self.player_turn == 'O':
                return w_score, 1, 1
        else:
            val = 0
            xCount = 0
            oCount = 0
            for col in range(0, self.n):
                for elem in self.current_state[col]:
                    if elem == "X":
                        xCount += 1
                    elif elem == "O":
                        oCount += 1
                if xCount == 3:
                    val += 1000
                elif oCount == 3:
                    val -= 1000
                elif xCount == 2:
                    val += 100
                elif oCount == 2:
                    val -= 100
                elif xCount == 1:
                    val += 10
                elif oCount == 1:
                    val -= 10
            for row in range(0, self.n):
                for elem in self.current_state[row]:
                    if elem == "X":
                        xCount += 1
                    elif elem == "O":
                        oCount += 1
                if xCount == 3:
                    val += 1000
                elif oCount == 3:
                    val -= 1000
                elif xCount == 2:
                    val += 100
                elif oCount == 2:
                    val -= 100
                elif xCount == 1:
                    val += 10
                elif oCount == 1:
                    val -= 10
            diag_front = [ self.current_state[i][i] for i in range(len(self.current_state)) ]
            for x in diag_front:
                if elem == "X":
                    xCount += 1
                elif elem == "O":
                    oCount += 1
            if xCount == 3:
                val += 1000
            elif oCount == 3:
                val -= 1000
            elif xCount == 2:
                val += 100
            elif oCount == 2:
                val -= 100
            elif xCount == 1:
                val += 10
            elif oCount == 1:
                val -= 10
            diag_back = [ row[-i-1] for i,row in enumerate(self.current_state) ]
            for y in diag_back:
                if elem == "X":
                    xCount += 1
                elif elem == "O":
                    oCount += 1
            if xCount == 3:
                val += 1000
            elif oCount == 3:
                val -= 1000
            elif xCount == 2:
                val += 100
            elif oCount == 2:
                val -= 100
            elif xCount == 1:
                val += 10
            elif oCount == 1:
                val -= 10
            if self.player_turn == 'X':
                return -val, 1, 1  # Note the negative sign
            if self.player_turn == 'O':
                return val, 1, 1


        print("Very concerning")
        return 1,0,0



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
        for i in range(0, self.n):
            for j in range(0, self.n):
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

    def alphabeta(self, alpha=-2, beta=2,depth=2, max=False):

        if round(time.time() - self.some_time, 7) > self.t:
            return self.heuristic()

        #print(depth)
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

        if depth > 0:
            depth = depth - 1

            for i in range(0, self.n):
                for j in range(0, self.n):
                    if self.current_state[i][j] == '.':
                        if max:
                            self.current_state[i][j] = 'O'
                            (v, _, _) = self.alphabeta(alpha, beta,depth, max=False)
                            print("Here O: "+str(v)+" "+str(value))
                            if v > value:
                                value = v
                                x = i
                                y = j
                        else:
                            self.current_state[i][j] = 'X'
                            (v, _, _) = self.alphabeta(alpha, beta,depth, max=True)
                            print("Here X: " + str(v) + " " + str(value))
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
        else:
            return self.heuristic()

        #print("Found: "+str(y)+" "+str(x))
        return (value, x, y)

    # Temporary Edited version of play with limited functionality
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
            self.some_time = start
            self.h_evaluations = 0

            if algo == self.MINIMAX:
                if self.player_turn == 'X':
                    (_, x, y) = self.minimax(max=False)
                else:
                    (_, x, y) = self.minimax(max=True)
            else:  # algo == self.ALPHABETA
                if self.player_turn == 'X':
                    #self.depth = self.d1
                    (m, x, y) = self.alphabeta(-2,2,self.d1,max=False)
                else:
                    #self.depth = self.d2
                    (m, x, y) = self.alphabeta(-2,2,self.d2,max=True)

            end = time.time()

            if (self.player_turn == 'X' and player_x == self.HUMAN) or (
                    self.player_turn == 'O' and player_o == self.HUMAN):
                print(F'i Evaluation time: {round(end - start, 7)}s')
                print(F'ii Heuristic evaluations: '+str(self.h_evaluations))
                print(F'Recommended move: '+ self.transform_move(x,y))
                (x, y) = self.input_move()

            if (self.player_turn == 'X' and player_x == self.AI) or (self.player_turn == 'O' and player_o == self.AI):
                print(F'i Evaluation time: {round(end - start, 7)}s')
                print(F'ii Heuristic evaluations: ' + str(self.h_evaluations))
                print(F'Player {self.player_turn} under AI control plays: ' + self.transform_move(x,y))

            self.current_state[x][y] = self.player_turn
            self.switch_player()


def some_setup():
    data = []
    n = int(input('Enter the the board size n (for board n x n): '))
    while True:
        if n in range(3, 11):
            break
        n = int(input('Invalid board size (range 3-10) - re-enter size n: '))
    blocks = []
    b = int(input('Enter the amount of blocks on the board: '))
    for x in range(b):
        [bx, by] = (input('Enter the coordinate(A..)(0..) of block {}: '.format(x+1)))
        blocks.append([bx, by])

    s = int(input('Enter the winning line-up size: '))

    # Player X
    d1 = int(input('Enter the the depth for player 1 (d1): '))

    # Player Y
    d2 = int(input('Enter the the depth for player 2 (d2): '))

    t = int(input('Enter the the max amount of time to make a move: '))

    a = int(input('Enter:  minimax (0) or alphabeta (1): '))
    type = int(input('Enter 1 for H-H, 2 for H-AI, 3 for AI-H, 4 for AI-AI: '))

    data.append(n)
    data.append(blocks)
    data.append(s)
    data.append(d1)
    data.append(d2)
    data.append(t)
    data.append(a)
    data.append(type)
    return data

def game_trace_files(n,b,s,t,blocks):
    f = open("gameTrace-{}{}{}{}.txt".format(n,b,s,t), "w")
    f.write("n={} b={} s={} t={}+\n".format(n,b,s,t))
    f.write("blocks=[")
    for elem in blocks:
        f.write("{},".format(elem))
    f.write("]+\n")


def main():

    g = Game(recommend=True)
    while True:
        data = some_setup()
        g.initialize_game(data[0], data[1], data[2], data[3], data[4], data[5])

        # Print output to file and to stdout
        # sys.stdout = Logger()
        print("n: " + str(data[0]))
        print("b: " + str(data[1]))
        print("s: " + str(data[2]))
        print("d1: " + str(data[3]))
        print("d2: " + str(data[4]))

        if data[6] == 1:
            if data[7] == 1:
                g.play(algo=Game.ALPHABETA, player_x=Game.HUMAN, player_o=Game.HUMAN)
            elif data[7] == 2:
                g.play(algo=Game.ALPHABETA, player_x=Game.HUMAN, player_o=Game.AI)
            elif data[7] == 3:
                g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.HUMAN)
            else:
                g.play(algo=Game.ALPHABETA, player_x=Game.AI, player_o=Game.AI)
        else:
            if data[7] == 1:
                g.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.HUMAN)
            elif data[7] == 2:
                g.play(algo=Game.MINIMAX, player_x=Game.HUMAN, player_o=Game.AI)
            elif data[7] == 3:
                g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.HUMAN)
            else:
                g.play(algo=Game.MINIMAX, player_x=Game.AI, player_o=Game.AI)

        # sys.stdout = sys.stdout
        p = input('Play again? (Y/N): ')
        if (p != 'Y'):
            break



if __name__ == "__main__":
    main()
