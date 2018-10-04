import itertools
floors = (0, 1, 2, 3, 4)
for (H, K, L, P, R) in list(itertools.permutations(floors)):
    if K != 0 and \
            L != 0 and L != 4 and \
            P > K and \
            abs(R - L) > 1 and \
            abs(L - K) > 1 and \
            H != 4:
        print('H', 'K', 'L', 'P', 'R')
        print(H, K, L, P, R)
        break
