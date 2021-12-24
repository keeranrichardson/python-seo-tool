import os
from folderUtils import FolderUtils
from htmlreporter import HTMLReporter


class ReportGenerator:
    def __init__(self, configParams, scanner):
        self.configParams = configParams
        self.scanner = scanner

    def generateReport(self):
        fileName = self.configParams.getHTMLReportFileName()
        path = self.getPath()

        FolderUtils().createFolderIfNotExists(path)
        
        #creates full directory
        self.pathAndFileName = os.path.join(path, fileName)

        #writes report to file
        file = open(self.pathAndFileName, "w")
        file.write(HTMLReporter(self.scanner.getResults()).makeReport())
        file.close()

    def getPathAndFileName(self):
        return self.pathAndFileName

    def getPath(self):
        path = self.configParams.getReportPath()

        if path == '':
            #creates directory
            directory = "reports"

            reportsFolder = FolderUtils()
            path = reportsFolder.getCWDPath(directory)

        return path