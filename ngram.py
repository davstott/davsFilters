import fileinput, time, re
filelist = "/var/tmp/googlebooks-eng-all-1gram-20090715-7.csv"
#filelist = "/var/tmp/smalllist.csv"
#filelist = "/var/tmp/verysmalllist.csv"
lastword = ""
currentcount = 0
maxbatchsize = 100
wordcount = 0
myGrams = dict()
starttime = time.time()
print starttime

def addNgram(thisGram):
  thisGram = thisGram.lower()
  if (thisGram not in myGrams):
    myGrams[thisGram] = 1
  else:
    myGrams[thisGram] = myGrams[thisGram] + 1


def ngramify(word):
  if (len(word) < 2):
    return None
  for i in range(0, len(word)):
    # 2 grams
    if (i + 2 <= len(word)):
      addNgram(word[i:i+2])
    # 3 grams
    if (i + 3 <= len(word)):
      addNgram(word[i:i+3])
   # 4 grams
    if (i + 4 <= len(word)):
      addNgram(word[i:i+4])


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

print myGrams
