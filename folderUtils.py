import os

class FolderUtils:
    def __init__(self):
        ''

    def createCWDFolder(self):
        path = self.getCWDPath()
        self.createPath(path)

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
        except OSError as error:
            pass
