import json
    
imdb = []
for line in open('/home/andrew/414/Data-Science-Techniques/INST414.w2/E1/imdb_movies_1985to2022.json', 'r'):
    imdb.append(json.loads(line))


totalavg = []
counter = 0

for x in imdb:
    for actorName in imdb[counter]["actors"]:
        #print(actorName[1])
        if actorName[1] == "Hugh Jackman":
            totalavg.append(imdb[counter]["rating"]["avg"])
            #print(imdb[counter]["title"])

    counter = counter + 1

#print(totalavg)
print("The average rating of Hugh Jackman movies is", sum(totalavg) / len(totalavg))