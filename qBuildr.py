import sys
import random
import pprint
import spotipy
import spotipy.util as util
import urllib.request
import tkinter as tk
from PIL import ImageTk, Image

#Must specify a path to display images of cover art
#NOTE: Change the path to whatever fits your local machine
picturePath = 'C:\\Users\\Eric\\Desktop\\qBuildr.jpg'

def searchSong(name):
    result = sp.search(name, limit = 1)
    items = result['tracks']['items'][0]
    songID = items['id']
    artist = items['artists'][0]['name']
    return (songID, artist)

def choosePlaylist():
    print()
    print('What playlist do you want to shuffle through?')
    for playlist in myPlaylists.keys():
        print ('-' + playlist)
    curPlaylist = input()
    while curPlaylist not in myPlaylists.keys():
        print('Playlist does not exist! Please choose another:')
        curPlaylist = input()
    return curPlaylist

#Class to build the window for the swipe function
class App():
    #Builds the tKinter window, loading in all widgets and cover art
    def __init__(self):
        self.isDone = False
        self.window = tk.Tk()
        urllib.request.urlretrieve(tup[2], "C:\\Users\\Eric\\Desktop\\qBuildr.jpg")
        self.window.title(tup[0] + ' - ' + tup[1])
        self.window.geometry("600x700")
        self.window.configure(background='grey')
        path = picturePath
        #Creates a Tkinter-compatible photo image
        img = ImageTk.PhotoImage(Image.open(path))
        #Label widget to display a text or image on the screen
        panel = tk.Label(self.window, image = img)
        #Pack geometry manager to pack widgets in rows and columns
        panel.grid(row=0, column = 0, columnspan=3, rowspan=3)
        #Start the GUI
        buttonLeft = tk.Button (self.window, text = "<==", command = self.swipeLeft, bg='red')
        buttonLeft.grid(row=2, column=0, in_ = self.window)
        buttonUp = tk.Button (self.window, text = "^^", command = self.swipeUp, bg='blue', fg = 'orange')
        buttonUp.grid(row=2, column=1, in_ = self.window)
        buttonRight = tk.Button (self.window, text = "==>", command = self.swipeRight, bg='green', fg = 'red')
        buttonRight.grid(row=2, column=2, in_ = self.window)
        buttonQuit = tk.Button (self.window, text = 'STOP', command = self.quit, bg='yellow')
        buttonQuit.grid(row=0, column=0, in_=self.window)
        self.window.mainloop()
    #Functions to implement interaction with widgets
    def swipeLeft(self):
        self.window.destroy()
    def swipeRight(self):
        sp.user_playlist_add_tracks(username, myPlaylists[newPlaylist], [tup[3]])
        print (tup[0] + ' by ' + tup[1] + ' added to playlist')
        self.window.destroy()
    def swipeUp(self):
        sp.user_playlist_add_tracks(username, myPlaylists[newPlaylist], [tup[3]], position = 0)
        print ('Super like! ' + tup[0] + ' by ' + tup[1] + ' added to front of playlist')
        self.window.destroy()
    def quit(self):
        self.isDone = True
        self.window.destroy()

#info for QBuildr
scope = 'playlist-modify-private playlist-read-private playlist-modify-public streaming'
client_id='36db8e86be2b4d69bd9095b092eac617'
client_sec='987dd190af9444cea7eeaea8da56135c'
redirect_uri='http://localhost:3000/'

#authentification of token and account
if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print ('Usage: %s username' % (sys.argv[0],))
    sys.exit()
token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)
if not token:
    print ("Can't get token for" + username)
    sys.exit()
sp = spotipy.Spotify(auth=token)
sp.trace = False

#create dictionary of playlist names with id
myPlaylists = {}
playlists = sp.user_playlists(username)
for playlist in playlists['items']:
    myPlaylists[playlist['name']] = playlist['id']

print('Welcome to QBuildr! Making a playlist has never been this fun!')

#creates new playlist
print('What do you want to name your dope new queue?')
newPlaylist = input()
while newPlaylist in myPlaylists:
    print('Playlist already exists! Pick another name:')
    newPlaylist = input()
print('Creating ' + newPlaylist + '...')
sp.user_playlist_create(username, newPlaylist)
playlists = sp.user_playlists(username)
for playlist in playlists['items']:
    myPlaylists[playlist['name']] = playlist['id']

#Initiates building of playlist
options = ['-shuffle playlist(s)', '-by name(n)', '-exit(x)']
while True:
    print ('How would you like to add songs?')
    for prompt in options:
        print (prompt)
    task = input()
    if task == 's':
        chosen = choosePlaylist()
        toShuffle = sp.user_playlist_tracks(username, myPlaylists[chosen])
        songs = []
        for song in toShuffle['items']:
            id = song['track']['id']
            name = song['track']['name']
            artist = (song['track']['artists'][0]['name'])
            url = song['track']['album']['images'][0]['url']
            songs.append((name, artist, url, id))
        random.shuffle(songs)
        print(chosen + ' has been shuffled! Get ready to start swiping!')
        print('Click "left" to skip, "right" to add to the end of the playlist, and "up" to add it to the top')
        print('Click STOP to move on')
        for tup in songs:
            tmp = App()
            if tmp.isDone:
                break
    elif task == 'n':
        print('What songs do you want to add? (separate search queries with commas)')
        songName = input()
        songs = songName.split(', ')
        titles = []
        for song in songs:
            res = searchSong(song)
            titles.append(res[0])
            print('Adding ' + song + ' by ' + res[1])
        sp.user_playlist_add_tracks(username, myPlaylists[newPlaylist], titles)
        print('...done')
    elif task == 'x':
        break
    else:
        print ('Not a valid task')