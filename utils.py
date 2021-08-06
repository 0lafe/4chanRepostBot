from progressbar import printProgressBar
from imgUtils import *
from tweeting import *
import pathlib
import json
from progressbar import printProgressBar

parentDirPath = str(pathlib.Path(__file__).parent.absolute())
PLACEHOLDERNAME = "placeHolder.file"

def uploadPosts(imgFileLocations, thread):
    totalPosts = len(imgFileLocations)
    for i, aimgFileLocation in enumerate(imgFileLocations):
        ID = thread.ReplyIDs[i]
        if "." in aimgFileLocation:
            extension = getFileExtension(aimgFileLocation)
            if extension == ".png":
                convert(aimgFileLocation)
            aimgFileLocation = checkFileSize(aimgFileLocation)
        uploadTwitter(aimgFileLocation, thread, i, ID)
        printProgressBar(i, totalPosts-1)

def getName(imgURL, board):
    p1 = imgURL.index(board)+len(board)+1
    p2 = imgURL.rfind(".")
    name = ""
    for a in range(p2-p1):
        b = p1 + a
        name = name + imgURL[b]
    return name

def getText(html):
    text = str(html)
    start = text.find('>')+1
    end = text.rfind('</blockquote>')
    message = ""
    for a in range(end-start):
        r = start+a
        message = message + text[r]
    return message

def dumpQuote(text):
    text = text.replace('<span class=\"quote\">&gt;', ">")
    text = text.replace("</span>", "")
    return text

def dumpAts(text):
    ID = ""
    if "<a class=\"quotelink\" href=\"#p" in text:
        text = text.replace("<a class=\"quotelink\" href=\"#p", "")
        a = text.index("\"")
        ID = text[0:a]
        b = text.index("a>")
        text = text[b+2:]
        text = text.replace("\">&gt;&gt;", "")
        text = text.replace("</a>", "")
    text = [text, ID]
    return text

def prettyMessage(text):
        addBreaks = text.replace('<br/>', '\n')
        noQuotes = dumpQuote(addBreaks)
        return noQuotes

def getImgUrl(html):
    link = str(html)
    if "href=" in link:
        pos = link.index("href=")
        p1 = link.index("\"", pos)+3
        p2 = link.index("\"", p1+1)
        url = ""
        for a in range(p2-p1):
            b = p1+a
            url = url + link[b]
    else:
        url = ""
    return url

def getFileExtension(file):
    extensionPos = file.rfind(".")
    extensionVal = ""
    for a in range(len(file)-extensionPos):
        b = extensionPos + a
        extensionVal = extensionVal + file[b]
    return extensionVal

def stripID(post):
    String = str(post)
    start = String.index("id=")+5
    stop = String.index('\"', start)
    ID = ""
    for a in range (stop-start):
        b = start+a
        ID = ID + String[b]
    return ID

def writeIDs(IDList, OPID):
    rPath = parentDirPath + "/threadIDs/" + str(OPID) + ".txt"
    sIDList = listToStr(IDList, ",")
    with open(rPath, "w") as file:
        file.write(sIDList)

def strToList(IDString, Seperator): #converts string of IDs to a list of IDs
    if len(IDString) == 0:
        return []
    IDList = []
    tempIDString = ''
    for letter in IDString:
        if letter != Seperator:
            tempIDString =  tempIDString + letter
        else:
            IDList.append(tempIDString)
            tempIDString = ''
    return IDList

def listToStr(list, Seperator):
    sList = ""
    for element in list:
        sList = sList + element + Seperator
    return sList
    

def deleteImageFiles():
    filePath = parentDirPath + "/files/"
    files = os.listdir(filePath)
    for file in files:
        if file != PLACEHOLDERNAME:
            afilePath = parentDirPath + file
            os.remove(afilePath)
