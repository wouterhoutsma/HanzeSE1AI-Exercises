from itertools import permutations

options = [0, 1, 2, 3, 4, 5, 6, 7, 8]

list = []
for option in permutations(options):
    list.append(option)
print(len(list))