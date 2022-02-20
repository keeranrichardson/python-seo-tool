import os
from folderUtils import FolderUtils
from htmlreporter import HTMLReporter

class ReportGenerator:
    """Writes the HTML report to a file
    
    This class triggers the HTML report generation and writes it to a file.
    The file is configured by the configuration parameters.
    
    Typical usage example:
    
    report = ReportGenerator(configParams, scanner)
    report.generateReport()

    Attributes:
        configParams: The ConfigParams object which is used to configure the output report
        scanner: The Scanner object which is used to get results
    """
    def __init__(self, configParams, scanner):
        self.configParams = configParams
        self.scanner = scanner
        self.pathAndFileName = ''

    def generateReport(self):
        fileName = self.configParams.getHTMLReportFileName()
        path = self.getPath()

        FolderUtils().createFolderIfNotExists(path)

        #creates full directory
        self.pathAndFileName = os.path.join(path, fileName)

        #writes report to file
        file = open(self.pathAndFileName, "w", encoding = "utf8")
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
        