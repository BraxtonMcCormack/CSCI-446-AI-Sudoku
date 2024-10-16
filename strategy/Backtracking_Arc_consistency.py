import csv
import numpy as np
import math
from collections import deque

class BTAC:
    def __init__(self, puzzle):
        # Initialize the BTAC (Backtracking with Arc Consistency) Sudoku solver.
        self.puzzle = puzzle.getBoard()  # Get the Sudoku puzzle board
        self.size = puzzle.getBoard().shape[0]  # Size of the puzzle (typically 9x9)
        self.domains = self.initialize_domains()  # Initialize domains for each cell
        self.epochs = 0  # Counter for the number of iterations
        self.fitness = 0  # Fitness score to evaluate the quality of the solution
        self.filename = puzzle.getFilename()

    def initialize_domains(self):
        # Initialize the domains for each cell in the puzzle.
        domains = []
        for _ in range(self.size):
            domain = []
            for _ in range(self.size):
                domain.append(set(range(1, self.size + 1)))  # Initialize with all possible values (1-9 for standard Sudoku)
            domains.append(domain)
        return domains

    def is_valid(self, row, col, num):
        # Check if placing 'num' at the given (row, col) is a valid move.
        for i in range(self.size):
            if (self.puzzle[row, i] == num or
                self.puzzle[i, col] == num or
                self.puzzle[(row // 3) * 3 + i // 3, (col // 3) * 3 + i % 3] == num):
                return False
        return True

    def enforce_arc_consistency(self):
        # Apply Arc Consistency by reducing domains based on initial puzzle values.
        queue = deque()

        for row in range(self.size):
            for col in range(self.size):
                if self.puzzle[row, col] != 0:
                    queue.append((row, col))

        while queue:
            row, col = queue.popleft()
            num = self.puzzle[row, col]

            for i in range(self.size):
                if col != i and num in self.domains[row][i]:
                    self.domains[row][i].remove(num)
                    if len(self.domains[row][i]) == 1:
                        queue.append((row, i))

                if row != i and num in self.domains[i][col]:
                    self.domains[i][col].remove(num)
                    if len(self.domains[i][col]) == 1:
                        queue.append((i, col))

                box_row, box_col = (row // 3) * 3 + i // 3, (col // 3) * 3 + i % 3
                if (row != box_row or col != box_col) and num in self.domains[box_row][box_col]:
                    self.domains[box_row][box_col].remove(num)
                    if len(self.domains[box_row][box_col]) == 1:
                        queue.append((box_row, box_col))

    def solve(self):
        # Solve the Sudoku puzzle using backtracking.
        with open(f"BTAC_Outputs/BTAC_{self.filename}_output.csv", mode='w', newline='') as csv_file:
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
        # Recursive backtracking algorithm to solve the Sudoku puzzle.
        self.fitness = self.sudoku_cost(self.puzzle)  # Calculate the initial fitness score

        empty_cell = self.find_empty()  # Find the first empty cell in the puzzle
        if not empty_cell:
            return True  # All cells are filled, solution found

        row, col = empty_cell
        for num in self.domains[row][col]:
            if self.is_valid(row, col, num):
                self.puzzle[row, col] = num
                with open(f"BTAC_Outputs/BTAC_{self.filename}_output.csv", mode='a', newline='') as csv_file:
                    csv_writer = csv.writer(csv_file)
                    # csv_writer.writerow(["n_decisions", "cost"])  # Write header row
                    csv_writer.writerow([self.epochs, self.sudoku_cost(self.puzzle)])
                # print(self.sudoku_cost(self.puzzle)) 
                self.epochs += 1

                if self.backtracking():
                    return True

                # If the current placement doesn't lead to a solution, backtrack
                self.puzzle[row, col] = 0

        return False

    def find_empty(self):
        # Find the first empty cell in the puzzle.
        for i in range(self.size):
            for j in range(self.size):
                if self.puzzle[i, j] == 0:
                    return (i, j)
        return None
    
    def sudoku_cost(self, board):
        # Calculate the cost of the Sudoku board. The cost is the sum of conflicts in the rows, columns, and subcells. Lower is better.
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
