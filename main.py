from collections import defaultdict
from setup.Board import *
#from setup.GUI import GUI
from agent.Agent import Agent
import csv

def __main__():
    strats = ['BT','BTFC', 'BTAC', 'SA', 'GA']
    difficulties = ['Easy', 'Med', 'Hard','Evil']

    for diff in difficulties:
        for i in range(1,6):
            name = diff+"-P"+str(i)
            b = Board(name)
            a = Agent("BTFC",b,0)
            a.solve()



if __name__ == '__main__':          #safety feature I guess? idk why people do this but it looks cool
    # run_and_save_solutions()
    __main__()