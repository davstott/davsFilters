import redis, sys, math

#for now, it's multiply for ngrams within words and addition for words in input
#this needs checking against how stats works
r = redis.Redis("localhost")

def checkProb(word, gramsize):
  global r
  if (len(word) < 2):
    return float(0)
  prob = float(0)
  for i in range(0,len(word)):
    # we know about 2, 3 and 4, but 2 isn't giving much contrast
    for j in gramsize:
      if (i + j <= len(word)):
        p = r.get(word[i:i+j])
        if p is not None:
          p = int(p) / float(r.get("totalGrams" + str(j)))
        else:
          p = 0
        if (p > 0):
          prob = prob + math.log(float(p), 10)
  if (prob == 1):
    return float(0)
  else:  
    return prob   

def getProb(line, gramsize):
  totalProb = float(0)
  for word in line.split(" "):
    thisProb = checkProb(word.lower(), gramsize)
    totalProb = totalProb + thisProb
  return totalProb

if __name__ == "__main__":
  stdInTotal = float(0)
  for line in sys.stdin:
    stdInTotal = stdInTotal + getProb(line, (3,))
  print "total: " + str(stdInTotal) + "\n"

