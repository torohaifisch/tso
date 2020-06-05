import random
from random import randint
from joblib import dump, load
import math

# Swap positions of 2 values
def swap(path):
	sequence = path.copy()
	idx = range(len(sequence))
	i, j = random.sample(idx, 2)
	temp = sequence[i]
	sequence[i]=sequence[j]
	sequence[j]=temp
	return sequence

# Left Shift
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

def symmetry(path):
	n = len(path)
	temp1 = path.copy()
	temp2 = path.copy()
	b  = math.ceil(1+(n-2)*random.random())
	R2 = math.ceil(1+(b-2)*random.random())
	R3 = math.ceil(1+(n-b-1)*random.random())
	a  = min(R2,R3)
	if b + 1 <=n and b + a <=n :
		temp1[b+1:b+a] = temp2[b-1:b-a:-1]
		temp1[b-1:b-a:-1] = temp2[b+1:b+a]
	return temp1


# 2-opt algorithm (local search)
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

# Oposition of initial population
def initObs(path,n):
	lista=[]
	sol=[]
	for j in path:
		for i in range(len(inputMatrix)):
			lista.append(len(inputMatrix)-1 - j[0][i])
			
		sol.append((lista,calculateDistance(lista)))
		lista=[]

	join = path+sol
	join.sort(key=lambda tup: tup[1])
	join = join[:n]
	return (join)

# Opossition of solution
def obs(path):
	lista=[]
	for i in range(len(inputMatrix)):
		lista.append(len(inputMatrix)-1 - path[i])
	return lista

def createSeeds(tree):
	seeds=[]
	s = swap(tree)
	seeds.append((s, calculateDistance(s)))
	s = shift(tree)
	seeds.append((s, calculateDistance(s)))
	s = symmetry(tree)
	seeds.append((s, calculateDistance(s)))

	if storeData:
		for i in seeds:
			dataList.append(i)

	return seeds


# Distance in matrix
def calculateDistance(path):
        index = path[0]
        distance = 0
        for nextIndex in path[1:]:
                distance += distanceMatrix[index][nextIndex]
                index = nextIndex
        return distance+distanceMatrix[path[-1]][path[0]]

# euclidean distance
def distance(city1: dict, city2: dict):
    return math.sqrt((city1['x'] - city2['x']) ** 2 + (city1['y'] - city2['y']) ** 2)

#define cost matrix from instance of TSP
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

# recommended 0.5
ST=0.7

fes = N

trees=[]
distances=[]
storeData = False
dataList=[]

# Init population

iPath = list(range(0,maxCities))

for i in range(N):
    random.shuffle(iPath)
    trees.append((iPath,calculateDistance(iPath)))

# Get best initial solutions by exploring opposed space
trees = initObs(trees,N)

#Get initial best
best = trees[0]
cfr=load("./svm/filename.joblib")
# discrete tree seed mh
while fes <maxFes:
	count=0
	for i in trees:
		nTree = randint(0,N-1)
		while (nTree == i):
			nTree = randint(0,N-1)
		kTree=trees[nTree]
		ns = 6

		if cfr.predict([i[0]])>ST:
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
# local search
rbest = two_opt(best[0])
print(rbest)


# store data for svm training
if storeData:
		f= open("data.txt","a")
		for i in dataList:
			f.write(str(rbest[1]/i[1]))
			for j in i[0]: 
				f.write(" "+str(j))
			f.write("\n")
		f.close()
