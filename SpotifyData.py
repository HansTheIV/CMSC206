import spotipy
from spotipy import client as cl
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials

import requests  # required for getting the csv file from spotify.chart   without 403 error: Forbidden
from io import StringIO  #

import json
import pandas as pd
from matplotlib import pyplot as plt
import plotly.express as px
from wordcloud import WordCloud
import multiprocessing as mp
from multiprocessing import Pool

from tqdm import tqdm



username = 'epalmer822'
CLIENT_ID = 'fc5e21deea874e2a9246c8e8935e9fe1'
CLIENT_SECRET = 'a79221482a5f40d286fc7b5e5c42e318'
NUM_OF_SONGS = 200
FIRST_SONG_ROW = 3
NUM_OF_ATTRIBUTES = 5
numbersList = list(range(FIRST_SONG_ROW, NUM_OF_SONGS))
URL_ROW = 4  # adjusted for columns being indexed at 1 in csv

NUM_OF_SONGS += 1  # compensate for headers (first song from spotify CSVs is listed in row 3)
genres = {"RAP" : 0, "OTHER": 0}
genre_list = list()

# ---- Cheolhong Ahn
csvFile = requests.get("https://spotifycharts.com/regional/us/weekly/latest/download", headers={
    'User-Agent': 'Mozilla/5.0'})  # we can replace 28 and 44 with this. Gets csv file directly from spotify.chart website.
fileData = StringIO(csvFile.text)  # requests and StringIO required to bypass  error:  urllib2.HTTPError: HTTP Error 403: Forbidden
inputCSV = pd.read_csv(fileData, header=1)




def checkCPUcount():  # ---- Ethan Ringel
    cores = mp.cpu_count()
    processes = int(cores / 2)
    print("Found " + str(cores) + " threads, using " + str(processes) + " processes.\n")
    return cores


class SongDataClass:
    dataPointCount = 0  # evaluate how many of the songs are actually being used as data points
    songAttributeDict = dict()


c = SongDataClass()


# each song data list will contain, in order, ['name'], ['artist], ['duration'], ['loudness'], ['tempo'], ['key'], and ['mode']
# indexed with the number of the position in top 200

# -------------------------------------------------------------------------------------------------------------------------

# notes: keys/modes are returned as numbers, but obviously a song isn't in the key of 5. Uses "standard pitch class notation"
# so on a scale of 1-11,

# 0 = C
# 1 = C#
# 2 = D
# 3 = Eb
# 4 = E
# 5 = F
# 6 = F#
# 7 = G
# 8 = G#
# 9 = A
# 10 = Bb
# 11 = B

# modes are also labeled as integers, but no support for more than the two most common modes, so the confidence value on that has to be lower
# because songs aren't always written in major or minor

# 0 = minor
# 1 = major


def numberToKey(keyNum):
    keys = {0: "C", 1: "C#", 2: "D", 3: "Eb", 4: "E", 5: "F", 6: "F#", 7: "G", 8: "G#", 9: "A", 10: "Bb", 11: "B"}
    try:
        return keys[keyNum]
    except KeyError:
        return "Invalid"


def numberToMode(modeNum):
    modes = {0: "Minor", 1: "Major"}
    try:
        return modes[modenum]
    except KeyError:
        return "Invalid"


# ----------------------------------------------------------------------------------------------------------------------

# made a function so multiprocessing can work

def SongDataSocket(i):  # ---- Ethan Ringel
    url = inputCSV.iloc[i - 1][
        URL_ROW]  # sets the song URL for this iteration of the loop, constant just in case spotify decides to reformat its

    songAnalysis = sp.audio_analysis(url)  # fetch the song attributes
    # confidenceValues = [songAnalysis['track']['tempo_confidence'],
    #                   songAnalysis['track']['time_signature_confidence'],
    #                 songAnalysis['track']['key_confidence'], songAnalysis['track']['mode_confidence']]

    # may implement that if I decide on logic that i like; otherwise it'll probably just disappear in an update eventually

    songAnalysis = songAnalysis['track']
    urlData = sp.track(url)
    trackData = \
        {
            'name': urlData['name'],
            'artist': urlData['album']['artists'][0]['name'],
            # for some reason spotify indexes all artist data in a list that only has one element, which is a dictionary. no clue why
            'duration': songAnalysis['duration'],
            'loudness': songAnalysis['loudness'],
            'tempo': songAnalysis['tempo'],
            'key': songAnalysis['key'],
            'mode': songAnalysis['mode']
            # 'extra data' : songAnalysis['extra data'] is always an option, we can use whatever data we decide we need
        }

    dataReturn = [str(i - 2), dict(trackData)]
    return dataReturn


result_list = []


def log_results(result):
    c.songAttributeDict.update({str(result[0]): result[1]})
    pbar.update(1)


def main(allowed_processes):  # ----Ethan Ringel
    pool = mp.Pool(processes=allowed_processes)  # creates a multiprocessing pool to fill the dictionary file

    for i in range(3, 203):
        pool.apply_async(SongDataSocket, args=(i,), callback=log_results)  # apply_async because they're indexed
        # by position, so what order they're
        # callback essentially feeds the output of                         # physically stored doesn't matter, can
        # SongDataSocket directly into log_results()                       # efficiently pull the correct data out regardless

    pool.close()
    pool.join()
    pool.close()


