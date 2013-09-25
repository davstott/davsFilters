import pickle, fileinput, math

with open('pickledCharFreqs', 'r') as f:
  freqs = pickle.load(f)

#inText = 'bonjour la classe, comment ca va'

probs = {}
for lang in freqs:
  probs[lang] = 0.

for thisLine in fileinput.input():
  for lang in freqs:
    total = 0.
    for c in thisLine:
      thisP = freqs[lang].get(c.lower(), 0)
      if thisP != 0:
        total = total + math.log(thisP)
    probs[lang] += total

print probs
