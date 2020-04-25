import random
from random import randint 
import math

def swap(path):
	sequence = path.copy()
	idx = range(len(sequence))
	i, j = random.sample(idx, 2)
	temp = sequence[i]
	sequence[i]=sequence[j]
	sequence[j]=temp
	return sequence

def shift(path):
	l = path.copy()
	idx = range(len(l))
	x, y = random.sample(idx, 2)
	if x<y:
		c = l[x:y]
		c.append(c.pop(0))
		l[x:y] = c
	else:
		c = l[y:x]
		c.append(c.pop(0))
		l[y:x] = c
	return l
#def mirror:

def two_opt(route):
	best = route
	improved = True
	while improved:
		improved = False
		for i in range(1, len(route)-2):
			for j in range(i+1, len(route)):
				if j-i == 1: continue # changes nothing, skip then
				new_route = route[:]
				new_route[i:j] = route[j-1:i-1:-1] # this is the 2woptSwap
				if (calculateDistance(new_route) < calculateDistance(best)):
					best = new_route
					improved = True
		route = best
	return best, calculateDistance(best)


def initObs(path):
	lista=[]
	sol=[]
	for j in path:
		for i in range(len(inputMatrix)):
			lista.append(len(inputMatrix)-1 - j[0][i])
			
		sol.append((lista,calculateDistance(lista)))

	join = path+sol
	join.sort(key=lambda tup: tup[1])
	join = join[:]
	return (join)


def obs(path):
	lista=[]
	for i in range(len(inputMatrix)):
		lista.append(len(inputMatrix)-1 - path[i])
	return lista

def createSeeds(Tree):
	seeds=[]
	tempT=Tree.copy()
	s = swap(tempT)
	seeds.append((s, calculateDistance(s)))
	tempT=Tree.copy()
	s = shift(tempT)
	seeds.append((s, calculateDistance(s)))
	tempT=Tree.copy()
	s = obs(tempT)
	seeds.append((s, calculateDistance(s)))
	return seeds

def calculateDistance(path):
        index = path[0]
        distance = 0
        for nextIndex in path[1:]:
                distance += distanceMatrix[index][nextIndex]
                index = nextIndex
        return distance+distanceMatrix[path[-1]][path[0]]
def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

def cMA():
        cities = []
        points = []
        with open('./att48.txt') as f:
                for line in f.readlines():
                        city = line.split(' ')
                        cities.append(dict(index=int(city[0]), x=int(city[1]), y=int(city[2])))
                        points.append((int(city[1]), int(city[2])))
        cost_matrix = []
        rank = len(cities)
        for i in range(rank):
                row = []
                for j in range(rank):
                        row.append(distance(cities[i], cities[j]))
                cost_matrix.append(row)
        return cost_matrix


inputMatrix=cMA()
distanceMatrix = inputMatrix
maxCities=len(inputMatrix)

#population
N=maxCities
#iterations
maxFes=200000

ST=0.5

iPath = list(range(0,maxCities))
trees=[]
distances=[]

for i in range(N):
    random.shuffle(iPath)
    trees.append((iPath,calculateDistance(iPath)))
trees = initObs(trees)
fes = N
tempTrees = trees.copy()
tempTrees.sort(key=lambda tup: tup[1])
best = tempTrees[0]
while fes <maxFes:
	count=0
	for i in trees:
		nTree = randint(0,N-1)
		while (nTree == i):
			nTree = randint(0,N-1)
		kTree=trees[nTree]
		ns = 6

		if random.random()<ST:
			seedT1 = createSeeds(best[0])
			seedT2 = createSeeds(kTree[0])
		else:
			seedT1 = createSeeds(kTree[0])
			seedT2 = createSeeds(i[0])

		fes += ns
		totalSeeds = seedT1+seedT2
		totalSeeds.sort(key=lambda tup: tup[1])                       
		bestT=totalSeeds[0]
		if bestT[1]<i[1]:
			trees[count] = bestT
		count+=1
	tempTrees = trees.copy()
	tempTrees.sort(key=lambda tup: tup[1])
	tBest = tempTrees[0]
	if tBest[1]<best[1]:
		best = tBest
print(best)	
print(two_opt(best[0]))
