import os


class FolderUtils:
    """Utility methods for creating folders

    To abstract away any operating system specific file handling,
    I've created utility methods for handling the paths and directories

    Typical usage example:

    FolderUtils().createFolderIfNotExists(path)
    """

    def __init__(self):
        """"""

    def getCWDPath(self, folderName):
        """
        gets current working directory
        """
        parentDir = os.getcwd()
        return os.path.join(parentDir, folderName)

    def createFolderIfNotExists(self, path):
        """
        creates a path if it doesn't exist
        """
        if os.path.exists(path) and os.path.isdir(path):
            pass
        else:
            self.createPath(path)

    def createPath(self, path):
        """
        tries to make a path
        """
        try:
            os.mkdir(path)
        except OSError as e:
            print("Exception when trying to Create Path" + str(path))
            print(e)
