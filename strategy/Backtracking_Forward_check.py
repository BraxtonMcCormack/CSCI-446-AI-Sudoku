import csv
import numpy as np
import math

# Define a class for Backtracking Sudoku Solver
class BTFC:
    def __init__(self, puzzle):
        # Initialize the Sudoku puzzle board and related attributes
        self.puzzle = puzzle.getBoard()  # Get the puzzle board
        self.size = puzzle.getBoard().shape[0]  # Get the size of the puzzle (typically 9x9)
        self.domains = self.initialize_domains()  # Initialize domains for each cell
        self.epochs = 0  # Count of iterations/epochs during solving
        self.fitness = 0  # Fitness score (errors) of the puzzle
        self.filename = puzzle.getFilename()

    def initialize_domains(self):
        # Initialize domains for each cell as sets of numbers from 1 to the size of the puzzle
        domains = []
        for _ in range(self.size):
            domain = []
            for _ in range(self.size):
                domain.append(set(range(1, self.size + 1)))
            domains.append(domain)
        return domains

    def is_valid(self, row, col, num):
        # Check if a number is valid to place in a given cell
        for i in range(self.size):
            if (
                self.puzzle[row, i] == num
                or self.puzzle[i, col] == num
                or self.puzzle[(row // 3) * 3 + i // 3, (col // 3) * 3 + i % 3] == num
            ):
                return False
        return True

    def forward_checking(self, row, col, num):
        # Update domains by removing num from cells in the same row, column, and subgrid
        for i in range(self.size):
            self.domains[row][i].discard(num)
            self.domains[i][col].discard(num)
            self.domains[(row // 3) * 3 + i // 3][(col // 3) * 3 + i % 3].discard(num)

    def solve(self):
        # Solve the Sudoku puzzle using backtracking
        with open(f"BTFC_Outputs/BTFC_{self.filename}_output.csv", mode='w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(["n_decisions", "cost"])  # Write header row
        if not self.backtracking():
            print("No solution exists.")
        else:
            print("Completed Sudoku:")
            print(self.puzzle)
            print(f"Epochs: {self.epochs}")
            print(f"Fitness Score (errors): {self.fitness}")

    def backtracking(self):

        # with open(f"BTFC_Outputs/BTFC_{self.filename}_output.csv", mode='a', newline='') as csv_file:
        #     csv_writer = csv.writer(csv_file)
            
    
            # Recursive backtracking algorithm to solve the Sudoku puzzle
            # csv_writer.writerow([self.epochs, self.fitness])
        self.csv_write(self.epochs, self.fitness)
        # print(self.epochs)
        self.fitness = self.sudoku_cost(self.puzzle)  # Calculate the fitness (cost) of the current puzzle
        # self.epochs += 1  # Increment the epoch count


        


        empty_cell = self.find_empty()
        if not empty_cell:
            return True  # All cells are filled, solution found

        row, col = empty_cell
        for num in range(1, self.size + 1):
            
            if self.is_valid(row, col, num):
                self.puzzle[row, col] = num  # Place the valid number in the cell
                self.forward_checking(row, col, num)  # Update domains

                self.epochs += 1  # Increment the epoch count

                if self.backtracking():
                    return True  # Recurse to the next cell, return True if a solution is found

                # If the current placement doesn't lead to a solution, backtrack
                self.puzzle[row, col] = 0  # Clear the cell
                # Restore the domains for backtracking
                for i in range(self.size):
                    self.domains[row][i].add(num)
                    self.domains[i][col].add(num)
                    self.domains[(row // 3) * 3 + i // 3][(col // 3) * 3 + i % 3].add(num)

        return False  # No valid number found for the current cell, trigger backtracking

    def find_empty(self):
        # Find the first empty cell (cell with 0) in the puzzle
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i, j] == 0:
                    return (i, j)
        return None  # No empty cell found, puzzle is solved

    def sudoku_cost(self, board):
        # Calculate the cost (fitness) of the Sudoku board
        n = board.shape[0]  # Get the size of the puzzle
        cost = 0

        for i in range(n):
            row = board[i, :]
            column = board[:, i]
            cost += n - len(np.unique(row))  # Increment cost for non-unique numbers in rows
            cost += n - len(np.unique(column))  # Increment cost for non-unique numbers in columns

        box_size = int(math.sqrt(n))
        for i in range(0, n, box_size):
            for j in range(0, n, box_size):
                box = board[i:i + box_size, j:j + box_size]
                cost += n - len(np.unique(box))  # Increment cost for non-unique numbers in subgrids

        return cost  # Lower cost is better, indicating a closer solution to a valid Sudoku


    def csv_write(self, epoch, fitness):
        with open(f"BTFC_Outputs/BTFC_{self.filename}_output.csv", mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([epoch, fitness])  # Write header row