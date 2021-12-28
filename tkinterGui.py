import tkinter as tk
from scanner import Scanner
from urllib.parse import urlparse
from tkinter import messagebox
import tkinter.scrolledtext as scrolledtext
from reportGenerator import ReportGenerator
from browserController import BrowserController
from tkinter import filedialog


class TkinterGui:
    def __init__(self, configParams):
        self.configParams = configParams

    def showGui(self):
        self.window = tk.Tk()
        self.window.title('link checker')
        #self.window.geometry("300x200+10+10")

        tk.Label(text="Enter URL:").pack()

        self.txtfld=tk.Entry(self.window)
        self.txtfld.pack()

        tk.Label(text="Select rate limiting value (milliseconds):").pack()

        self.rateLimitValue = tk.IntVar()
        self.rateLimitValue.set(0)
        self.rateLimitMenu = tk.OptionMenu(self.window, self.rateLimitValue, 2000, 1000, 500, 0)
        self.rateLimitMenu.pack()

        tk.Label(text="Enter file name of HTML report:").pack()

        self.enterPath=tk.Entry(self.window)
        self.enterPath.pack()

        self.choosePathButton = tk.Button(self.window, text = "select path for HTML report", command = self.choosePath)
        self.choosePathButton.pack()

        self.pathLabel = tk.Label(text="Path for HTML report = "+self.getCurrentHTMLReportPath())
        self.pathLabel.pack()

        self.startScanBtn=tk.Button(self.window, text="Start Scan", command = self.startScan)
        self.startScanBtn.pack()

        self.showLogs=scrolledtext.ScrolledText(self.window, height = 5)
        #self.showLogs.see(tk.END)
        self.showLogs.pack()

        self.btn2=tk.Button(self.window, text="open report", command = self.openReport)
        self.btn2.pack()
        self.btn2["state"] = "disabled"

        self.window.mainloop()

    def startScan(self):
        self.configParams.setReportFileName(self.enterPath.get()) 
        urlToParse = self.getUrlToParse()
        urlValidator = ValidateUrl(urlToParse)

        if not urlValidator.canUrlBeScanned():
            self.showErrorMessage("error: url is not valid")
            return

        parseUrl = urlparse(urlToParse)
        #todo: add url validation, needs to have netloc and scheme
        self.scanner = Scanner(urlToParse, parseUrl.netloc)
        #scanner.scan()
        self.startScanBtn["state"] = "disabled"
        self.btn2["state"] = "disabled"
        self.continueScan()

    def continueScan(self):
        if(self.scanner.isMoreToScan()):
            eventLog = self.scanner.scanNext()
            # update gui
            for event in eventLog:
                self.showLogs.see(tk.END)
                self.showLogs.insert(tk.END, event+"\n") 
                self.showLogs.see(tk.END)
                               
            self.window.after(self.rateLimitValue.get()+1, self.continueScan)
        
        else:
            self.startScanBtn["state"] = "normal"
            self.btn2["state"] = "normal"
            self.showLogs.see(tk.END)
            self.generateReport()

    def openReport(self):
        BrowserController().open(self.report.getPathAndFileName())

    def generateReport(self):
        self.report = ReportGenerator(self.configParams, self.scanner)
        self.report.generateReport()

    def getUrlToParse(self):
        return self.txtfld.get()

    def showErrorMessage(self, errorMessage):
        tk.messagebox.showerror(title = "error", message = errorMessage)

    def choosePath(self):
        reportPath = filedialog.askdirectory()
        if len(reportPath) == 0:
            return

        self.configParams.setReportPath(reportPath)
        self.pathLabel.config(text = "Path for HTML report = "+self.getCurrentHTMLReportPath())

    def getCurrentHTMLReportPath(self):
        return ReportGenerator(self.configParams, None).getPath()

class ValidateUrl:
    def __init__(self, url):
        self.url = url

    def canUrlBeScanned(self):
        parseUrl = urlparse(self.url)
        if parseUrl.netloc != '' and parseUrl.scheme != '':
            return True
        else:
            return False



#TkinterGui().showGui()
