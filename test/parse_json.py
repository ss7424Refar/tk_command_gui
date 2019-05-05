import json

f = open('/opt/hello.json', 'r')
content = f.read()
# print(content)

detail = json.loads(content)

c = detail['frames']


dic = {}
for item in c:
    if len(c[item]):
        v = c[item]
        for index in range(len(v)):
            s = v[index]
            tag = s['tags'][0]
            if dic.__contains__(tag):
                dic[tag] = dic[tag] + 1
            else:
                dic[tag] = 1

print(dic)