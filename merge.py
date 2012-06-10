work = [9, 1, 3, 6, 2, 4, 5, 8, 7]

debug = 0


def merge(start, count) :

  d = []
  if count == 1 :
    d.append(work[start])
    return d
  
  if debug: input ("start = " + str(start) + " count = " + str(count))
  b = merge(start, int(count / 2))
  c = merge(int(start + count / 2), count - int(count/ 2))
  i = 0
  j = 0
  while (1):
    if i == len(b):
      if debug: print ("appending rest of c to d")
      d.extend(c[j:len(c)])
      break
    if j == len(c):
      if debug: print ("appending rest of b to d")
      d.extend(b[i:len(b)])
      break
    if b[i] < c[j] :
      if debug: print ("appending b[i] to d")
      d.append(b[i])
      i = i + 1
    else :
      if c[j] < b[i] :
        if debug: print ("appending c[j] to d")
        d.append(c[j])
        j = j + 1

  if debug: print (d)
  return d

out = merge(0, len(work))

print (work)
print (out)

