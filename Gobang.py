import sys
import string
import copy

# parameters taken are size and flag to play white or black
# must support only one command, <move> which takes in (letter,number) pair (column,row)
# no more than 30 seconds to decide move


class Gobang:

    def __init__(self, size, color):
        # self.gameboard = numpy.zeros(shape=(size,size))
        self.gameboard = [[0 for x in range(size)] for y in range(size)]
        self.size = size
        self.movesLeft = size * size
        self.AI= color
        if self.AI == 'b':
            self.player = 'w'
        else:
            self.player = 'b'



    def current_board(self):
        return self.gameboard

    def any_moves_left(self,board):
        for x in range(0, self.size):
            for y in range(0, self.size):
                if board[x][y] == 0:
                    return True
        return False


    def did_game_end(self, move, board, player):
        return self.hor_check(move,board,player) or self.ver_check(move,board,player) or self.pos_diagonal_check(move,board,player) or self.neg_diagonal_check(move,board,player)


    def neg_diagonal_check(self, point, board, player):
        count = 0
        char = player
        max = 9
        round = 0
        hor = point[1]
        ver = point[0]
        otro = 0

        while (hor >= 0 and hor <= self.size - 1 and ver >= 0 and ver <= self.size - 1 and otro <= 4):
            hor -= 1
            ver -= 1
            otro +=1
        hor += 1
        ver += 1

        while (hor >= 0 and hor <= self.size - 1 and ver >= 0 and ver <= self.size - 1 and round <= max):
            if board[ver][hor] == char:
                count += 1
            elif count == 5:
                return True
            else:
                count = 0
            max += 1
            ver += 1
            hor += 1
            # print count
        return False


    def pos_diagonal_check(self, point, board, player):
        # if this path length is less than 5, then we don't give a damn about it
        count = 0
        otro = 0
        char = player
        max = 9
        round = 0
        hor = point[1]
        ver = point[0]
        # find starting spot from below
        while(hor >= 0 and hor <= self.size-1 and ver >= 0 and ver <= self.size-1 and otro <= 4):
            hor -=1
            ver +=1
            otro +=1
        hor +=1
        ver -=1

        while(hor >= 0 and hor <= self.size-1 and ver >= 0 and ver <= self.size-1 and round<=max):
            if board[ver][hor] == char:
                count += 1
            elif count == 5:
                return True
            else:
                count = 0
            max +=1
            ver -=1
            hor +=1
        return False



    def ver_check(self, point, board, player):
        ver_start = None
        ver_stop = None

        bottom_min = 0
        top_max = self.size - 1

        # bottom to top
        # check if up or down is the one that does not fit
        if point[1] + 4 > top_max:
            # close to the top (or in this case bottom)
            ver_stop = top_max
            ver_start = point[1] - 4

        elif point[1] - 4 < bottom_min:
            ver_start = bottom_min
            ver_stop = point[1] + 4

        else:
            # all good
            ver_start = point[1] - 4
            ver_stop = point[1] + 4

        # we can now traverse from low number to high number
        ver_char = player
        ver_count = 0
        for i in range(ver_start,ver_stop+1):
            if board[i][point[1]] == ver_char:
                ver_count +=1
            elif ver_count == 5:
                return True

        return False

    def hor_check(self, point, board, player):
        hor_start = None
        hor_stop = None

        leftmin = 0
        rightmax = self.size - 1

        # left to right
        # check if left or right is the one that can't fit or maybe they all good
        if point[1] + 4 > rightmax:
            # close to the right edge
            hor_stop = rightmax
            hor_start = point[1] - 4
        elif point[1] - 4 < leftmin:
            # close to the left edge
            hor_start = leftmin
            hor_stop = point[1] + 4
        else:
            hor_start = point[1] - 4
            hor_stop = point[1] + 4

        # we can now loop on the left to right to check for a win
        hor_char = player
        hor_count = 0

        for i in range(hor_start, hor_stop + 1):
            if board[point[0]][i] == hor_char:
                hor_count += 1
            elif hor_count == 5:
                return True

        return False


    def valid_move(self,move,board):
        if board[move[0]][move[1]] != 0:
            return False
        else:
            return True

    def print_board(self):
        sys.stdout.write("  ")
        i = 0
        for c in string.ascii_lowercase:
            i += 1
            if i > self.size:
                break
            sys.stdout.write("   %s" % c)
        sys.stdout.write("\n   +")
        for i in range(0, self.size):
            sys.stdout.write("---+")
        sys.stdout.write("\n")

        for i in range(0, self.size):
            sys.stdout.write("%2d |" % (i + 1))
            for j in range(0, self.size):
                if self.gameboard[i][j] == 'w':
                    sys.stdout.write(" L |")
                elif self.gameboard[i][j] == 'b':
                    sys.stdout.write(" D |")
                else:
                    sys.stdout.write("   |")
            sys.stdout.write("\n   +")
            for j in range(0, self.size):
                sys.stdout.write("---+")
            sys.stdout.write("\n")

    def get_avail_moves(self, board):
        """
        Given a gameboard, returns spots in board that are not taken
        """

        moves = []
        for x in range(0,self.size):
            for y in range(0,self.size):
                if board[x][y] == 0:
                    moves.append((x,y))
        return moves



    def hor_bounding_box(self, point, size):
        # left to right
        hor_min = None
        hor_max = None

        if point[1] - 5 < 0:
            # if here then the left won't fit
            hor_min = 0
            hor_max = 10

        elif point[1] + 5 > size - 1:
            hor_max = size - 1
            hor_min = hor_max - 10
        else:
            hor_min = point[1] - 5
            hor_max = point[1] + 5

        return hor_min, hor_max

    def ver_bounding_box(self, point, size):
        # up and down
        ver_min = None
        ver_max = None

        if point[0] - 5 < 0:
            ver_min = 0
            ver_max = 10
        elif point[0] + 5 > size - 1:
            ver_max = size - 1
            ver_min = ver_max - 10
        else:
            ver_min = point[0] - 5
            ver_max = point[0] + 5

        return ver_min, ver_max

    def it_fits(self, point, size):
        lr = None
        tp = None
        # for point [0]
        if point[0] - 5 < 0:
            tp = False
        elif point[0] + 5 > size - 1:
            tp = False
        else:
            tp = True

        # for point [1]
        if point[1] - 5 < 0:
            lr = False
        elif point[1] + 5 > size - 1:
            lr = False
        else:
            lr = True

        return lr and tp

    def get_perimeter(self, point, size):
        hor_min = None
        hor_max = None
        ver_min = None
        ver_max = None

        if self.it_fits(point, size):
            hor_min = point[1] - 5
            hor_max = point[1] + 5
            ver_max = point[0] + 5
            ver_min = point[0] - 5
            # topL = (point[0]-5,point[1]-5)
            # topR = (point[0]-5,point[1]+5)
            # bottomL = (point[0]+5,point[1]-5)
            # bottomR = (point[0]+5,point[1]+5)
            return hor_min, hor_max, ver_min, ver_max

        else:
            hor_min, hor_max = self.hor_bounding_box(point, size)
            ver_min, ver_max = self.ver_bounding_box(point, size)
            return hor_min, hor_max, ver_min, ver_max




    def alter_get_avail_moves(self, board, lastMove):
        boundaries = self.get_perimeter(lastMove,self.size)
        moves = []
        for x in range(boundaries[2], boundaries[3]):
            for y in range(boundaries[0], boundaries[1]):
                if board[x][y] == 0:
                    moves.append((x, y))
        return moves




    def find_max(self, board,lastMove):
        if self.size > 11:
            moves = self.alter_get_avail_moves(board,lastMove)
        else:
            moves = self.get_avail_moves(board)

        # print moves
        currBoard = copy.deepcopy(board)
        min = float('-inf')
        next_move = None
        for move in moves:
            # print move
            # get moves from that move
            curr = self.place_move(currBoard,move,self.AI)
            if self.size > 11:
                moves2 = self.alter_get_avail_moves(curr,lastMove)
            else:
                moves2 = self.get_avail_moves(curr)
            temp = self.find_min(moves2,curr,min)
            # print "THE VALUE WAS: ",temp
            if temp > min:
                min = temp
                next_move = move
            trash = self.place_move(currBoard, move, 0)
        return next_move




    def find_min(self, moves, board, best):
        # just look at each moves and evaluate score, return smallest one
        min = float('inf')
        next_move = None
        currBoard = copy.deepcopy(board)
        for move in moves:
            curr = self.place_move(currBoard, move, self.player)
            # print "NAAACAS",curr
            temp = self.evaluate(curr)
            # print "move, temp: ",move,temp
            if temp < min:
                min = temp
                next_move = move
            trash = self.place_move(currBoard, move,0)
            if best != float('-inf') and min <= best:
                return min
        return min


    def place_move(self,board,move,player):
        """
        :param board:
        :param move:
        :param player: used to indicate whether to use 'b' or 'w'
        :return: modified board
        """
        board[move[0]][move[1]] = player
        return board




    def row_eval(self, board):

        """
        :param board: takes in a state and does the math for a particular row
        :return: whiteCount and blackCount arrays
        """
        whiteCount = [0, 0, 0, 0, 0]
        blackCount = [0, 0, 0, 0, 0]
        char = None
        count = None
        # attacking row's first
        for x in range(0, self.size):
            for i in range(0, self.size):
                if i == 0:
                    # for when you start
                    char = board[x][i]
                    count = 1
                elif board[x][i] == char and board[x][i] != 0:
                    # if the pattern continues
                    count += 1
                elif board[x][i] == 0:
                    # if the pattern is interrupted by 0
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count - 1] += 1
                        count = 0
                        if i != self.size - 1:
                            char = board[x][i + 1]

                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count - 1] += 1
                        count = 0
                        if i != self.size - 1:
                            char = board[x][i + 1]

                    elif char == 0:
                        count = 0
                        if i != self.size - 1:
                            char = board[x][i + 1]

                else:
                    # all that is left is if it's the other symbol
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count - 1] += 1
                        count = 1
                        char = 'w'
                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count - 1] += 1
                        count = 1
                        char = 'b'
                    else:
                        count = 1
                        char = board[x][i]


            # handle last cell in row
            if char != 0 and count != 0:
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count - 1] += 1
                elif char == 'w':
                    if count > 5: count = 5
                    whiteCount[count - 1] += 1

        return whiteCount, blackCount


    def col_eval(self, board):

        whiteCount = [0, 0, 0, 0, 0]
        blackCount = [0, 0, 0, 0, 0]
        char = None
        count = None
        # attacking row's first
        for x in range(0, self.size):
            for i in range(0, self.size):
                if i == 0:
                    # for when you start
                    char = board[i][x]
                    count = 1
                elif board[i][x] == char and board[i][x] != 0:
                    # if the pattern continues
                    count += 1
                elif board[i][x] == 0:
                    # if the pattern is interrupted by 0
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count - 1] += 1
                        count = 0
                        if i != self.size - 1:
                            char = board[i + 1][x]

                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count - 1] += 1
                        count = 0
                        if i != self.size - 1:
                            char = board[i + 1][x]

                    elif char == 0:
                        count = 0
                        if i != self.size - 1:
                            char = board[i + 1][x]

                else:
                    # all that is left is if it's the other symbol
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count - 1] += 1
                        count = 1
                        char = 'w'
                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count - 1] += 1
                        count = 1
                        char = 'b'
                    else:
                        count = 1
                        char = board[i][x]

            # handle last cell in row
            if char != 0 and count != 0:
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count - 1] += 1
                elif char == 'w':
                    if count > 5: count = 5
                    whiteCount[count - 1] += 1
            # print "HEEERE",whiteCount, blackCount
        return whiteCount, blackCount


    def tB_diag(self, board):

        """
        Top to bottom diagonals
        :param board:
        :return:
        """
        whiteCount = [0, 0, 0, 0, 0]
        blackCount = [0, 0, 0, 0, 0]
        char = None
        count = None
        additional = (self.size-5) * 2

        # main diagonal
        for i in range(0, self.size):
            if i == 0:
                # for when you start
                char = board[i][i]
                count = 1
            elif board[i][i] == char and board[i][i] != 0:
                # if the pattern continues
                count += 1
            elif board[i][i] == 0:

                # if the pattern is interrupted by 0
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count - 1] += 1
                    count = 0
                    if i != self.size - 1:
                        char = board[i+1][i + 1]

                elif char == 'w':
                    if count > 5: count = 5
                    whiteCount[count - 1] += 1
                    count = 0
                    if i != self.size - 1:
                        char = board[i+1][i + 1]

                elif char == 0:
                    count = 0
                    if i != self.size - 1:
                        char = board[i+1][i + 1]

            else:
                # all that is left is if it's the other symbol
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count - 1] += 1
                    count = 1
                    char = 'w'
                else:
                    if count > 5: count = 5
                    whiteCount[count - 1] += 1
                    count = 1
                    char = 'b'



        # handle last cell in row
        if char != 0 and count != 0:
            if char == 'b':
                if count > 5: count = 5
                blackCount[count - 1] += 1
            elif char == 'w':
                if count > 5: count = 5
                whiteCount[count - 1] += 1


        # additional diagonals
        if additional == 0:
            return whiteCount, blackCount
        else:
            # print "ABBOUT TO DO ADDITIONAL" , whiteCount, blackCount
            #logic for additional diagonals
            a=1
            b=0
            max = self.size - 1
            char = None
            count = None
            for q in range(self.size-5):
                # print "OUTER LOOP BRUH", whiteCount, blackCount
                a = q + 1
                b = 0
                char = None
                count = None
                for i in range(max):
                    # print a,b
                    # print "currr ", whiteCount, blackCount
                    if i ==0:
                        char = board[a][b]
                        count = 1
                    elif board[a][b] == char and board[a][b] != 0:
                        count +=1
                    elif board[a][b] == 0:
                        if char == 'b':

                            blackCount[count-1] +=1
                            count = 0
                            if i != max-1:
                                char = board[a+1][b+1]

                        elif char == 'w':
                            if count > 5: count = 5
                            whiteCount[count-1] +=1
                            count = 0
                            if i != max-1:
                                char = board[a+1][b+1]

                        elif char == 0:
                            count = 0
                            if i != max-1:
                                char = board[a+1][b+1]

                    else:

                        if char == 'b':
                            if count > 5: count = 5
                            blackCount[count -1] +=1
                            count =1
                            char = 'w'
                        elif char == 'w':
                            if count > 5: count = 5
                            whiteCount[count-1] +=1
                            count = 1
                            char = 'b'
                        else:
                            count = 1
                            char = board[a][b]
                    a+=1
                    b+=1

                max-=1

                # handle extra ones
                if char != 0 and count != 0:
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count-1] +=1
                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count-1] +=1
            # print "WE RETURN THIS",whiteCount,blackCount


            b = 1
            a = 0
            max = self.size - 1
            char = None
            count = None
            for q in range(self.size - 5):
                # print "OUTER LOOP BRUH", whiteCount, blackCount
                b = q + 1
                a = 0
                char = None
                count = None
                for i in range(max):
                    # print a, b
                    # print "currr ", whiteCount, blackCount
                    if i == 0:
                        char = board[a][b]
                        count = 1
                    elif board[a][b] == char and board[a][b] != 0:
                        count += 1
                    elif board[a][b] == 0:
                        if char == 'b':
                            if count > 5: count = 5
                            blackCount[count - 1] += 1
                            count = 0
                            if i != max - 1:
                                char = board[a + 1][b + 1]

                        elif char == 'w':
                            if count > 5: count = 5
                            whiteCount[count - 1] += 1
                            count = 0
                            if i != max - 1:
                                char = board[a + 1][b + 1]

                        elif char == 0:
                            count = 0
                            if i != max - 1:
                                char = board[a + 1][b + 1]

                    else:

                        if char == 'b':
                            if count > 5: count = 5
                            blackCount[count - 1] += 1
                            count = 1
                            char = 'w'
                        elif char == 'w':
                            if count > 5: count = 5
                            whiteCount[count - 1] += 1
                            count = 1
                            char = 'b'
                        else:
                            count = 1
                            char = board[a][b]
                    a += 1
                    b += 1

                max -= 1

                # handle extra ones
                if char != 0 and count != 0:
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count - 1] += 1
                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count - 1] += 1





            return whiteCount, blackCount




    def bT_diag(self, board):

        """
        Bottom to top diagonals
        :param board:
        :return:
        """
        whiteCount = [0, 0, 0, 0, 0]
        blackCount = [0, 0, 0, 0, 0]
        char = None
        count = None
        additional = (self.size - 5) * 2
        x = self.size - 1
        # main diagonal
        for i in range(0, self.size):
            if i == 0:
                # for when you start
                char = board[x][i]
                count = 1
            elif board[x][i] == char and board[x][i] != 0:
                # if the pattern continues
                count += 1
            elif board[x][i] == 0:
                # if the pattern is interrupted by 0
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count - 1] += 1
                    count = 0
                    if i != self.size - 1:
                        char = board[x - 1][i + 1]

                elif char == 'w':
                    if count > 5: count = 5
                    whiteCount[count - 1] += 1
                    count = 0
                    if i != self.size - 1:
                        char = board[x - 1][i + 1]

                elif char == 0:
                    count = 0
                    if i != self.size - 1:
                        char = board[x - 1][i + 1]

            else:
                # all that is left is if it's the other symbol
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count - 1] += 1
                    count = 1
                    char = 'w'
                else:
                    if count > 5: count = 5
                    whiteCount[count - 1] += 1
                    count = 1
                    char = 'b'
            x -= 1

        # handle last cell in row
        if char != 0 and count != 0:
            if char == 'b':
                if count > 5: count = 5
                blackCount[count - 1] += 1
            elif char == 'w':
                if count > 5: count = 5
                whiteCount[count - 1] += 1


        # additional diagonals
        if additional == 0:
            return whiteCount, blackCount
        else:
            # return whiteCount, blackCount
            # logic for additional diagonals
            # additional var is # of additional

            a = self.size-1
            b = 1
            max = self.size - 1
            for q in range(self.size-5):
                a = self.size-1
                b = q +1
                char = None
                count = None

                for y in range(max):
                    # print a,b
                    if y == 0:
                        char = board[a][b]
                        count = 1
                    elif board[a][b] == char and board[a][b] !=0:
                        count += 1
                    elif board[a][b] == 0:
                        if char == 'b':
                            if count > 5: count = 5
                            blackCount[count-1] += 1
                            count = 0
                            if y != max-1:
                                char = board[a-1][b+1]

                        elif char == 'w':
                            if count > 5: count = 5
                            whiteCount[count-1] += 1
                            count = 0
                            if y != max-1:
                                char = board[a-1][b+1]

                        elif char == '0':
                            count=0
                            if y!=max-1:
                                char = board[a-1][b+1]

                    else:
                        if char == 'b':
                            if count > 5: count = 5
                            blackCount[count-1] +=1
                            count=1
                            char = 'w'
                        elif char == 'w':
                            if count > 5: count = 5
                            whiteCount[count-1] += 1
                            count = 1
                            char = 'b'
                        else:
                            count = 1
                            char = board[a][b]
                    a-=1
                    b+=1

                max -=1

                if char != 0 and count != 0:
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count-1] +=1
                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count-1] +=1
        # print "we return: ", whiteCount, blackCount



        max = self.size-1
        char = None
        count = None
        a = self.size-2
        newA = self.size-2
        for n in range(self.size-5):
            b =0

            for k in range(max):
                # logic goes here
                # print a,b
                if k == 0:
                    char = board[a][b]
                    count = 1
                elif board[a][b] == char and board[a][b] != 0:
                    count +=1
                elif board[a][b] == 0:
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count-1] += 1
                        count = 0
                        if k != max-1:
                            char = board[a-1][b+1]

                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count-1] += 1
                        count = 0
                        if k!=max-1:
                            char = board[a-1][b+1]

                    elif char == '0':
                        count = 0
                        if k!=max-1:
                            char = board[a-1][b+1]

                else:
                    if char == 'b':
                        if count > 5: count = 5
                        blackCount[count-1] += 1
                        count =1
                        char = 'w'
                    elif char == 'w':
                        if count > 5: count = 5
                        whiteCount[count-1] += 1
                        count = 1
                        char = 'b'
                    else:
                        count = 1
                        char = board[a][b]


                # modify a,b to next values
                a = a-1
                b =  b+ 1

            if char != 0 and count != 0:
                if char == 'b':
                    if count > 5: count = 5
                    blackCount[count-1] += 1
                elif char == 'w':
                    if count > 5: count = 5
                    whiteCount[count-1] += 1


            max = max-1
            newA = newA-1
            a = newA
        # print "we return: ", whiteCount, blackCount
        return whiteCount, blackCount

    def diag_eval(self, board):
        wCount, bCount = self.tB_diag(board)
        wC, bC = self.bT_diag(board)

        #print "TB DIAG" ,wCount, bCount


        for i in range(5):
            wCount[i] = wCount[i] + wC[i]
            bCount[i] = bCount[i] + bC[i]

        return wCount, bCount


    def test_eval(self, board):
        # wDiag, bDiag = self.diag_eval(board)
        wCol, bCol = self.row_eval(board)
        return wCol, bCol

    def evaluate(self, board):
        """
        Loop through entire board and calculate score based on heauristic
        :param board: board that you want to evaluate
        :return: score for that particular board
        """

        wDiag, bDiag = self.diag_eval(board)

        wRow, bRow = self.row_eval(board)

        wCol, bCol = self.col_eval(board)


        # print "wDiag: ", wDiag
        # print "wRow: ", wRow
        # print "wCol: ", wCol

        for i in range(5):
            wRow[i] = wRow[i] + wCol[i] + wDiag[i]
            bRow[i] = bRow[i] + bCol[i] + bDiag[i]



        if self.player == 'w':
            return (100*bRow[4] + 6*bRow[3] + 2*bRow[2] + bRow[1]) - (100*wRow[4] + 60*wRow[3] + 2*wRow[2] + wRow[1])
        else:
            return (100 * wRow[4] + 6 * wRow[3] + 2 * wRow[2] + bRow[1]) - (100* bRow[4] + 60 * bRow[3] + 2 * bRow[2] + bRow[1])


