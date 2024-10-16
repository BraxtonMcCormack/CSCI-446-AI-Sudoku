# Search, Constraint Satisfaction, and Sudoku

## Authors: 
Benjamin Heinze, Braxton McCormack  
Email: ben.c.heinze@gmail.com, braxton.j.mccormack@gmail.com  
Group #8

## Project Overview:
This project explores various search algorithms to solve Sudoku puzzles of differing difficulty levels (Easy, Medium, Hard, and Evil). We implemented and compared the performance of the following algorithms: Simple Backtracking, Backtracking with Forward Checking, Backtracking with Arc Consistency, Simulated Annealing, and Genetic Algorithm. The key objective was to evaluate the number of decisions made and the uniqueness of the solutions provided by each algorithm.

## Key Components:
- **Simple Backtracking**: A brute-force approach that fills cells with values, backtracking when it hits an invalid assignment.
- **Backtracking with Forward Checking**: An enhancement of Simple Backtracking, maintaining lists of potential values for unfilled cells and updating them with each assignment.
- **Backtracking with Arc Consistency**: Further refinement, checking the consistency of the domain of possible values before proceeding with backtracking.
- **Simulated Annealing**: A local search algorithm that minimizes conflicts iteratively, using randomness to improve solutions over time.
- **Genetic Algorithm**: Evolves two randomly initialized boards over several generations by crossover and mutation, aiming to reduce inconsistencies.

## Problem Statement:
The project aims to test the efficiency and effectiveness of these five algorithms in solving Sudoku, a constraint satisfaction problem (CSP). We expected the backtracking-based algorithms to guarantee a solution but differ in their decision-making efficiency, while local search algorithms like Simulated Annealing and Genetic Algorithm would take longer and may not always find a solution, but offer more unique results.

## Hypothesis:
Backtracking algorithms were expected to solve puzzles with fewer decisions, while Simulated Annealing and Genetic Algorithm were expected to produce more varied solutions. We hypothesized that the performance of each algorithm would correlate with the puzzle's difficulty level, with harder puzzles taking more time and decisions to solve.

## Methodology:
- **Backtracking Algorithms**: Measured by the number of decisions made (input attempts for cells).
- **Local Search Algorithms**: Measured by the number of conflicts (inconsistencies) at each cycle and how fitness values converge to zero (a solved board).
- We recorded results for each puzzle in CSV files, capturing the decision count and fitness values to track the progress of each algorithm towards solving the puzzle.

## Key Results:
- **Simple Backtracking**: Solved all puzzles but showed a high variance in the number of decisions depending on the puzzle's difficulty. Average decisions ranged from 635 (Easy) to over 12,000 (Hard).
- **Backtracking with Forward Checking**: Reduced decision count compared to Simple Backtracking by maintaining updated lists of potential values.
- **Backtracking with Arc Consistency**: Further reduced decision counts but was less efficient than Forward Checking.
- **Simulated Annealing**: Consistent in reducing conflicts across all difficulty levels but failed to solve puzzles within 10,000 cycles. The fitness values converged close to zero but never reached a perfect solution.
- **Genetic Algorithm**: Showed a similar performance to Simulated Annealing, producing solutions with varying degrees of fitness. Convergence was slower, and solutions were luck-based, especially for more complex puzzles.

## Conclusion:
- **Backtracking Algorithms**: Found solutions consistently with varying efficiency depending on the implementation (Forward Checking and Arc Consistency improving decision counts).
- **Simulated Annealing and Genetic Algorithm**: These algorithms produced more unique solutions but required significantly more cycles and often failed to find a complete solution within a practical timeframe.
- **Summary**: For guaranteed solutions, backtracking methods are superior, though local search methods offer potential for unique, non-deterministic solutions in longer runs.

## References:
- Levine, John. Constraint Satisfaction: The AC-3 Algorithm. YouTube, 14 Dec. 2019, [Link](https://youtu.be/4cCS8rrYT14?si=MHB8XkCbzfEuxBrw). Accessed 1 Sept. 2023.
- Russell, Stuart J., et al. “Chapter 4 Search in Complex Environments, Chapter 6 Constraint Satisfaction Problems.” Artificial Intelligence: A Modern Approach, Fourth Edition, Pearson Education, Harlow, 2022.
