import json

f = open('my_ippool.json')
s = json.load(f)
a = s[1]
b = a['url']
c = str(b)
d = "http://cri.gz.gov.cn" + c
print d
print b