def move_played(move):
    # 1 is letter, 0 is number
    letter = chr(move[1] + 97)
    number = str(move[0] + 1)
    return str(letter + number)

def parse_move(game):
    """
    a maps to index 0
    1 maps to index 0
    :return move pair (letter,number)
    """
    # raw_move = raw_input("move: ")
    # letter = ord(raw_move[0])-97
    # number = int(raw_move[1:]) - 1

    good = False
    move = None
    max_letter = game.size + 96
    min_letter = 97
    max_number = game.size
    min_number = 1
    while not good:
        raw_move = raw_input("move: ")
        #raw_move = sys.stdin.readline()
        #sys.stdin.flush()
        # check if in valid format
        raw_letter = ord(raw_move[0])
        raw_number = int(raw_move[1:])

        if raw_letter <= max_letter and raw_letter >= min_letter and raw_number <= max_number and raw_number >= min_number:
            letter = ord(raw_move[0]) - 97
            number = int(raw_move[1:]) - 1

            move = [number, letter]
            # check if in range

            # check if spot is taken

            if game.valid_move(move,game.gameboard):
                good = True
            else:
                print "invalid move, pick again"
        else:
            print "invalid move, pick again"



    return (move[0],move[1])

def check_args():
    flags = [11, 'w']
    if len(sys.argv) == 1:
        return flags
    for i in range(len(sys.argv)):
        if sys.argv[i] == '-l':
            flags[1] = 'b'
        elif sys.argv[i] == '-n':
            flags[0] = int(sys.argv[i+1])
    return flags


