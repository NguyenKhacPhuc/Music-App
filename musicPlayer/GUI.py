import json
import os
import tkinter as tk
import urllib
from time import sleep
from tkinter import Tk, Label, IntVar, Button, Listbox, Checkbutton, Text, W, E, END, ACTIVE, S
from urllib.request import urlopen
from pygame import mixer
from youtube_dl import YoutubeDL


class MyGUI:
    def __init__(self, master):
        # Create the main window widget.

        self.sleep = True
        self.DATA = []
        self.colors = {
            'white': '#FFFFFF',
            'blue': '#2B547E',
            'black': '#000000',
            'red': '#FF3346',
            'green': '#306754',
            'grey': '#E5E4E2',
            'hex': '#9bcbff',
            'button_color': '#C0C0C0'
        }

        self.check = 0
        self.chosenSong = ''
        self.chosenId = 0
        self.POP = []
        self.CHILL = []
        self.DANCE = []
        self.check_pop = IntVar()
        self.check_chill = IntVar()
        self.check_dance = IntVar()
        self.master = master
        self.master.title('Music Player')
        self.master.configure(bg=self.colors['hex'])
        self.master.geometry('850x600')
        self.f_name = ''
        self.imagePath = tk.PhotoImage(file='Logo.png')
        self.rewindImg = tk.PhotoImage(file='rewind.png')
        self.playImage = tk.PhotoImage(file='play.png')
        self.pauseImage = tk.PhotoImage(file='pause.png')
        self.nextImage = tk.PhotoImage(file='unpause.png')
        self.image = tk.Label(master, image=self.imagePath, borderwidth=0, bg=self.colors['hex'])

        # widgets
        self.file_name_label = Label(
            master, fg=self.colors['black'], bg=self.colors['button_color'],
            text='Enter a name for your file: ',
            width=57, font='Helvetica 10 bold')

        self.pop = Checkbutton(
            master, fg=self.colors['black'], bg=self.colors['hex'],
            text='POP', highlightbackground=self.colors['black'],
            variable=self.check_pop)

        self.chill = Checkbutton(
            master, fg=self.colors['black'], bg=self.colors['hex'],
            text='CHILL', highlightbackground=self.colors['black'],
            variable=self.check_chill)

        self.dance = Checkbutton(
            master, fg=self.colors['black'], bg=self.colors['hex'],
            text='DANCE', highlightbackground=self.colors['black'],
            variable=self.check_dance)

        self.file_name = Text(
            master, fg=self.colors['blue'],
            bg=self.colors['grey'], width=57, height=1)

        self.explorer_label1 = Button(
            master, fg=self.colors['grey'], bg=self.colors['blue'],
            width=30, text='Download Tracks/Show Genres', command=self.download)

        self.explorer = Listbox(
            master, fg=self.colors['blue'], bg=self.colors['grey'],
            width=70, height=15, highlightcolor=self.colors['green'])

        self.explorer2 = Listbox(
            master, fg=self.colors['blue'], bg=self.colors['grey'],
            width=70, height=15, highlightcolor=self.colors['green'])

        self.search_btn = Button(
            master, fg=self.colors['grey'], bg=self.colors['blue'],
            width=30, text='Search', command=self.showGenre)

        self.delete_button = Button(
            master, fg=self.colors['white'],
            bg=self.colors['red'], text='DELETE', width=31,
            highlightbackground=self.colors['black'], command=self.delete)

        self.stop_button = Button(
            master, fg=self.colors['grey'], image=self.pauseImage,
            bg=self.colors['green'], text='PAUSE', width=80, font='Helvetica 10 bold',
            highlightbackground=self.colors['black'], command=self.stop)

        self.unpause_button = Button(
            master, fg=self.colors['grey'], image=self.playImage,
            bg=self.colors['green'], text='PAUSE', width=80, font='Helvetica 10 bold',
            highlightbackground=self.colors['black'], command=self.unpause)

        self.play_button = Button(
            master, image=self.playImage, fg=self.colors['grey'],
            bg=self.colors['green'], text='PLAY', width=80,
            highlightbackground=self.colors['black'], command=self.play)

        self.status_label = Label(
            master, fg=self.colors['grey'], bg=self.colors['black'],
            width=60, text='Hello')
        self.clear_button = Button(
            master, fg=self.colors['grey'],
            bg=self.colors['green'], text='CLEAR',
            width=15, highlightbackground=self.colors['black'], command=self.clear)

        self.rewind_button = Button(
            master, image=self.rewindImg, fg=self.colors['grey'],
            bg=self.colors['green'], text='REWIND', width=80,
            highlightbackground=self.colors['black'], command=self.rewind)

        self.next_button = Button(
            master, image=self.nextImage, fg=self.colors['grey'],
            bg=self.colors['green'], text='REWIND', width=80,
            highlightbackground=self.colors['black'], command=self.nextSelection)

        # grid
        self.image.grid(row=0, sticky=W + E)
        self.explorer.grid(row=7, sticky=W, padx=20)
        self.explorer2.grid(row=7, sticky=E, padx=20)
        self.play_button.grid(row=8, sticky=W, padx=100, pady=20)
        self.delete_button.grid(row=8, sticky=E, padx=20, pady=20)
        self.search_btn.grid(row=6, sticky=E, padx=20)
        self.status_label.grid(row=13, sticky=E + W, padx=20)
        self.rewind_button.grid(row=8, sticky=W, padx=20, pady=20)
        self.next_button.grid(row=8, sticky=W, padx=180, pady=20)
        self.file_name.grid(row=2, sticky=E, padx=20)
        self.displayAllData()

        if self.checkingConnection():
            self.file_name_label.grid(row=2, sticky=W, padx=20)
            self.file_name.grid(row=2, sticky=E, padx=20)
            self.pop.grid(row=3, sticky=W, padx=100, pady=5)
            self.chill.grid(row=3, pady=5)
            self.dance.grid(row=3, sticky=E, padx=100, pady=5)
            self.explorer_label1.grid(row=6, sticky=W, padx=20)
            self.clear_button.grid(row=8, sticky=W, padx=350, pady=20)

    # search_for_Genre
    def showGenre(self):
        keywords = self.file_name.get('1.0', END).strip()
        if self.check_pop.get() == 1 or keywords == 'POP':
            self.explorer.delete(0, 'end')
            self.getAllPopSongs()
        elif self.check_chill.get() == 1 or keywords == 'CHILL':
            self.explorer.delete(0, 'end')
            self.getAllChillSongs()
        elif self.check_dance.get() == 1 or keywords == 'DANCE':
            self.explorer.delete(0, 'end')
            self.getAllDanceSongs()

        elif keywords == 'ALL':
            self.explorer.delete(0, 'end')
            self.displayAllData()
        else:
            self.explorer.delete(0, 'end')
            self.search(keywords)

    # download

    def download(self):
        self.POP = []
        self.CHILL = []
        self.DANCE = []
        self.f_name = self.file_name.get('1.0', END).strip()
        options = {
            'default_search': 'ytsearch1',
            'quiet': True
        }
        ydl = YoutubeDL(options)
        search_result = ydl.extract_info(self.f_name, download=False)
        songs = search_result["entries"]
        self.downloadSong(songs[0]['id'])
        obj = {
            'ID': songs[0]['id'],
            'Title': self.f_name,
            'Creator': songs[0]['creator'],
            'Duration': songs[0]['duration'],
            'Alternative Title': songs[0]['alt_title']
        }
        if self.check_dance.get() == 1:
            self.DANCE.append(obj)
        elif self.check_chill.get() == 1:
            self.CHILL.append(obj)
        elif self.check_pop.get() == 1:
            self.POP.append(obj)
        self.saveData(obj)
        self.showGenre()

    def play(self):
        self.check = self.check + 1
        try:
            self.clear()
            self.displayIn4()
            self.chosenId = ''
        except Exception as FormatError:
            self.explorer2.insert("0", 'Format Error')
        chosenSong = self.explorer.get(ACTIVE).strip()
        self.chosenId = self.searchReturnId(chosenSong)
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        mixer.init()
        mixer.music.load("D:\\MusicPlayer\\musicPlayer\\musicdownloads\\" + self.chosenId + ".mp3")
        if self.check == 1:
            self.play_button.grid_forget()
            self.stop_button.grid(row=8, sticky=W, padx=100, pady=20)
            mixer.music.play()

    def rewind(self):
        mixer.music.rewind()

    def stop(self):

        self.check = self.check + 1
        if self.check % 2 == 0:
            self.unpause_button.grid(row=8, sticky=W, padx=100, pady=20)
            mixer.music.pause()
            self.stop_button.grid_forget()

    def unpause(self):

        self.check = self.check + 1
        if self.check % 2 != 0:
            self.stop_button.grid(row=8, sticky=W, padx=100, pady=20)
            self.unpause_button.grid_forget()
            mixer.music.unpause()

    def delete(self):
        deleting = self.explorer.get(ACTIVE).strip()
        dataPop = []
        dataChill = []
        dataDance = []
        allData = []
        a = {}
        allData = self.getAlldata()
        for item in range(len(allData)):
            if allData[item]['Title'] == deleting:
                a = allData[item]
        allData.remove(a)
        with open('data.json', 'w', encoding="utf8") as data_file:
            jsonData = json.dumps(allData)
            data_file.write(jsonData)
        openPop = open('pop.json')
        dataPop = json.load(openPop)
        openPop.close()
        tempK = {}
        for k in (dataPop):
            if k == a:
                tempK = k
                dataPop.remove(tempK)
        with open('pop.json', 'w', encoding="utf8") as pop_file:
            popData = json.dumps(dataPop)
            pop_file.write(popData)
        openChill = open('chill.json')
        dataChill = json.load(openChill)
        openChill.close()
        tempC = {}
        for c in (dataChill):
            if c == a:
                tempC = c
                dataChill.remove(tempC)
        with open('chill.json', 'w', encoding="utf8") as chill_file:
            chillData = json.dumps(dataChill)
            chill_file.write(chillData)
        openDance = open('dance.json')
        dataDance = json.load(openDance)
        openDance.close()
        tempD = {}
        for d in (dataDance):
            if d == a:
                tempD = d
                dataChill.remove(tempD)
        with open('dance.json', 'w', encoding="utf8") as dance_file:
            danceData = json.dumps(dataDance)
            dance_file.write(danceData)

    def saveData(self, obj):
        self.DATA.append(obj)
        data = []
        input_data = open('data.json')
        data = json.load(input_data)
        data = data + self.DATA
        input_data.close()
        with open('data.json', 'w', encoding="utf8") as data_file:
            jsonData = json.dumps(data)
            data_file.write(jsonData)

    def sort(self, arr):
        n = len(arr)
        # Traverse through all array elements
        for i in range(n):
            # Last i elements are already in place
            for j in range(0, n - i - 1):
                # traverse the array from 0 to n-i-1
                # Swap if the element found is greater
                # than the next element
                if arr[j]['Title'] > arr[j + 1]['Title']:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]

    def clear(self):
        self.file_name.delete('1.0', END)
        self.check_pop.set(0)
        self.check_dance.set(0)
        self.check_chill.set(0)
        self.explorer2.delete('0', END)

    def search(self, name):
        dataSearching = self.getAlldata()
        l = 0
        r = len(dataSearching) - 1
        self.sort(dataSearching)
        while l <= r:
            mid = int(l + (r - l) / 2);
            # Check if x is present at mid
            if dataSearching[mid]['Title'] == name:
                self.explorer.insert(0, dataSearching[mid]['Title'])
                break
            # If x is greater, ignore left half
            elif dataSearching[mid]['Title'] < name:
                l = mid +1
            # If x is smaller, ignore right half
            else:
                r = mid - 1

    def checkingConnection(self):
        try:
            urlopen('https://www.google.com', timeout=1)
            return True
        except urllib.error.URLError as Error:
            print(Error)
            return False

    def searchReturnId(self, name):
        dataSearchingID = self.getAlldata()
        l = 0
        r = len(dataSearchingID) - 1
        self.sort(dataSearchingID)
        while l <= r:
            mid = (l + (r - l) // 2);
            # Check if x is present at mid
            if dataSearchingID[mid]['Title'] == name:
                return dataSearchingID[mid]["ID"]
            # If x is greater, ignore left half
            elif dataSearchingID[mid]['Title'] < name:
                l = mid + 1
            # If x is smaller, ignore right half
            else:
                r = mid - 1

    def displayAllData(self):
        allData = self.getAlldata()
        self.sort(allData)
        for a in range(len(allData)):
            self.explorer.insert(len(allData), allData[a]['Title'])

    def downloadSong(self, id):
        options = {
            # specify the path to download
            'outtmpl': 'musicdownloads/%(id)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Tách lấy audio
                'preferredcodec': 'mp3',  # Format ưu tiên là mp3
                'preferredquality': '192',  # Chất lượng bitrate
            }]
        }
        ydl = YoutubeDL(options)
        # download() có thể truyền vào 1 str hoặc 1 list
        ydl.download(["https://www.youtube.com/watch?v={}".format(id)])

    def displayIn4(self):
        string = self.explorer.get(ACTIVE).strip()
        data = self.getAlldata()
        obj = {}
        for x in (data):
            if x['Title'] == string:
                obj = x
                break
        values = obj.values()
        for k, v in obj.items():
            self.explorer2.insert(len(values), k + ": " + str(v))

    def getAlldata(self):
        allData = []
        input_AllData = open('data.json')
        allData = json.load(input_AllData)
        input_AllData.close()

        return allData

    def nextSelection(self):
        if self.sleep:
            sleep(2)
        self.check = 0
        selection_indices = self.explorer.curselection()
        # default next selection is the beginning
        next_selection = 0
        # make sure at least one item is selected
        if len(selection_indices) > 0:
            # Get the last selection, remember they are strings for some reason
            # so convert to int
            last_selection = int(selection_indices[-1])
            # clear current selections
            self.explorer.selection_clear(selection_indices)
            # Make sure we're not at the last item
            if last_selection < self.explorer.size() - 1:
                next_selection = last_selection + 1
            self.explorer.activate(next_selection)
            self.explorer.selection_set(next_selection)
            self.play()

    def getAllChillSongs(self):
        chillLst = []
        input_chill = open('chill.json')
        chillLst = json.load(input_chill)
        chillLst = chillLst + self.CHILL
        input_chill.close()
        with open('chill.json', 'w', encoding="utf8") as chill_file:
            jsonChill = json.dumps(chillLst)
            chill_file.write(jsonChill)
            self.sort(chillLst)
        for y in range(len(chillLst)):
            self.explorer.insert(len(chillLst), chillLst[y]['Title'])

    def getAllDanceSongs(self):
        danceLst = []
        input_dance = open('dance.json')
        danceLst = json.load(input_dance)
        danceLst = danceLst + self.DANCE
        input_dance.close()
        with open('dance.json', 'w', encoding="utf8") as dance_file:
            jsonDance = json.dumps(danceLst)
            dance_file.write(jsonDance)
        self.sort(danceLst)
        for d in range(len(danceLst)):
            self.explorer.insert(len(danceLst), danceLst[d]['Title'])

    def getAllPopSongs(self):
        popLst = []
        input_pop = open('pop.json')
        popLst = json.load(input_pop)
        danceLst = popLst + self.DANCE
        input_pop.close()
        with open('dance.json', 'w', encoding="utf8") as dance_file:
            jsonDance = json.dumps(popLst)
            dance_file.write(jsonDance)
        self.sort(popLst)
        for d in range(len(popLst)):
            self.explorer.insert(len(popLst), popLst[d]['Title'])


root = Tk()
my_gui = MyGUI(root)
root.mainloop()
