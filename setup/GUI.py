from agent.Agent import Agent
class GUI:
    def __init__(self, strat, board):
        self.agent = Agent(strat)
        self.strat = strat
        self.board = board

    def solve(self):
        # self.agent.setStrategy(self.strat)
        # self.agent.solve(self.board)
        self.agent.solve()