import fileinput
from datetime import datetime
import re
filelist = "/var/tmp/googlebooks-eng-all-1gram-20090715-7.csv"
filelist = "/var/tmp/smalllist.csv"
lastword = ""
currentcount = 0
maxbatchsize = 10
wordcount = 0
starttime = datetime.now()
print starttime

for thisLine in fileinput.input(filelist):
    bits = thisLine.split("\t")
    # only look at words used 'recently'
    if (bits[1] > 1980):
        # only look at words containing only letters
        if (re.search(bits[0], "[^a-zA-Z]") == None):
            # we've found a word. is it the same as the last word?
            if (bits[0] == lastword):
                currentcount = currentcount + int(bits[2])
            else:
                print (lastword + " was found " + str(currentcount) + " times \n")
                lastword = bits[0]
                currentcount = int(bits[2])
                wordcount = wordcount + 1
                if (wordcount % maxbatchsize):
                    #report time
                    print ("processed " + str(wordcount) + " words in " + str((datetime.now() - starttime).total_seconds()) + " seconds = " + str(wordcount / ((datetime.now() - starttime).total_seconds())) + " words per second")
                      
