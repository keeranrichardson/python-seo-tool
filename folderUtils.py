import os

class FolderUtils:
    def __init__(self, folderName):
        self.folderName = folderName

    def createCWDFolder(self):
        path = self.getCWDPath()
        try:
            os.mkdir(path)
        except OSError as error:
            pass

    def getCWDPath(self):
        parentDir = os.getcwd() #gets current working directory
        return os.path.join(parentDir, self.folderName)