import os

class FolderUtils:
    def __init__(self):
        ''

    def getCWDPath(self, folderName):
        parentDir = os.getcwd() #gets current working directory
        return os.path.join(parentDir, folderName)

    def createFolderIfNotExists(self, path):
        if os.path.exists(path) and os.path.isdir(path):
            pass
        else:
            self.createPath(path)

    def createPath(self, path):
        try:
            os.mkdir(path)
        except OSError as e:
            print("Exception when trying to Create Path" + str(path))
            print(e)
