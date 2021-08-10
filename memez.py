from Grabbers import *
from postClass import thread


URL = 'https://boards.4channel.org/lit/thread/18819502' #Url you wish to download from
allHtmlContent = requests.get(URL) #gets all the html content from the URL
print("Website Captured!")
crash = [".webm", '.gif'] #files that cant be uploaded to the certain site
board = "lit" #url title of the specific board

aThread = thread(board, allHtmlContent)

aThread.loadAuth()
print('Auth tokens loaded!')
aThread.isolatePosts()
print("Posts isolated!")
aThread.removeReposts()
print("Reposts Removed!")
aThread.loadReplyData()
aThread.storeImgUrls()
aThread.storeText()
aThread.storeIDs()
print("Posts and IDs stored!")
aThread.getCurrentIDs()
aThread.upload()
print("Posts Uploaded!")
aThread.saveIDs("write")
deleteImageFiles()
print("Finished!")


