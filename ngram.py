import fileinput, time, re, redis, sys

if (len(sys.argv) != 2):
  print "usage " + sys.argv[0] + " filename"
  exit(1)

filelist = sys.argv[1]
#filelist = "/var/tmp/smalllist.csv"
#filelist = "/var/tmp/verysmalllist.csv"
lastword = ""
currentcount = 0
maxbatchsize = 1000
wordcount = 0
gramcount = {}
myGrams = dict()
starttime = time.time()
print starttime

r = redis.Redis("localhost")

# todo: work out how to normalise for word frequency in a single pass
# it's easy if you store the grams by word then do another loop to assemble them
# todo: try to work out if markov chain maths applies 
# or the cheaty way of normalising Bayes at the end rather than as you go
# todo: work out how to use the frequency of a word appearing after another word
# it's a step in the wrong direction for language detection, but would be useful in the model for word unshredding

def addNgram(thisGram):
  global gramcount, myGrams
  thisGram = thisGram.lower()
  if (len(thisGram) in gramcount):
    gramcount[len(thisGram)] = gramcount[len(thisGram)] + 1
  else:
    gramcount[len(thisGram)] = 1

  if (thisGram not in myGrams):
    myGrams[thisGram] = [1,0]
  else:
    myGrams[thisGram][0] = myGrams[thisGram][0] + 1


def ngramify(word):
  if (len(word) < 2):
    return None
  for i in range(0, len(word)):
    for j in range(2,4):    
      if (i + j <= len(word)):
        addNgram(word[i:i+j])

# I bet redis is fast enough to use directly instead of the myGrams dict

for thisLine in fileinput.input(filelist):
  bits = thisLine.split("\t")
  # only look at words used 'recently'
  if (bits[1] > 1980):
    # only look at words containing only letters
    if (bits[0].isalpha()):
      # we've found a word. is it the same as the last word?
      if (bits[0] == lastword):
        currentcount = currentcount + int(bits[2])
      else:
        print (lastword + " was found " + str(currentcount) + " times \n")
        # do something with the frequency stats
        ngramify(lastword)
        lastword = bits[0]
        currentcount = int(bits[2])
        wordcount = wordcount + 1
        if (wordcount % maxbatchsize == 0):
          #report time
          print ("processed " + str(wordcount) + " words in " + str(time.time() - starttime) + " seconds = " + str(wordcount / (time.time() - starttime)) + " words per second")

# this seems like a job for map(fn, thisGram)
for thisGram in myGrams:
  r.incr(thisGram, myGrams[thisGram][0])
  #myGrams[thisGram][1] = myGrams[thisGram][0] / float(gramcount[len(thisGram)])
  # todo: implement incrbyfloat in pyredis
  #if (r.exists(thisGram)):
  #  r.set(thisGram, float(r.get(thisGram)) + myGrams[thisGram][1])
  #else:
  #  r.set(thisGram, myGrams[thisGram][1])

#print myGrams
print ("total grams: " + str(gramcount))
print ("total words: " + str(wordcount))
#gets set to 0 beforehand if it's not defiend
for thisLen in gramcount:
  r.incr("totalGrams" + str(thisLen), gramcount[thisLen])

r.incr("totalWords", wordcount)
