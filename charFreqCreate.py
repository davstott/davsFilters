import pickle

freqs = {}
# the data in this file was published by the Oxford Dictionary
with open('englishFreqs', 'r') as f:
  freqs['english'] = {}
  for line in f:
    bits = line.split('\t')
    if len(bits[0]) == 1:
      freqs['english'][bits[0]] = float(bits[1]) / 100

# the data in this file are taken from the Wikipedia character frequencies page
with open('otherFreqs', 'r') as f:
  headings = f.readline()
  headings = headings.split('\t')
  for lang in headings:
    freqs[lang] = {}
  for line in f:
    bits = line.split('\t')
    if len(bits[0]) == 1:
      for i in range(1, len(bits)):
        freqs[headings[i]][bits[0]] = float(bits[i]) / 100

#print freqs
del freqs['Letter']
with open('pickledCharFreqs', 'w') as f:
  pickle.dump(freqs, f)


inText = 'bonjour la classe, comment ca va'

probs = {}

for lang in freqs:
  total = 1.
  for c in inText:
    thisP = freqs[lang].get(c, 0)
    if thisP != 0:
      total = total * thisP
  probs[lang] = thisP

print probs
