import re

def readFile(filename):
    #filename = 'data1.csv'
    
    
    lines = open(filename).read().split("\n")
    
    d = []
    st = []
    s = []
    
    for line in lines:
        if line.strip():
            line = line.rstrip()
            if line.startswith('nBakeryProducts'):
                nBakeryProducts = int(re.split('\s+', line)[1])
            elif line.startswith('Timehorizon'):
                Timehorizon = int(re.split('\s+', line)[1])
            elif line.startswith('l'):
                l = re.split('\s+', line)[1:]
                l = list(map(int, l))
            elif line.startswith('h'):
                h = re.split('\s+', line)[1:]
                h = list(map(float, h))
                h = list(map(int, h))
            elif line.startswith('K'):
                K = re.split('\s+', line)[1:]
                K = list(map(int, K))
            elif line.startswith('a'):
                a = re.split('\s+', line)[1:]
                a = list(map(int, a))
            elif line.startswith('d'):
                temp = re.split('\s+', line)[1:]
                temp = list(map(float, temp))
                temp = list(map(int, temp))
                d.append(temp)
            elif line.startswith('st'):
                temp = re.split('\s+', line)[1:]
                temp = list(map(float, temp))
                temp = list(map(int, temp))
                st.append(temp)
            elif line.startswith('s'):
                temp = re.split('\s+', line)[1:]
                temp = list(map(float, temp))
                temp = list(map(int, temp))
                s.append(temp)
               

    return nBakeryProducts, Timehorizon, l, h, K, a, d, s, st

readFile('lotData1.txt')