import re
import sys
from collections import deque

def similarity(P, S):
  boundary = '\W+'
  sim = 0.00
  res = 0.00
  M = re.split(boundary, P)
  N = re.split(boundary, S)
  for i in M:
    for j in N:
      if i==j:
        sim += 1
      else:
        sim += 0
    res += min(1, sim)
    sim = 0 
  return res/len(M)

def isnovel(P, cache, index):
  for S in cache:
    if similarity(P, S) >= index:
      return 0
  return 1

def main():
  # initialization
  size = int(sys.argv[1])
  index = float(sys.argv[2])
  path = sys.argv[3]
  pathout = sys.argv[4]

  corpus = open(path, 'r')
  output = open(pathout, 'w')
  
  # cache set-up
  P = corpus.readline()
  cache = deque() 
  cache.append(P) 
  output.write(P)
  i = size
  while (i > 0):
    S = corpus.readline()
    if (isnovel(S, cache, index)):
      cache.append(S)
      output.write(S)
      i -= 1
    P = S

   # continue 
  for S in corpus:
    if (isnovel(S, cache, index)):
      cache.popleft()
      cache.append(S)
      output.write(S)   
  
  corpus.close()
  output.close()  

if __name__ == "__main__":
  main()    
