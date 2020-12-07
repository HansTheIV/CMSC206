#This graph shows that tempo is evenly distributed among top 200 chart by rank and shows no significant correlation between tempo and rank.
#However, one thing to note is major songs showed even distribution around 80~160bpm  while minor songs were generally faster 120~160bpm
#
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px



with open('SpotifyDataDict.txt','r') as inf:
    data = eval(inf.read())
dataPd = pd.DataFrame.from_dict(data, orient='index')
dataPd.index = dataPd.index.astype(int)
dataPd = dataPd.sort_index(ascending= False)



print("The average tempo of top 200 song is ", dataPd["tempo"].mean(), "bpm")


fig = px.scatter(
    data_frame= dataPd,
    y = "tempo",
    x = dataPd.index,
    color = "tempo",
    hover_name= 'name',
    facet_col= "mode",
  
)
fig.show()