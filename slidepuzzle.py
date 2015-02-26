import heapq
# [[int]] -> bool
def isgoalstate(board):
    count = 0
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == count:
                count += 1
            else:
                return False
    return True
assert(isgoalstate([[0,1,2],[3,4,5],[6,7,8]]) == True)
assert(isgoalstate([[5,6,7],[3,4,2],[1,0,8]]) == False)

#row,col is position of zero
# int,int,[[int]] -> [[[int]]]
def generatesuccessors(row,col,board):
    rows = [row+x for x in [1,-1] if row+x<len(board) and row+x>-1]
    cols = [col+x for x in [1,-1] if col+x<len(board) and row+x>-1]
    moves = [[x,row] for x in cols]+[[col,y] for y in rows]
    successorstates = []
    for m in moves:
        newboard = [[board[i][j] for j in range(len(board))] for i in range(len(board))]
        t = newboard[col][row]
        newboard[col][row] = newboard[m[1]][m[0]]
        newboard[m[1]][m[0]] = t
        successorstates.append(newboard)
    return successorstates

#assert(generatesuccessors(1,1,[[2,3,4],[5,0,6],[1,7,8]]) == [[[2,3,4],[5,6,0],[1,7,8]],\
#        [[2,3,4],[0,5,6],[1,7,8]],[[2,3,4],[5,7,6],[1,0,8]],[[2,0,4],[5,3,6],[1,7,8]]])

#returns [col,row] for position of zero
# [[int]] -> [int,int]
def findzero(board):
    zero = [[i,j] for i in range(len(board)) for j in range(len(board)) if board[i][j] == 0]
    return zero[0]
assert(findzero([[0,1,2],[3,4,5],[6,7,8]]) == [0,0])
assert(findzero([[4,5,6],[6,7,0],[1,1,1]]) == [1,2])

def printboard(board):
    print '-'*20
    for row in board:
        print row

def tup(board):
    return tuple([tuple(row) for row in board])

#[[int]] -> int
def manhattanprioritizer(state):
    rank = 0
    for i in range(len(state)):
        for j in range(len(state)):
            actiondict = {0: i+j,1:i+abs(j-1),2:i+abs(j-2),3:abs(i-1)+j,\
            4:abs(i-1)+abs(j-1),5:abs(i-1)+abs(j-2),6:abs(i-2)+j,\
            7:abs(i-2)+abs(j-1),8:abs(i-2)+abs(j-2)}
            rank += actiondict[state[i][j]]
    return rank
assert(manhattanprioritizer([[0,1,2],[3,4,5],[6,7,8]]) == 0)
assert(manhattanprioritizer([[4,8,0],[3,7,2],[1,5,6]]) == 16)

#[heap],[[int]] -> [heap]
def addtovisit(statestovisit,currstate):
    heapq.heappush(statestovisit,(manhattanprioritizer(currstate),currstate))
    return statestovisit

#[[int]] -> [[int]]
def solvepuzzleniol(board):
    statestovisit = []
    statestovisit = addtovisit(statestovisit,board)
    visited = set()
    while len(statestovisit) > 0:
        print("Num states visisted: %i" % (len(visited)))
        state = heapq.heappop(statestovisit)[1]
        if isgoalstate(state):
            printboard(state)
            return True
        else:
            printboard(state)
            tupedstate = tup(state)
            if tupedstate not in visited:
                visited.add(tupedstate)
                zero = findzero(state)
                col,row = zero[0],zero[1]
                map(lambda x: addtovisit(statestovisit,x),generatesuccessors(row,col,state))
    return False

board3 = [[1,2,5],[3,7,4],[0,6,8]]
board2 = [[1,4,2],[3,5,8],[6,7,0]]
board1 = [[1,0,2],[3,4,5],[6,7,8]]
board = [[1,2,0],[3,4,5],[6,7,8]]
solvepuzzleniol(board3)
