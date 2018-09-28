import matplotlib.pyplot as plt
import random
import time
import itertools
import math
from namedlist import namedlist


# Based on Peter Norvig's IPython Notebook on the TSP

City = namedlist('City', 'x y v')
# c1 = City(4,0)
# c2 = City(0,3)


def distance(A, B):
    return math.hypot(A.x - B.x, A.y - B.y)


def try_all_tours(cities):
    "Generate and test all possible tours of the cities and choose the shortest tour."
    tours = alltours(cities)
    best = min(tours, key=tour_length)
    print(best)
    return best


def alltours(cities):
    # Return a list of tours (a list of lists), each tour a permutation of cities, but
    # each one starting with the same city.
    start = next(iter(cities)) # cities is a set, sets don't support indexing
    tours = [[start] + list(rest)
            for rest in itertools.permutations(cities - {start})]
    return tours


def tour_length(tour):
    # The total of distances between each pair of consecutive cities in the tour.
    return sum(distance(tour[i], tour[i-1])
               for i in range(len(tour)))


def make_cities(n, width=1000, height=1000):
    # Make a set of n cities, each with random coordinates within a rectangle (width x height).

    random.seed(1113) # the current system time is used as a seed
    # note: if we use the same seed, we get the same set of cities

    return [City(random.randrange(width), random.randrange(height), False)
                     for c in range(n)]


def plot_tour(tour):
    # Plot the cities as circles and the tour as lines between them.
    points = list(tour) + [tour[0]]
    plt.plot([p.x for p in points], [p.y for p in points], 'bo-')
    plt.axis('scaled') # equal increments of x and y have the same length
    plt.axis('off')
    plt.show()


def plot_tsp(algorithm, cities):
    # Apply a TSP algorithm to cities, print the time it took, and plot the resulting tour.
    t0 = time.clock()
    tour = algorithm(cities)
    t1 = time.clock()
    print("{} city tour with length {:.1f} in {:.3f} secs for {}"
          .format(len(tour), tour_length(tour), t1 - t0, algorithm.__name__))
    print("Start plotting ...")
    plot_tour(tour)

# Our custom algorithms for pathfinding
def just_loop_through_them(cities):
    tour = []
    for c in cities:
        tour.append(c)
    return tour

def nearest_neighbour(cities):
    tour = []
    tour.append(cities[0])
    cities[0].v = True
    for c in cities:
        lowest = False
        for comparison in cities:
            if comparison.v:
                continue
            if lowest is False or distance(c, lowest) > distance(c, comparison):
                lowest = comparison
        if lowest is False:
            tour.append(cities[0])
            break
        tour.append(lowest)
        lowest.v = True
    return tour

def remove_crossings(cities):
    tour = nearest_neighbour(cities)
    crossings_found = True
    while crossings_found:
        crossings_found = False
        print("Got here")
        for index_a in range(len(tour)-1):
            a1 = tour[index_a]
            a2 = tour[index_a+1]
            for index_b in range(len(tour)-1):
                b1 = tour[index_b]
                b2 = tour[index_b+1]
                if find_intersection(a1.x, a1.y, a2.x, a2.y, b1.x, b1.y, b2.x, b2.y):
                    print(a1, a2, b1, b2)
                    tour[index_a+1] = b2
                    tour[index_b+1] = a2
                    crossings_found = True
                    break

    return tour

def find_intersection(
        x1, y1,
        x2, y2,
        x3, y3,
        x4, y4):
    x12 = x1 - x2
    x34 = x3 - x4
    y12 = y1 - y2
    y34 = y3 - y4

    interception = x12 * y34 - y12 * x34
    if abs(interception) == 0:
        return False

    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4

    x = (a * x34 - b * x12) / interception
    y = (a * y34 - b * y12) / interception

    if x >= x1 and x <= x2 and x >= x3 and x <= x4:
        return x, y
    return False

cities = make_cities(10)

plot_tsp(remove_crossings, cities)
#plot_tsp(nearest_neighbour, cities)

