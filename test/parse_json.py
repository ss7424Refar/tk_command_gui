import json

f = open('C:/Users/skr/Desktop/mira/videos/7sites/1.steps_1/101.mp4.json', 'r')
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
            # print(s)
            tag = s["tags"]
            if tag:
                tag = tag[0]
                if dic.__contains__(tag):
                    dic[tag] = dic[tag] + 1
                else:
                    dic[tag] = 1

print(dic)