#This shows how many artists are featurerd in top 200 chart to see how diverse the music chart is at the moment.

import pandas as pd
import matplotlib.pyplot as plt



with open('SpotifyDataDict.txt','r') as inf:
    data = eval(inf.read())
dataPd = pd.DataFrame.from_dict(data, orient='index')

totalArtists = len(dataPd['artist'])
uniqueArtists = len(dataPd.drop_duplicates(subset=['artist']))


fig = plt.figure()
ax = fig.add_axes([0,0,1,1])
artistType = ["UniqueArtists", "Number of Songs"]
artistCount = [uniqueArtists,totalArtists]
ax.bar(artistType, artistCount)
ax.set_title('Artist Diversity in the top chart')
plt.show()
