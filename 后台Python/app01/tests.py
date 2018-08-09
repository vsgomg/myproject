from django.test import TestCase

# Create your tests here.

import redis

conn = redis.Redis(host='192.168.11.128',port=6379)
conn.hset('n1','name','alan')
print(conn.hget('n1','name'))