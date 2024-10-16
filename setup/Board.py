import numpy as np

class Board:    
    def __init__(self, filename):
        self.filename = filename
        #creates pathname with filename
        path = "puzzlesCSV/"+filename+".csv"
        #generates 2d array from data, converts data to ints; 0's represent unknown cells (formerly question marks)
        try:
            with open(path, 'r', encoding='utf-8-sig') as f:
                arr = np.genfromtxt(f, dtype=int, delimiter=',')
            arr[arr == (-1)] = 0  #converts -1's to 0s for easier view# ing
            #assigns object var                                     
            self.board = arr
            print("INITIAL ARRAY:")
            print(arr)
            print("-----------------------------")
            #creates 9x9x9 array, array[row][col][index]
            self.domain_board = np.full((9,9,9), np.arange(1,10))
            #np boolean array for if that cell is prefilled
            self.immutableCellArr = self.board > 0 #any elem > 0 sets that cell to true

        except FileNotFoundError:
            print("Error: "+path+" not found.")
            exit()

    def getBoard(self):
        return self.board

    #array of every cell's domains 
    def getDomainArr(self):
        return self.domain_board

    def getFilename(self):
        return self.filename
    def getImmutableCellArr(self):
        return self.immutableCellArr
    