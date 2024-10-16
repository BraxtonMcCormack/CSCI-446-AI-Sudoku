import pandas as pd
import matplotlib.pyplot as plt


def main(graph):
    # Set the figure size
    plt.rcParams["figure.figsize"] = [11.00, 5]
    plt.rcParams["figure.autolayout"] = True

    # Make a list of columns
    columns = ['p1Fitness', 'p2Fitness', 'averageTotalFitness']  #

    # Read a CSV file
    df = pd.read_csv(graph, usecols=columns)
    name = graph[:-4]
    # Plot the lines
    df.plot(linewidth=1)
    plt.xlabel("Cycles")
    plt.ylabel("Total Inconsistencies")
    plt.title("Number of Inconsistencies over Ten Thousands of Generations for " + graph)
    plt.grid()
    plt.yticks([0,10,20,30,40,60,80,100,120])
    plt.xticks([0, 5000, 10000, 15000, 20000,25000,30000])
    name = graph[:-4]
    plt.ylim(0,100)
    plt.savefig("graphs/"+name + ".png", dpi=160)
    plt.show()


#main("GA_Easy-P1_output.csv")

diff = ["Easy","Med","Hard","Evil"]
for d in diff:
  for i in range(1,6):
      name = "GA_"+d+"-P"+str(i)+"_output.csv"
      main(name)
