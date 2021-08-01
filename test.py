import pathlib

parentDirPath = str(pathlib.Path(__file__).parent.absolute())

a = "r"
Files = ["TwitterIDs", "postIDs"]
for file in Files:
    path = parentDirPath + "//replyIDs//" + str(18703193) + file + ".txt"
    with open(path, a) as f:
        q = f.read()
        print(q)
