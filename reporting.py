import matplotlib.pyplot as plt

def reporting(history, options):
    print("Reporting")
    iterations = list(history.keys())
    tree_populations = [history[i]["Tree_population"] for i in iterations]
    rock_populations = [history[i]["Rock_population"] for i in iterations]
    fire_populations = [history[i]["Fire_population"] for i in iterations]

    # Create plot
    plt.figure(figsize=(10, 6))
    plt.plot(iterations, tree_populations, label='Tree Population')
    plt.plot(iterations, rock_populations, label='Rock Population')
    plt.plot(iterations, fire_populations, label='Fire Population')

    # Add details
    plt.xlabel('Iterations')
    plt.ylabel('Population')
    plt.title('Population over Iterations')
    plt.legend()

    # Show plot
    plt.show()
