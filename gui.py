#!/usr/bin/env python3
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
from tkinter import scrolledtext 
from tkinter import messagebox
from itertools import compress
import os
import os.path
from pebble import ProcessPool
from time import sleep
import multiprocessing
import sys

from getlinks import *
from vlc_playlist import *
from rename import renamefiles
from tooltips import *
from path import resource_path

cl = None
loading = None
pl = None

def createloading():
    winimg = tk.PhotoImage(file=resource_path('./Assets/uoa_logo.png'))
    lw = tk.Toplevel(app)
    lw.resizable(False, False)
    lw.minsize(width=200, height=250)
    lw.title("Loading")
    lw.tk.call('wm', 'iconphoto', lw._w, winimg)
    lw.Label = tk.Label(lw, text="Please Wait...")
    lw.Label.pack()
    return lw

def selectitems(lectures,type):
        def select_all():
            for item in select:
                l = item
                if sa.get():
                    l.set(1)
                else:
                    l.set(0)
            print(list(compress(a, selection())))
        def selection():
            selection = []
            for item in select:
                selection.append(item.get())
            return selection

        global cl
        if (cl==None or not tk.Toplevel.winfo_exists(cl)):
            cl = tk.Toplevel(app)
            cl.title("Select Lectures")
            img = tk.PhotoImage(file=resource_path('./Assets/uoa_logo.png'))
            cl.tk.call('wm', 'iconphoto', cl._w, img)
            sa = tk.IntVar()
            sa.set(1)
            ttk.Checkbutton(cl, text="Select All",variable=sa,command=select_all).pack(anchor = 'w')
            sb = tk.Scrollbar(cl,orient="vertical")
            text = tk.Text(cl, width=40, height=20, yscrollcommand=sb.set)
            sb.config(command=text.yview)
            sb.pack(side="right",fill="y")
            text.pack(side="top",fill="both",expand=True)
            select=[]
            for i in range(len(lectures)):
                select.append(tk.IntVar())
                select[-1].set(1)
                cb = ttk.Checkbutton(text,text=lectures[i][1],variable=select[-1])
                text.window_create("end", window=cb)
                text.insert("end", "\n")
            try:
                a,b=zip(*lectures)
            except:
                cl.destroy()
                return
            a=list(a)
            b=list(b)
            for i in range(len(a)):
                a[i] = getFileURL(getId(a[i]))
            if type == "p":
                tk.Button(cl, text="Select",height=1,width=6,command= lambda: [cl.destroy(),app.textfield.delete('1.0', tk.END),createplaylist(list(compress(a, selection())),list(compress(b, selection())),app.dir.get("1.0",tk.END).rstrip())],bg="#5091cd").pack(anchor = 'w')
            elif type=="gl":
                tk.Button(cl, text="Select",height=1,width=6,command= lambda: [cl.destroy(),app.textfield.delete('1.0', tk.END),printlinks(list(compress(a, selection())))],bg="#5091cd").pack(anchor = 'w')

def guicreateplaylist():
    global pl
    global loading
    global cl
    if(cl == None or not tk.Toplevel.winfo_exists(cl)) and (loading == None or not tk.Toplevel.winfo_exists(loading)) and (pl==None or not tk.Toplevel.winfo_exists(pl)):
        input = app.textfield.get('1.0', 'end-1c')
        directory=app.dir.get("1.0",tk.END).rstrip()
        #Invalid directory
        if not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid Directory")
            return
        #No links
        if input == "":
            return
        else:
            result = False
            try:
                loading = createloading()
                with ProcessPool() as pool:
                    future = pool.schedule(inputLinks, args=[input,app.Traverse.get()])
                    while not future.done():
                        loading.update()
                        if not  tk.Toplevel.winfo_exists(loading):
                            future.cancel()
                            return
                        sleep(0.001)
                    result = future.result()
                loading.destroy()
            except:
                messagebox.showerror("Error", "Invalid Link(s)")
                loading.destroy()
                return
            if result: 
                f = open(resource_path("./Memory/playlist_dir.txt"),'r+')
                f.truncate(0)
                f.write(directory)
                f.close()
                selectitems(result,"p")

def browse():
    dir = filedialog.askdirectory()
    if dir:
        app.dir.delete('1.0', tk.END)
        app.dir.insert('1.0', dir)

def printlinks(links):
    global pl
    pl = tk.Toplevel(app)
    pl.title("Video Links")
    img = tk.PhotoImage(file=resource_path('./Assets/uoa_logo.png'))
    pl.tk.call('wm', 'iconphoto', pl._w, img)
    sb = tk.Scrollbar(pl,orient="vertical")
    text = tk.Text(pl, width=40, height=20, yscrollcommand=sb.set)
    sb.config(command=text.yview)
    sb.pack(side="right",fill="y")
    text.pack(side="top",fill="both",expand=True)

    for link in links:
        text.insert('1.0',link + "\n")


