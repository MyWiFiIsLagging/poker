while True:
    cisla = [0, 1]
    n = int(input("n: "))
    for i in range(n):
        cisla[i%2-1] = cisla[0] + cisla[1]
    print(max(cisla))