from os import write
from utils import *
from Grabbers import *

class thread:
    def __init__(self, board, allHtmlContent) -> None:
        self.board = board
        self.allHtmlContent = allHtmlContent

    def isolatePosts(self):
        self.OP = grabOP(self.allHtmlContent)
        self.threadID = getOPID(self.OP)
        self.allPosts = grabReplies(self.OP, self.allHtmlContent)

    def removeReposts(self): #removes posts already uploaded
        fullPath = parentDirPath + "/threadIDs/" + str(self.threadID) + ".txt"
        try:
            with open(fullPath, "r") as file:
                alreadyUPloadedIDs = file.read()
                alreadyUPloadedIDs = strToList(alreadyUPloadedIDs, ",")
                LastDone = int(alreadyUPloadedIDs[-1]) #sets the most recent post ID to the last ID in the saved ID list
        except:
            LastDone = 0 #if no file exists of IDs, set the most recent posted ID to 0 to allow all IDs
        newPosts = []
        for post in self.allPosts:
            ID = post.find('div', class_= 'post op')
            if ID is None:
                ID = post.find('div', class_='post reply')
            ID = int(stripID(ID))
            if ID > LastDone:
                newPosts.append(post)
        self.posts = newPosts

    def storeImgUrls(self):
        imgs = []
        for post in self.posts:
            img = post.find('a', class_='fileThumb')
            imgUrl = getImgUrl(img)
            imgs.append(imgUrl)
        self.IMGUrls = imgs

    def storeText(self):
        texts = []
        replyIDs = []
        for post in self.posts:
            HTMLtext = post.find('blockquote', class_='postMessage')
            postText = getText(HTMLtext)
            postText = prettyMessage(postText)
            postText = dumpAts(postText)
            replyIDs.append(postText[1])
            texts.append(postText[0])
        self.ReplyIDs = replyIDs
        self.MSGS = texts


    def storeIDs(self):
        IDs = []
        for post in self.posts:
            ID = post.find('div', class_= 'post op')
            if ID is None:
                ID = post.find('div', class_='post reply')
            ID = stripID(ID)
            IDs.append(ID)
        if len(IDs) > 0:
            writeIDs(IDs, self.threadID)
        self.postIDs = self.postIDs + IDs

    def upload(self):
        imgFileLocations = saveFile(self.IMGUrls, self.board)
        print("Uploading " + str(len(imgFileLocations)) + " posts!")
        uploadPosts(imgFileLocations, self)

    def saveIDs(self, action):
        aTwitterIDs = []
        apostIDs = []
        if action == 'write':
            a = 'w'
        else:
            a = 'r'
        Files = ["TwitterIDs", "postIDs"]
        for file in Files:
            path = parentDirPath + "/replyIDs/" + str(self.threadID) + file + ".txt"
            try:
                with open(path, a) as f:
                    if action == "write":
                        savedIDs = listToStr(getattr(self, file), ",")
                        f.write(savedIDs)
                    else:
                        if file == "TwitterIDs":
                            aTwitterIDs = f.read()
                        else:
                            apostIDs = f.read()
            except:
                pass
        return [strToList(aTwitterIDs, ","), strToList(apostIDs, ",")]

    def loadReplyData(self):
        inputIDs = self.saveIDs("read")
        self.TwitterIDs = inputIDs[0]
        self.postIDs = inputIDs[1]
        
    def getCurrentIDs(self):
        path = parentDirPath + "/threadIDs/" + str(self.threadID) + ".txt"
        with open(path, "r") as f:
            self.currentIDs = strToList(f.read(), ",")

    def loadAuth(self):
        path = parentDirPath + "/authFiles.json"
        with open(path) as f:
            tokens = json.load(f)
        self.replyauthv = tokens['REPLYauthv']
        self.replyauths = tokens['REPLYauths']
        self.replytoken = tokens['REPLYtoken']
        self.replytokens = tokens['REPLYtokens']

        self.OPauthv = tokens[self.board + 'authv']
        self.OPauths = tokens[self.board + 'auths']
        self.OPtoken = tokens[self.board + 'token']
        self.OPtokens = tokens[self.board + 'tokens']
        