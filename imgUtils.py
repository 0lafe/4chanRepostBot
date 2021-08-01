from PIL import Image

def reSize(imgPath):
    img = Image.open(imgPath)  
    newsize = (1080, 1080) #resize depending on platform
    img = img.resize(newsize) 
    img.save(imgPath)

def convert(path1): #converts png to jpg for some platforms
    im1 = Image.open(path1)
    im2 = im1.convert('RGB')
    path2 = path1[:(len(path1)-3)] + "jpeg"
    im2.save(path2)
    return path2