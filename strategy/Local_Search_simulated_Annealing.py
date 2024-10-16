import csv
import numpy as np
import math
import random

class SimulatedAnnealing:
    def __init__(self, board):  #   Initialize the SimulatedAnnealng class with a Sudoku board.
        self.board = board
        self.sudokuBoard = board.getBoard()
        self.n_decisions = 0
        self.immutableBoard = board.getImmutableCellArr()
        self.filename = "output"  # You may want to set a filename here.
        self.filename = board.getFilename()


    def get_decisions(self):    #Get the number of decisions made during the solving process
        return self.n_decisions
    
    def sudoku_cost(self, board):   #   Calculate the cost of the Sudoku board. The cost of the sum of conflicts in the rows, columns and subcells. lower is better
        n = board.shape[0]
        cost = 0

        for i in range(n):
            row = board[i, :]
            column = board[:, i]
            cost += n - len(np.unique(row))
            cost += n - len(np.unique(column))

        box_size = int(math.sqrt(n))
        for i in range(0, n, box_size):
            for j in range(0, n, box_size):
                box = board[i:i+box_size, j:j+box_size]
                cost += n - len(np.unique(box))
        
        return cost
    
    
    def simulated_annealing(self, initial_board, max_iterations, max_temp, cooling_rate):
        solutionStrength = 0
        current_solution = initial_board.copy()
        current_cost = self.sudoku_cost(current_solution)
        best_solution = current_solution.copy()
        best_cost = current_cost
        temperature = max_temp

        with open(f"SA_Outputs/SA_{self.filename}_output.csv", mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["n_decisions", "cost"])  # Write header row

            for iteration in range(max_iterations):
                self.n_decisions += 1
                if current_cost == 0:
                    break

                i = random.randint(0, 8)
                j = random.randint(0, 8)
                while initial_board[i, j] != 0:
                    i = random.randint(0, 8)
                    j = random.randint(0, 8)

                new_solution = current_solution.copy()
                new_solution[i, j] = random.randint(1, 9)
                new_cost = self.sudoku_cost(new_solution)

                cost_diff = new_cost - current_cost

                if cost_diff <= 0 or random.random() < math.exp(-cost_diff / temperature):
                    current_solution = new_solution
                    current_cost = new_cost

                if current_cost < best_cost:
                    best_solution = current_solution.copy()
                    best_cost = current_cost

                temperature *= cooling_rate

                # Write current decision and cost to the CSV file
                csv_writer.writerow([self.n_decisions, best_cost])

        return best_solution, best_cost

    def solve(self):
        max_iterations = 10000
        max_tempature = 3.0
        cooling_rate = 0.85

        best_solution, best_cost = self.simulated_annealing(self.sudokuBoard, max_iterations, max_tempature, cooling_rate)

        print("Ammount of decisions was:")
        print(self.n_decisions)
        print("The best cost was:")
        print(best_cost)

        for row in best_solution:
            print(" ".join(map(str, row)))