def print_results():
    print(c.songAttributeDict)


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(username=username, scope="user-library-read", client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET, redirect_uri="https://spotify.com"))
if __name__ == '__main__':
    sp.me()  # to trigger a spotify authentication, without opening 200 chrome tabs
    outFileName = "SpotifyDataDict.txt"
    try:
        with open(outFileName, 'r') as g:
            DataUsable = json.loads(
                g.read())  # checks to see if file exists, if it does, will just use existing data. If not, throws filenotfound, and will create a new file
    except FileNotFoundError:
        allowed_processes = checkCPUcount()
        pbar = tqdm(total=200)  # generates a progress bar
        main(allowed_processes)
        pbar.close()  # ends the progress bar so it isn't displayed twice
        with open(outFileName, 'w') as f:  # outputs the data to the file specified above
            f.write(json.dumps(c.songAttributeDict))
            DataUsable = json.dumps(c.songAttributeDict)

        # after this, DataUsable is set to what it needs to be regardless, but there will also be a file with the data so it does not need to be retrieved again.

    # plots -------------------------------------------------------------------------------------------------------




    # Key frequency ---- Ethan Ringel
    keyFreq = {"C": 0, "C#": 0, "D": 0, "Eb": 0, "F": 0, "F#": 0, "G": 0, "G#": 0, "A": 0, "Bb": 0, "B": 0}
    for num in range(1, 200):
        tempKey = DataUsable[str(num)]['key']
        tempKey = numberToKey(tempKey)
        if tempKey in keyFreq:
            keyFreq[tempKey] += 1
        else:
            keyFreq[tempKey] = 1
    labelList = list()
    dataList = list()
    for key in keyFreq:
        labelList.append(key)
        dataList.append(keyFreq[key])
    KFP = plt.figure()
    KFP = KFP.add_axes([0.05, 0.05, 0.90, 0.85])
    KFP.bar(labelList, dataList, color="olive")
    KFP.set_title("Frequency of musical keys in Spotify top 200")
    for bar in KFP.patches:
        KFP.annotate(format(bar.get_height(), '.0f'),
                     (bar.get_x() + bar.get_width() / 2,
                      bar.get_height() / 1.5), ha='center', va='center',
                     size=8, xytext=(0, 8),
                     textcoords='offset points')
    plt.show()


    # Artist Word Cloud ---- Cheolhong Ahn
    with open('SpotifyDataDict.txt', 'r') as inf:
        data = eval(inf.read())
    dataPd = pd.DataFrame.from_dict(data, orient='index')

    tracks = ' '.join(
        [artist for artist in dataPd['name']])  # change inputCSV to newDF if you decide to not change the inputCSV

    wordcloud = WordCloud(max_words=100, background_color="white").generate(tracks)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")
    plt.show()

    #Artist Diversity Bar Chart ---- Cheolhong Ahn
    # This shows how many artists are featured in top 200 chart to see how diverse the music chart is at the moment.

    with open('SpotifyDataDict.txt', 'r') as inf:
        data = eval(inf.read())
    dataPd = pd.DataFrame.from_dict(data, orient='index')

    totalArtists = len(dataPd['artist'])
    uniqueArtists = len(dataPd.drop_duplicates(subset=['artist']))

    fig = plt.figure()
    ax = fig.add_axes([0.075, 0.05, 0.95, 0.95])
    artistType = ["Unique Artists", "Number of Songs"]
    artistCount = [uniqueArtists, totalArtists]
    ax.bar(artistType, artistCount, color="purple")
    ax.set_title('Artist Diversity in the top chart')
    plt.show()

    # Genre Diversity- Talal Brek
    top_200_artists = inputCSV['Artist']
    for i in top_200_artists:
        artist = sp.search(q=i, type='artist')
        genre_str = ''
        for genre in artist['artists']['items'][0]['genres']:
            genre_str += genre
            genre_list.append(genre)
        if 'rap' in genre_str:
            genres['RAP'] += 1

        else:
            genres['OTHER'] += 1
        artist_list = i.split(' ')

    wordcloud_string = ''

    wordcloud = WordCloud(width=1600, height=800, max_font_size=200, background_color="white").generate(str(genre_list))
    # plt the image generated by WordCloud class
    plt.figure(figsize=(12, 10))
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.show()
    # plt.savefig('TBrek_Genre_WordCloud.png')

    x = list(genres.keys())
    y = list(genres.values())
    fig, axs = plt.subplots(2)
    plt.title("RAP VS OTHER GENRES TOP 200 2020", fontsize=14);
    axs[0].pie(x=y, autopct="%.1f%%", labels=x, pctdistance=0.5)

    # plt.savefig('tbrek_rap_vs_other_pie.png')
    axs[1].bar(x, y, width=0.2, color='maroon')
    plt.xlabel("Genres")
    plt.ylabel("No. of songs")
    plt.show()
    plt.title("RAP VS OTHER GENRES TOP 200 2020", fontsize=14);
    # plt.savefig('tbrek_rap_vs_other_bar.png')






    #Tempo Chart ---- Cheolhong Ahn
    # This graph shows that tempo is evenly distributed among top 200 chart by rank and shows no significant correlation between tempo and rank.
    # However, one thing to note is major songs showed even distribution around 80~160bpm  while minor songs were generally faster 120~160bpm
    #


    with open('SpotifyDataDict.txt', 'r') as inf:
        data = eval(inf.read())
    dataPd = pd.DataFrame.from_dict(data, orient='index')
    dataPd.index = dataPd.index.astype(int)
    dataPd = dataPd.sort_index(ascending=False)
    mean = str(dataPd["tempo"].mean()).split(".")[0] + "." + str(dataPd["tempo"].mean()).split(".")[1][:2]
    print("The average tempo of the top 200 spotify songs is ", mean, " bpm")

    TempoPlot = px.scatter(
        data_frame=dataPd,
        y="tempo",
        x=dataPd.index,
        color="tempo",
        hover_name='name',
        facet_col="mode",
    )
    TempoPlot.show()

