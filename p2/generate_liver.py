import sys

porcentaje = [90, 80, 70, 60, 50]

lines = []
for p in porcentaje:
	lines.append(354*p/100)

print lines

for p,l in zip(porcentaje, lines):
	f = open('liver/100.data', 'r')
	fnew = open("liver/"+str(p)+".data", 'w')
	count = 1
	while (count <= l):
		fnew.write(f.readline())
		count += 1
	print count


