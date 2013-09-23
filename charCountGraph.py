import fileinput, sys, matplotlib.pyplot as p

def newBlank():
  found = []
  for i in range(0,256):
    found.append(0)
  return found

def plot(thisFound, lastFileName, total):
  def norm(x):
    global total
    return float(x) / float(total)

  thisFound = map(norm, thisFound)
  p.plot(range(0, 256), thisFound, label=lastFileName)


#if len(sys.argv) == 2:
#  filein = open(sys.argv[1], "r")
#else:
#  filein = sys.stdin

lastFileName = ""
thisFound = newBlank()
total = 0

for thisLine in fileinput.input():
  #c = filein.read(1)
  if lastFileName == "":
    lastFileName = fileinput.filename()

  if lastFileName != "" and lastFileName != fileinput.filename():
    plot(thisFound, lastFileName, total)
    lastFileName = fileinput.filename()
    thisFound = newBlank()
    total = 0

  for c in thisLine:
    thisFound[ord(c)] += 1
    total += 1

plot(thisFound, lastFileName, total)

p.xlabel('byte values')
p.ylabel('relative frequency')
p.legend()
p.show()
