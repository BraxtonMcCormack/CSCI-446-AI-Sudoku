import random
import numpy as np
def fill(board, immutableArr):
    for row in range(9):
        for col in range(9):
            if not immutableArr[row][col]:
                board[row][col] = random.randint(1,9)
    return board
def colCollisionCount(board, col, value):
    count=-1
    for i in range(9):                 #loops over col
        if board[i][col] == value:
            count+=1                    #counts number of equal values
    return count
def rowCollisionCount(board, row, value):
    count=-1
    for i in range(9):                 #loops over col
        if board[row][i] == value:
            count+=1                    #counts number of equal values
    return count
def gridCollisionCount(board, row,col, value):
    # [1a,1b,1c] GRID DIAGRAM
    # [2a,2b,2c]
    # [3a,3b,3c]
    count = -1
    #first column
    if 0 <= col <= 2:
        #1a
        if 0 <= row <= 2:
            for ro in range(3):
                for co in range(3):
                    if board[ro][co]==value:
                        count +=1
        # 2a
        elif 3 <= row <= 5:
            for ro in range(3,6):
                for co in range(3):
                    if board[ro][co] == value:
                        count += 1
        # 3a
        elif 6 <= row <= 8:
            for ro in range(6,9):
                for co in range(3):
                    if board[ro][co] == value:
                        count += 1
    #second column
    # 1b
    elif 3 <= col <= 5:
        if 0 <= row <= 2:
            for ro in range(0,3):
                for co in range(3,6):
                    if board[ro][co] == value:
                        count += 1
        # 2b
        elif 3 <= row <= 5:
            for ro in range(3,6):
                for co in range(3,6):
                    if board[ro][co] == value:
                        count += 1
        # 3b
        elif 6 <= row <= 8:
            for ro in range(6,9):
                for co in range(3,6):
                    if board[ro][co] == value:
                        count += 1
    #third column
    # 1c
    elif 6 <= col <= 8:
        if 0 <= row <= 2:
            for ro in range(0,3):
                for co in range(6,9):
                    if board[ro][co] == value:
                        count += 1
        # 2c
        elif 3 <= row <= 5:
            for ro in range(3,6):
                for co in range(6,9):
                    if board[ro][co] == value:
                        count += 1
        # 3c
        elif 6 <= row <= 8:
            for ro in range(6,9):
                for co in range(6,9):
                    if board[ro][co] == value:
                        count += 1
    return count
def mutate(board, immutableArray):
    #tunable parameters
    th = random.randint(1,3)    #randomizes threshold
    threshold = th   #threshold that determines whats high chance and whats low chance
    chanceUpperBound = 1000
    highCollisionChance = 900 # out of
    lcc = random.randint(1,10)   #randomiezs low collision chance
    lowCollisionChance = lcc

    for row in range(9):
        for col in range(9):
            if immutableArray[row][col]:
                pass
            else:
                collisions = (rowCollisionCount(board,row,board[row][col])+
                              colCollisionCount(board,col,board[row][col])+
                              gridCollisionCount(board,row,col,board[row][col]))
                probability = random.randint(1,chanceUpperBound)
                #if threshold is high then it has a high chance to mututae
                if collisions>threshold:
                    if probability <= highCollisionChance:
                        board[row][col] = random.randint(1,9)
                else:
                    # if probability chose either 24,25 (arbitrary nums), it has a higher chance to mutuate
                    if probability <= lowCollisionChance:
                        board[row][col] = random.randint(1,9)
    return board
def totalFitness(board):
    fitness = 0
    for row in range(9):
        for col in range(9):
            fitness += (colCollisionCount(board,col,board[row][col]) +
                  rowCollisionCount(board,row,board[row][col]) +
                  gridCollisionCount(board,row,col, board[row][col]))
    return fitness
