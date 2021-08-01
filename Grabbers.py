from utils import *
from bs4 import BeautifulSoup
import requests


def grabOP(allHtmlContent): #gets the whole OP HTML from the full page HTML
    soup = BeautifulSoup(allHtmlContent.content, 'html.parser')
    OPHTML = soup.find_all('div', class_="postContainer opContainer")
    return OPHTML

def getOPID(OPHTML): #gets the post ID of the OP
    for post in OPHTML:
        ID = post.find('div', class_= 'post op')
    return stripID(ID)

def grabReplies(OP, allHtmlContent): #gets all replies from the page's whole HTML
    soup = BeautifulSoup(allHtmlContent.content, 'html.parser')
    RepliesHTML = soup.find_all('div', class_="postContainer replyContainer")
    return OP + RepliesHTML

def saveFile(imgURLs, board): #saves the file from each post
    paths = []
    for imgURL in imgURLs:
        if "." in imgURL:
            fullURL = str("http://" + imgURL)
            savedFile = requests.get(fullURL, allow_redirects=True)
            fileType = getFileExtension(fullURL)
            name = "\\files\\" + getName(imgURL, board)
            realSavedPath = parentDirPath + name + fileType
            open(realSavedPath, 'wb').write(savedFile.content)
            paths.append(realSavedPath)
        else:
            paths.append("") #if no file associated with the post, it will place a 0 length string to keep ordering between posts and imgs
    return paths #saves names of files for uploading later