def getvideolinks():
    global pl
    global loading
    global cl
    if(cl == None or not tk.Toplevel.winfo_exists(cl)) and (loading == None or not tk.Toplevel.winfo_exists(loading)) and (pl==None or not tk.Toplevel.winfo_exists(pl)):
        input = app.textfield.get('1.0', 'end-1c')
        #No links
        if input == "":
            return
        else:
            result = False
            try:
	            loading = createloading()
	            with ProcessPool() as pool:
	                future = pool.schedule(inputLinks, args=[input,app.Traverse.get(),True])
	                while not future.done():
	                    loading.update()
	                    if not  tk.Toplevel.winfo_exists(loading):
	                        future.cancel()
	                        return
	                    sleep(0.001)
	                result = future.result()
	            loading.destroy()
            except:
                messagebox.showerror("Error", "Invalid Link(s)")
                loading.destroy()
                return
            if result[1]:
                app.textfield.delete('1.0', tk.END)
                selectitems(result[0],"gl")
            elif result[0]:
                app.textfield.delete('1.0', tk.END)
                a,b = result
                z,x =zip(*a)
                z = list(z)
                for i in range(len(z)):
                    z[i] = getFileURL(getId(z[i]))
                printlinks(z)

def renamedownloaded():
    global pl
    global loading
    global cl
    if(cl == None or not tk.Toplevel.winfo_exists(cl)) and (loading == None or not tk.Toplevel.winfo_exists(loading)) and (pl==None or not tk.Toplevel.winfo_exists(pl)):
        files = filedialog.askopenfilenames(parent=app,title='Choose a file')
        files = list(files)
        loading = createloading()
        with ProcessPool() as pool:
            future = pool.schedule(renamefiles, args=[files])
            while not future.done():
                loading.update()
                if not  tk.Toplevel.winfo_exists(loading):
                    future.cancel()
                    return
                sleep(0.001)
        loading.destroy()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    #Window
    app = tk.Tk()
    app.title("Delos Utilities")
    winimg = tk.PhotoImage(file=resource_path('./Assets/uoa_logo.png'))
    app.tk.call('wm', 'iconphoto', app._w, winimg)

    #Options
    app.Traverse = tk.IntVar()
    app.Traverse.set(0)
    ttk.Checkbutton(app,text="Include all search pages",variable=app.Traverse).grid(row=0,column=0,sticky=tk.W)
    rnmimg = tk.PhotoImage(file=resource_path('./Assets/renameicon.png'))
    app.rename = tk.Button(app, text="Rename downloaded files",image=rnmimg,height=40,width=48,command=renamedownloaded,bg="#5091cd",anchor="center")
    CreateToolTip(app.rename,"Rename downloaded files")
    app.rename.grid(row=0,column=3,sticky=tk.E)



    #Links Field
    app.textfield = scrolledtext.ScrolledText(app, wrap=tk.WORD)
    app.textfield.grid(row=1,column=0,columnspan=4,rowspan=2,sticky=tk.NSEW)

    #Add Links
    app.buttonframe = tk.Frame(app)
    app.buttonframe.grid(row=3, column=0, columnspan=1,sticky=tk.W)
    listimg = tk.PhotoImage(file=resource_path('./Assets/playlist.png'))
    app.playlist = tk.Button(app.buttonframe, text="Create Playlist",image=listimg,height=40,width=48,command=guicreateplaylist,bg="#5091cd",anchor="center")
    CreateToolTip(app.playlist,"Create playlist")
    app.playlist.grid(row=3,column=0,sticky=tk.W)
    CreateToolTip(app.rename,"Rename downloaded files")
    linkimg = tk.PhotoImage(file=resource_path('./Assets/link.png'))
    app.links = tk.Button(app.buttonframe, text="Get Links",image=linkimg,height=40,width=48,command=getvideolinks,bg="#5091cd",anchor="center")
    CreateToolTip(app.links,"Get video links")
    app.links.grid(row=3,column=1,sticky=tk.W)

    #Save directory for playlist
    app.browseframe = tk.Frame(app)
    app.browseframe.grid(row=3, column=3, columnspan=1,sticky=tk.E)
    tk.Label(app.browseframe, text="Save directory:").grid(row=2,column=2)
    app.dir = tk.Text(app.browseframe,height=1,width=35,wrap=tk.WORD)
    f = open(resource_path("./Memory/playlist_dir.txt"),'r')
    app.dir.insert('1.0', f.readline())
    f.close()
    app.dir.grid(row=3,column=2,sticky=tk.E)
    ttk.Button(app.browseframe, text="Browse",command=browse).grid(row=3,column=3,sticky=tk.E)

    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_columnconfigure(2, weight=1)
    app.grid_columnconfigure(3, weight=1)
    app.rowconfigure(0, weight=1)
    app.rowconfigure(1, weight=1)
    app.rowconfigure(2, weight=1)
    app.rowconfigure(3, weight=1)
            
    app.mainloop()