def onePointCrossover(p1, p2):
    child1 = np.copy(p1)
    child2 = np.copy(p2)

    #chooses a random point in the middle of the sudoku puzzle
    rowPoint = random.randint(3,6)
    colPoint = random.randint(0,8)

    #loop until it reaches end of puzzle
    while rowPoint <=8 and colPoint<=9:
        child1[rowPoint][colPoint] = p2[rowPoint][colPoint]
        child2[rowPoint][colPoint] = p1[rowPoint][colPoint]
        colPoint+=1
        if colPoint >=9:
            rowPoint+=1
            colPoint = 0

    #ADD return the 2 lowest collisions between all 4 options
    p1f = totalFitness(p1)
    p2f = totalFitness(p2)
    c1f = totalFitness(child1)
    c2f = totalFitness(child2)

    #sorts the best options
    l = [[p1,p1f], [p2,p2f],[child1,c1f], [child2, c2f]]
    l.sort(key = lambda x:x[1])
    return l[0][0], l[1][0]

class Local_Search_Genetic_Algorithm:
    def __init__(self,board):
        self.filename = board.getFilename()
        self.board = board
        self.immutableCell = board.getImmutableCellArr()
        self.fitnessArr = np.zeros((9,9), dtype = int)
    def solve(self):
        outputName = "GA_Outputs/GA_"+self.filename+"_output.csv"
        file = open(outputName,"w")
        #Gets blank copies of sudoku puzzle
        OG = np.copy(self.board.getBoard())
        p1 = np.copy(OG)
        p2 = np.copy(OG)
        #Loops for lower collision rating, keeps the lowest board
        for i in range(1):
            pTemp = np.copy(OG)
            fill(pTemp, self.immutableCell)
            temp = totalFitness(pTemp)
            cur = totalFitness(p1)
            if temp < cur:
                p1 = pTemp
        fill(p2, self.immutableCell)        #fills p2

        #Tracks Data
        best = p1                           #best board
        bestFitness = totalFitness(best)    #best fitness (least total collisions)
        initialFitnessP1 = bestFitness
        bestFoundAt = 0                     #number of loops it took to get the best value
        average1 = 0                        #p1 sum of totalFitnesses
        average2 = 0                        #p2 sum of totalFitnesses

        nCycles = 30000                      #number of cycles you'd like to loop to
        #loop for however long
        file.write("cycle,p1Fitness,p2Fitness,averageTotalFitness\n")
        for cycle in range(1,nCycles+1):
            #crossover two boards
            p1, p2 = onePointCrossover(p1,p2)
            #mutate both
            p1= mutate(p1,self.immutableCell)
            p2= mutate(p2,self.immutableCell)
            p1Fitness = totalFitness(p1)
            p2Fitness = totalFitness(p2)

            average1 += p1Fitness
            average2 += p1Fitness
            av = (int((average1 / cycle))+int((average2 / cycle))/2)
            #writes data to file
            data = str(cycle)+","+str(p1Fitness)+","+str(p2Fitness)+","+str(av)+"\n"
            file.write(data)

            #records best
            if p1Fitness < bestFitness or p2Fitness < bestFitness:
                if p1Fitness < p2Fitness:
                    best = p1
                    bestFitness = p1Fitness
                else:
                    best = p2
                    bestFitness = p2Fitness
                bestFoundAt = cycle

            #if finished, it stops
            if p1Fitness == 0 or p2Fitness == 0:
                print("solution found:")
                file.write("0,0,0,0\n")
                file.write(np.array2string(p1))
                file.write(np.array2string(p2))
                break

            #gets average number of collisions for the 2 parents

            #print("average1:",average1/cycle)
            #print("average2:", average2 / cycle)

        #printing data when finished looping
        print("best:")
        print(best)
        print("fitness of best:",bestFitness)
        print("found at cycle number :",bestFoundAt)
        #av = ((average1/nCycles)+(average2/nCycles))/2
        #print("Slope:", (av-initialFitnessP1)/(nCycles-1)) #rise/run (y2-y1)/(x2-x1)
        file.close()#closes file