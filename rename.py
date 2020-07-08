from getlinks import *
import os

def renamefiles(files):
    filenames = []
    for file in files:
        filenames.append(getVideoName(getWebSiteURL((file.split("/"))[-1].split(".")[0])))
    for i in range(len(files)):
        if filenames[i]:
            #Remove windows forbiden characters
            filenames[i] = filenames[i].replace(":","_")
            filenames[i] = filenames[i].replace("/","")
            filenames[i] = filenames[i].replace("\\","")
            filenames[i] = filenames[i].replace("*","")
            filenames[i] = filenames[i].replace("?","")
            filenames[i] = filenames[i].replace("<","")
            filenames[i] = filenames[i].replace(">","")
            filenames[i] = filenames[i].replace("|","")
            
            os.rename(files[i],(files[i].rsplit("/", 1)[0] + "/" + filenames[i].rstrip(' ') + "." + files[i].rsplit(".", 1)[1]))