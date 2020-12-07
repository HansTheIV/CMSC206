import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt

with open('SpotifyDataDict.txt','r') as inf:
    data = eval(inf.read())
dataPd = pd.DataFrame.from_dict(data, orient='index')

tracks = ' '.join([artist for artist in dataPd['name']])      # change inputCSV to newDF if you decide to not change the inputCSV

wordcloud = WordCloud(max_words=100).generate(tracks)
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")
plt.show()



