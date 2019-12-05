import os
import threading
from tkinter import *
from mutagen.mp3 import MP3
import tkinter.messagebox
from tkinter import filedialog
from tkinter import ttk
from ttkthemes import themed_tk as tk

import time
from pygame import mixer

root =tk.ThemedTk()
root.get_themes()
root.set_theme("plastik")

statusbar = Label(root, text = "welcome to mplayer", relief = SUNKEN, font = 'Times 15 bold')
statusbar.pack(side = BOTTOM, fill = X)

#create menubar
menubar = Menu(root)
root.config(menu = menubar)

playlist = []

#playlist - contains the path + filename
#playlisbox - contains only the filename
#Path + filename is required for playing music inside play_music and load music
def browse_file():
    global filename_path
    filename_path = filedialog.askopenfilename()
    add_to_playlist(filename_path)

def add_to_playlist(filename):
    filename = os.path.basename(filename)
    index = 0
    playlistbox.insert(index, filename)
    playlist.insert(index, filename_path)
    playlistbox.pack()
    index +=1

#create submenu
subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "File", menu = subMenu)
subMenu.add_command(label = "Open", command = browse_file)
subMenu.add_command(label = "Exit", command = root.destroy)

def about_us():
    tkinter.messagebox.showinfo('About mplayer', 'This is a music player build using python tkinter developed by zakir hossain')

subMenu = Menu(menubar, tearoff = 0)
menubar.add_cascade(label = "Help", menu = subMenu)
subMenu.add_command(label = "About us", command = about_us)

mixer.init() #initializing the mixer
root.title("Mplayer")
root.iconbitmap(r'images/mplayer.ico')

#Root Window - StatusBar, RightFrame, LeftFrame
#LeftFrame - Listbox(playlist)
#RightFrame - TopFrame, MiddleFrame, BottomFrame

leftframe = Frame(root)
leftframe.pack(side = LEFT, padx = 20)

playlistbox = Listbox(leftframe)
playlistbox.pack()

addBtn = ttk.Button(leftframe, text = "Add", command = browse_file)
addBtn.pack(side = LEFT)

def del_song():
    selected_song = playlistbox.curselection()
    selected_song = int(selected_song[0])
    playlistbox.delete(selected_song)
    playlist.pop(selected_song)

deleteBtn = ttk.Button(leftframe, text = "Delete", command = del_song)
deleteBtn.pack(side = RIGHT)

rightframe = Frame(root)
rightframe.pack(pady = 30)

topframe = Frame(rightframe)
topframe.pack()

lengthlabel = ttk.Label (topframe, text = 'Total Length --:--')
lengthlabel.pack(pady = 5)

currenttimelabel = ttk.Label (topframe, text = 'Current Time --:--', relief = GROOVE)
currenttimelabel.pack()

#functions goes here
def show_details(play_song):
    statusbar['text'] = "Playing"+ '-'+os.path.basename(play_song)

    file_data = os.path.splitext(play_song)

    if file_data[1] == '.mp3':
        audio = MP3(play_song)
        total_length = audio.info.length
    else:
        a = mixer.Sound(play_song)
        total_length = a.get_length()

    #div - total_length/60, mod - total_length % 60
    mins, secs = divmod(total_length, 60)
    mins = round(mins)
    secs = round(secs)
    timeformat = '{:02d}:{:02d}'.format(mins,secs)
    lengthlabel['text'] = "Total length " + '' +timeformat

    t1 = threading.Thread(target = start_count, args = (total_length, ))
    t1.start()

def start_count(t):
    global  paused
    current_time = 0
    #mixer.music.get_busy(): returns FALSE when we press the stop button(music stops playing)
    while current_time<=t and mixer.music.get_busy():
        if paused:
            continue
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins,secs)
            currenttimelabel['text'] = "Current Time " + '' +timeformat
            time.sleep(1)
            current_time += 1

def play_music():
    global paused
    global play_it
    if paused:
        mixer.music.unpause()
        statusbar['text'] = "Music resumed"
        statusbar['text'] = os.path.basename(play_it)
        paused = FALSE
    else:
        try:
            stop_music()
            time.sleep(1)
            selected_song = playlistbox.curselection()
            selected_song = int(selected_song[0])
            play_it = playlist[selected_song]
            mixer.music.load(play_it)
            mixer.music.play()
            statusbar['text'] = "Playing music"+'-'+os.path.basename(play_it)
            show_details(play_it)
        except:
            tkinter.messagebox.showerror('mplayer','File not found!')

def stop_music():
    mixer.music.stop()
    statusbar['text'] = "Music stopped"

paused = FALSE

def pause_music():
    global paused
    paused = TRUE
    mixer.music.pause()
    statusbar['text'] = "Music paused"

def set_vol(val):
    volume = float(val)/100
    mixer.music.set_volume(volume)

def replay_music():
    play_music()
    statusbar['text'] = "Music rewinded"

muted = FALSE
def mute_music():
    global muted
    if muted: #unmute the music
        mixer.music.set_volume(0.3)
        speakerBtn.configure(image = speakerPhoto)
        scale.set(30)
        muted = FALSE
    else: #mute the music
        mixer.music.set_volume(0)
        speakerBtn.configure(image = mutePhoto)
        scale.set(0)
        muted = TRUE

#middleframe for play, pause and stop
middleframe = Frame(rightframe)
middleframe.pack(padx = 30, pady = 30)

playPhoto = PhotoImage(file = 'images/play.png')
playBtn = ttk.Button(middleframe, image = playPhoto, command = play_music)
playBtn.grid(row = 0, column = 0,padx = 5)

stopPhoto = PhotoImage(file = 'images/stop.png')
stopBtn = ttk.Button(middleframe, image = stopPhoto, command = stop_music)
stopBtn.grid(row = 0, column = 1,padx = 5)

pausePhoto = PhotoImage(file = 'images/pause.png')
pauseBtn = ttk.Button(middleframe, image = pausePhoto, command = pause_music)
pauseBtn.grid(row = 0, column = 2,padx = 5)

#bottomframe for rewind, speaker and mute
bottomframe = Frame(rightframe)
bottomframe.pack()

replayPhoto = PhotoImage(file ='images/replay.png')
replayBtn = ttk.Button(bottomframe, image = replayPhoto, command = replay_music)
replayBtn.grid(row = 0, column = 0, padx = 20)

mutePhoto = PhotoImage(file = 'images/mute.png')
speakerPhoto = PhotoImage(file = 'images/speaker.png')
speakerBtn = ttk.Button(bottomframe, image = speakerPhoto, command = mute_music)
speakerBtn.grid(row = 0, column = 1)

scale = ttk.Scale(bottomframe, from_=0, to_=100, orient= HORIZONTAL, command= set_vol)
scale.set(30)
mixer.music.set_volume(0.3)
scale.grid(row = 0, column = 2, pady = 15)

def on_closing():
    stop_music()
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
