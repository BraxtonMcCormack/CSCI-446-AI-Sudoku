import csv
import random
import numpy as np
import math

class SBT:
    def __init__(self, puzzle):
        # Initialize the Sudoku Backtracking (SBT) solver with a puzzle.
        self.puzzle = puzzle.getBoard()  # Get the puzzle's board as a NumPy array.
        self.size = puzzle.getBoard().shape[0]  # Get the size of the puzzle (e.g., 9 for a 9x9 Sudoku).
        self.domains = self.initialize_domains()  # Initialize possible domain values for each cell.
        self.epochs = 0  # Initialize the number of iterations (backtracking steps).
        self.fitness = 0  # Initialize the fitness score (Sudoku board cost).
        self.filename = puzzle.getFilename()

    def initialize_domains(self):
        # Initialize possible domain values (numbers 1 to size) for each cell in the puzzle.
        domains = []
        for _ in range(self.size):
            domain = []
            for _ in range(self.size):
                domain.append(set(range(1, self.size + 1)))  # Initialize domain as a set from 1 to size.
            domains.append(domain)
        return domains

    def is_valid(self, row, col, num):
        # Check if placing 'num' in the given 'row' and 'col' is a valid move.
        for i in range(self.size):
            if (self.puzzle[row, i] == num or
                self.puzzle[i, col] == num or
                self.puzzle[(row // 3) * 3 + i // 3, (col // 3) * 3 + i % 3] == num):
                return False  # If 'num' is in the same row, column, or subgrid, it's not valid.
        return True

    def solve(self):
        # Solve the Sudoku puzzle using backtracking.
        with open(f"BT_Outputs/BT_{self.filename}_output.csv", mode='w', newline='') as csv_file:
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
        # Perform backtracking to solve the Sudoku puzzle.
        self.fitness = self.sudoku_cost(self.puzzle)  # Calculate the fitness (Sudoku board cost).
        self.csv_write(self.epochs, self.fitness)
        self.epochs += 1  # Increment the number of iterations.

        empty_cell = self.find_empty()
        if not empty_cell:
            return True  # All cells are filled, and the puzzle is solved.

        row, col = empty_cell
        for num in self.domains[row][col]:
            if self.is_valid(row, col, num):
                self.puzzle[row, col] = num  # Place 'num' in the current cell.
                self.epochs += 1  # Increment the number of iterations.

                if self.backtracking():
                    return True  # Recursively try to solve the puzzle.

                # If the current placement doesn't lead to a solution, backtrack.
                self.puzzle[row, col] = 0  # Reset the cell to an empty state.

        return False  # No valid number could be placed in the current cell.

    def find_empty(self):
        # Find the first empty (0) cell in the puzzle and return its coordinates.
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i, j] == 0:
                    return (i, j)
        return None  # If no empty cell is found, return None.

    def sudoku_cost(self, board):
        # Calculate the cost of the Sudoku board. The cost is the sum of conflicts in rows, columns, and subgrids.
        n = board.shape[0]  # Get the size of the board.
        cost = 0

        for i in range(n):
            row = board[i, :]  # Get the current row.
            column = board[:, i]  # Get the current column.
            cost += n - len(np.unique(row))  # Add the number of conflicts in the row.
            cost += n - len(np.unique(column))  # Add the number of conflicts in the column.

        box_size = int(math.sqrt(n))  # Determine the size of subgrids (e.g., 3x3 for a 9x9 Sudoku).
        for i in range(0, n, box_size):
            for j in range(0, n, box_size):
                box = board[i:i+box_size, j:j+box_size]  # Get the current subgrid.
                cost += n - len(np.unique(box))  # Add the number of conflicts in the subgrid.
        
        return cost  # Return the total cost of the board.

    def csv_write(self, epoch, fitness):
        with open(f"BT_Outputs/BT_{self.filename}_output.csv", mode='a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow([epoch, fitness])  # Write header row