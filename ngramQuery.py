import redis, sys

#for now, it's multiply for ngrams within words and addition for words in input
#this needs checking against how stats works
totalProb = float(0)
r = redis.Redis("localhost")

def checkProb(word):
  global r
  if (len(word) < 2):
    return float(0)
  prob = float(1)
  for i in range(0,len(word)):
    # we know about 2, 3 and 4, but 2 isn't giving much contrast
    for j in range(3,4):
      if (i + j <= len(word)):
        p = r.get(word[i:i+j])
        if (p > 0):
          prob = prob * float(p)
  if (prob == 1):
    return float(0)
  else:  
    return prob   

for line in sys.stdin:
  for word in line.split(" "):
    thisProb = checkProb(word)
    print word + " " + str(thisProb) + "\n"
    totalProb = totalProb + thisProb
 
print "total: " + str(thisProb) + "\n"

