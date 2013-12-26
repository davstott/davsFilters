import redis, random
r = redis.Redis("localhost")

lName = "2gram:cumulative"
max2 = r.zrange(lName, r.zcard(lName) - 1, r.zcard(lName), withscores = True)[0][1]

lName = "3gram:cumulative"
max3 = r.zrange(lName, r.zcard(lName) - 1, r.zcard(lName), withscores = True)[0][1]

for i in range(10):
  word = ""
  for j in range(3):
   word = word + r.zrangebyscore(lName, "(" + str(random.randint(1, max3)), "+inf", 0, 1)[0]
  print word
