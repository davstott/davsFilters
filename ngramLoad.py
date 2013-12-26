import redis,string

r = redis.Redis("localhost")
i = open("ngramDump.txt", "r")
#i = open("short", "r")

cumulative = {}
cumulative[2] = 0.
cumulative[3] = 0.

for thisLine in i:
  bits = thisLine.split("|")
  bits[1] = string.strip(bits[1])
  r.set(bits[0], bits[1])
  if len(bits[0]) < 4:
    r.rpush(str(len(bits[0])) + "gram:list", bits[0])
    cumulative[len(bits[0])] += float(bits[1])
    # this old verison of pyredis has the zadd arguments swapped round accidentally
    r.zadd(str(len(bits[0])) + "gram:cumulative", bits[0], cumulative[len(bits[0])])
