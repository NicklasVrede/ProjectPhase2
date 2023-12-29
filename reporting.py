import matplotlib.pyplot as plt

def reporting(history):
    """
    Displays a plot of the population over iterations.

    Parameters:
    history (Dict[int, Dict[str, int]]): A dictionary of simulation history.
    """
    print("Reporting")
    iterations = list(history.keys())
    rock_populations = [history[i]["Rock_population"] for i in iterations]
    fire_populations = [history[i]["Fire_population"] for i in iterations]
    tree_populations = [history[i]["Tree_population"] for i in iterations]


    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, rock_populations, label='Rock Population', color='grey', lw=2.0)
    plt.plot(iterations, fire_populations, label='Fire Population', color='red', lw=2.0)
    plt.plot(iterations, tree_populations, label='Tree Population', color='green', lw=2.0)

    # Add details
    plt.xlabel('Iterations')
    plt.ylabel('Population')
    plt.title('Population over Iterations')
    plt.legend()

    # Show plot
    plt.show()