def main():
    x = check_args()
    game = Gobang(x[0],x[1])
    i = 0
    game.print_board()
    # game.gameboard = game.place_move(game.gameboard, (5, 4), game.AI)
    if game.player == 'b':
        while(1): #later will be while(win condition or tie not met)
            sys.stdout.flush()
            if i == 0:

                currMove = parse_move(game)
                a = move_played(currMove)

                game.gameboard = game.place_move(game.gameboard, currMove, game.player)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()


                # print game.test_eval(game.gameboard)
                nextMove = game.find_max(game.gameboard,currMove)
                a = move_played(nextMove)
                # print "Move played: ", a

                game.gameboard = game.place_move(game.gameboard, nextMove, game.AI)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()
            else:

                currMove = parse_move(game)
                a = move_played(currMove)

                game.gameboard = game.place_move(game.gameboard, currMove, game.player)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()

                if game.did_game_end(currMove,game.gameboard,game.player):
                    print "Dark Player Won (Human)"
                    break

                if not game.any_moves_left(game.gameboard):
                    print "NO VALID MOVES LEFT"
                    break


                nextOne = game.find_max(game.gameboard,nextMove)
                a = move_played(nextOne)
                # print "Move played: ", a

                game.gameboard = game.place_move(game.gameboard, nextOne,game.AI)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()

                if game.did_game_end(nextOne,game.gameboard,game.AI):
                    print "Light Player Won (COM)"
                    break

                if not game.any_moves_left(game.gameboard):
                    print "NO VALID MOVES LEFT"
                    break

            i+=1
    else:
        # if player is white
        while (1):  # later will be while(win condition or tie not met

            if i ==0:
                # make initial AI move, perhaps top left corner first since it always exist (or any valid move in 5x5)
                nextMove = (0,0)
                a = move_played(nextMove)
                # print "Move played: ", a

                game.gameboard = game.place_move(game.gameboard, (0,0), game.AI)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                # print nextMove
                game.print_board()


                currMove = parse_move(game)
                a = move_played(currMove)
                game.gameboard = game.place_move(game.gameboard, currMove, game.player)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()


            else:
                nextMove = game.find_max(game.gameboard, nextMove)
                a = move_played(nextMove)
                # print "Move played: ", a

                game.gameboard = game.place_move(game.gameboard, nextMove, game.AI)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()

                if game.did_game_end(nextMove, game.gameboard, game.AI):
                    print "Dark Player Won (COM)"
                    break


                if not game.any_moves_left(game.gameboard):
                    print "NO VALID MOVES LEFT"
                    break

                currMove = parse_move(game)
                a = move_played(currMove)

                game.gameboard = game.place_move(game.gameboard, currMove, game.player)
                sys.stdout.write("Move played: %s\n" % a)
                sys.stdout.flush()
                game.print_board()

                if game.did_game_end(currMove, game.gameboard, game.AI):
                    print "Light Player Won (Human)"
                    break

                if not game.any_moves_left(game.gameboard):
                    print "NO VALID MOVES LEFT"
                    break

            i+=1

main()

