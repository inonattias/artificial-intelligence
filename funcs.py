from utils import distance

inputFolder = "Input/tsp15_xy.txt"
rows=[]
f = open(inputFolder,"r")
for line in f:
    rows.append(line.split())
    # print(line)

print(rows[1][0])
print(rows[1])
#a=distance(str(rows[1]) ,str(rows[2])) //need to convert to the right type of distance
print(a)
