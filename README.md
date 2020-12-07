# Spotify Data Project


Requirements.txt contains the short list of dependencies required to run the project. 
Install each of them with either pip or conda, and you should be good to go.

For spotipy to work, you will need to grant it access through your spotify account. 
Change the username to your own in the "username" variable found on line 14 of DictionarySorting.py. Upon the first run of the program, it will throw an error: "unable to read cache at [filename]." DO NOT PANIC. This is normal. It will then ask for a url that you were redirected to. In order to be redirected, you must run this code on your local machine; google colab does not work. Simply grant the application access in your new browser window, and then copy and paste the URL into the console.




You can replace "US_Top200_10-10-2020.csv" with a different top-200 spotify chart 
(you may need to change the constants if spotify decided to change their formatting, but that's unlikely)

