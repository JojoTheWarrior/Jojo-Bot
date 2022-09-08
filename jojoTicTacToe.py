import random

board = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

remainingMoves = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9'
]

winningRows = [
    [0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]
]


def ruleSet():
    return ("Welcome to Tic-Tac-Toe!\n\t- The computer uses 'X'\n\t- You, the player, use '@'\n\t- The computer will "
            "go first\nGood luck!")


# user moves with @
# computer moves with X

class TTT:
    def __init__(self, userId):
        self.userId = userId
        self.board = board
        self.remainingMoves = remainingMoves
        self.compMoves = 0
        self.userMoves = 0

    def resetBoard(self, userId):
        self.board.clear()
        self.remainingMoves.clear()
        for i in range(1, 10):
            self.board.append(str(i))
            self.remainingMoves.append(str(i))

    def computerMove(self):
        # how many moves has the user done so far?
        if self.almostWon() != False:
            place = self.almostWon()
            print(place)
            self.remainingMoves.remove(str(place))
            self.board[self.board.index(str(place))] = 'X'
        else:
            if self.compMoves == 0 and self.userMoves == 0:
                # first move so far
                place = 5
            elif self.compMoves == 0 and self.userMoves == 1:
                # user moved once, computer's turn now
                if self.board[4] != '@':
                    # go middle if possible
                    place = 5
                else:
                    # otherwise, go corner
                    place = 1
            elif self.compMoves == 1 and self.userMoves == 1:
                # both have played once, computer must have one in the center
                userSpot = 0
                for x in range(9):
                    if self.board[x] == '@':
                        userSpot = x
                        break
                # if corner
                if userSpot == 0:
                    place = 7
                if userSpot == 2:
                    place = 1
                if userSpot == 8:
                    place = 3
                if userSpot == 6:
                    place = 9
                # if edge
                if userSpot == 1 or 3:
                    place = 9
                else:
                    place = 1
            elif self.compMoves == 1 and self.userMoves == 2:
                if self.board[4] == '@':
                    # player got the centre
                    place = 3
                else:
                    # computer got the centre
                    corners = 0
                    if self.board[0] == '@':
                        corners += 1
                    if self.board[2] == '@':
                        corners += 1
                    if self.board[6] == '@':
                        corners += 1
                    if self.board[8] == '@':
                        corners += 1

                    if corners == 0:
                        # all edges
                        if self.board[3] == '@' and self.board[7] == '@':
                            # only double trap scenario for the selection of 3
                            place = 7
                        else:
                            place = 3
                    elif corners == 1:
                        # one corner, one edge
                        if self.board[1] == '@':
                            if self.board[8] == '@':
                                place = 3
                            else:
                                place = 1
                        elif self.board[3] == '@':
                            if self.board[2] == '@':
                                place = 1
                            else:
                                place = 7
                        elif self.board[7] == '@':
                            if self.board[0] == '@':
                                place = 7
                            else:
                                place = 9
                        elif self.board[5] == '@':
                            if self.board[0] == '@':
                                place = 3
                            else:
                                place = 9
                    else:
                        # two corners
                        place = 4
            elif self.compMoves == 2 and self.userMoves == 2:
                if self.board[4] == 'X':
                    # computer has center, and checking corners rn
                    cCor = 0
                    uCor = 0
                    if self.board[0] == '@':
                        uCor += 1
                    if self.board[2] == '@':
                        uCor += 1
                    if self.board[6] == '@':
                        uCor += 1
                    if self.board[8] == '@':
                        uCor += 1

                    if self.board[0] == '@':
                        cCor += 1
                    if self.board[2] == '@':
                        cCor += 1
                    if self.board[6] == '@':
                        cCor += 1
                    if self.board[8] == '@':
                        cCor += 1

                    if cCor == 1 and uCor == 1:
                        place = 7
            else:
                # completely random
                place = random.choice(self.remainingMoves)
            self.remainingMoves.remove(str(place))
            self.board[self.board.index(str(place))] = 'X'
        self.compMoves += 1

    def userCanMove(self, place):
        if not self.remainingMoves.__contains__(str(place)):
            return False
        else:
            return True

    def userMove(self, place):
        self.remainingMoves.remove(str(place))
        self.board[self.board.index(str(place))] = '@'
        self.userMoves += 1

    def hasWon(self):
        for x in winningRows:
            a, b, c = x[0], x[1], x[2]
            if self.board[a] == self.board[b] == self.board[c]:
                return True
        return False

    def almostWon(self):
        """
        :return: Returns a boolean representing whether there are wins. If True, returns one number representing
        the winning spot. Always returns optimal move.
        """
        ws = -1  # winning square
        bs = -1  # blocking square
        for x in winningRows:
            a, b, c = x[0], x[1], x[2]
            if self.board[a] == self.board[b] != self.board[c]:
                if self.board[b] == 'X' and self.board[c] != '@':
                    ws = c
                elif self.board[b] == '@' and self.board[c] != 'X':
                    bs = c
            elif self.board[a] == self.board[c] != self.board[b]:
                if self.board[a] == 'X' and self.board[b] != '@':
                    ws = b
                elif self.board[a] == '@' and self.board[b] != 'X':
                    bs = b
            elif self.board[b] == self.board[c] != self.board[a]:
                if self.board[b] == 'X' and self.board[a] != '@':
                    ws = a
                elif self.board[b] == '@' and self.board[a] != 'X':
                    bs = a
        # if there is a winning square, go there. otherwise, go to blocking square
        if ws != -1:
            return ws + 1
        elif bs != -1:
            return bs + 1
        else:
            return False

    def printBoard(self):
        return str(
            "`" + self.board[0] + " " + self.board[1] + " " + self.board[2] + "`\n`" + self.board[3] + " " + self.board[
                4] +
            " " + self.board[5] + "`\n`" + self.board[6] + " " + self.board[7] + " " + self.board[8] + "`")
