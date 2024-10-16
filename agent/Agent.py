from strategy.Backtracking_Forward_check import BTFC
from strategy.Backtracking_Arc_consistency import BTAC
import strategy.Local_Search_Genetic_Algorithm
from strategy.Local_Search_simulated_Annealing import SimulatedAnnealing
from strategy.Simple_Backtrack import SBT

# class Agent:
#     def __init__(self,solver,n_decisions):
#         self.solver = solver
#         self.n_decisions = n_decisions

#     '''chooses which strategy algorithm to use'''
#     def setStrategy(self, strat):
#         self.solver = strat

#     def solve(self, board):
#         pass

#         '''returns number of decisions made by the algorithm'''
#     def getSteps(self):
#         return self.n_decisions


class Agent:
    def __init__(self,solver,board ,n_decisions):
        self.n_decisions = n_decisions
        self.board = board
        match solver:
            case 'BT':
                self.solver = strategy.Simple_Backtrack.SBT(self.board)
            case 'BTFC':
                self.solver = BTFC(self.board)
            case 'BTAC':
                self.solver = BTAC(self.board)
            case 'SA':
                self.solver = SimulatedAnnealing(self.board)
            case 'GA':
                self.solver = strategy.Local_Search_Genetic_Algorithm.Local_Search_Genetic_Algorithm(self.board)

            case default:
                print("AGENT DEFAULT CASE REACHED")


    '''chooses which strategy algorithm to use'''
    def setStrategy(self, strat):
        self.solver = strat

    def solve(self):
        self.solver.solve()


    '''returns number of decisions made by the algorithm'''
    def getSteps(self):
        return self.n_decisions
