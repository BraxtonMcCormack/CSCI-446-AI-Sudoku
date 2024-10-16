import pandas as pd
import matplotlib.pyplot as plt


def main(graph):
    # Set the figure size
    plt.rcParams["figure.figsize"] = [11.00, 5]
    plt.rcParams["figure.autolayout"] = True

    # Make a list of columns
    columns = ['n_decisions', 'cost']  #

    # Read a CSV file
    df = pd.read_csv(graph, usecols=columns)
    name = graph[:-4]
    # Plot the lines
    df.plot(linewidth=1)
    plt.xlabel("Cycles")
    plt.ylabel("Total Inconsistencies")
    plt.title("Number of Inconsistencies over Ten Thousands of Generations for " + graph)
    plt.grid()
    # plt.xticks(range(0, max(n_decisions) + 1, 5))
    # plt.ylim(min(cost), max(cost) + 5)  # Adjust the y-axis limits as needed
    name = graph[:-4]
    plt.ylim(0,150)
    plt.savefig("graphs/"+name + ".png", dpi=160)
    plt.show()


#main("GA_Easy-P1_output.csv")

diff = ["Easy","Med","Hard","Evil"]
for d in diff:
  for i in range(1,6):
      name = "BTFC_"+d+"-P"+str(i)+"_output.csv"
      main(name)
