from urllib.parse import urlparse
import tkinter as tk
import tkinter.scrolledtext as scrolledtext
from tkinter import filedialog
from scanner import Scanner
from reportGenerator import ReportGenerator
from browserController import BrowserController
from sitemapScanner import SitemapScanner
from validateUrl import ValidateUrl


class TkinterGui:
    def __init__(self, configParams):
        self.configParams = configParams
        self.scanIsActive = False
        self.window = None
        self.txtfld = None
        self.rateLimitValue = None
        self.enterPath = None
        self.pathLabel = None
        self.startScanBtn = None
        self.pauseScanBtn = None
        self.continueScanBtn = None
        self.reportBtn = None
        self.showLogs = None
        self.scanner = None
        self.report = None

    def showGui(self):
        self.window = tk.Tk()
        self.window.title('link checker')
        #self.window.geometry("300x200+10+10")

        tk.Label(text="Enter domain or sitemap URL:").pack()

        entryFrame = tk.Frame(self.window)

        self.txtfld=tk.Entry(entryFrame)
        self.txtfld.insert(0, self.configParams.getUrlToParse())
        self.txtfld.pack(fill = 'x')

        entryFrame.pack(padx = 20, fill = 'x')

        tk.Label(text="Select rate limiting value (milliseconds):").pack()

        self.rateLimitValue = tk.IntVar()
        self.rateLimitValue.set(self.configParams.getRateLimit())
        rateLimitMenu = tk.OptionMenu(self.window, self.rateLimitValue, 2000, 1000, 500, 0)
        rateLimitMenu.pack()

        enterFileNameFrame = tk.Frame(self.window)

        tk.Label(enterFileNameFrame, text="Enter file name of HTML report:").pack()

        self.enterPath=tk.Entry(enterFileNameFrame)
        self.enterPath.insert(0, self.configParams.getHTMLReportFileName())
        self.enterPath.pack(fill = 'x')

        enterFileNameFrame.pack(padx = 20, fill = 'x')

        choosePathButton = tk.Button(self.window, text = "select path for HTML report", command = self.choosePath)
        choosePathButton.pack()

        self.pathLabel = tk.Label(text="Path for HTML report = "+self.getCurrentHTMLReportPath())
        self.pathLabel.pack()

        buttonFrame = tk.Frame(self.window)

        self.startScanBtn=tk.Button(buttonFrame, text="Start Scan", command = self.startScan)
        self.startScanBtn.pack(side = tk.LEFT)

        self.pauseScanBtn=tk.Button(buttonFrame, text="Pause Scan", command = self.pauseScan)
        self.pauseScanBtn.pack(side = tk.LEFT)
        self.pauseScanBtn["state"] = "disabled"

        self.continueScanBtn=tk.Button(buttonFrame, text="Continue Scan", command = self.unpauseScan)
        self.continueScanBtn.pack(side = tk.LEFT)
        self.continueScanBtn["state"] = "disabled"

        buttonFrame.pack()

        scrolledTextFrame = tk.Frame(self.window)

        self.reportBtn=tk.Button(self.window, text="open report", command = self.openReport)
        self.reportBtn.pack()
        self.reportBtn["state"] = "disabled"

        self.showLogs=scrolledtext.ScrolledText(scrolledTextFrame)
        #self.showLogs.see(tk.END)
        self.showLogs.pack(fill = 'both', expand = True)

        scrolledTextFrame.pack(padx = 20, pady = 20, fill = 'both', expand = True)

        self.window.mainloop()

    def startScan(self):
        self.configParams.setReportFileName(self.enterPath.get())
        urlToParse = self.getUrlToParse()
        urlValidator = ValidateUrl(urlToParse)

        if not urlValidator.canUrlBeScanned():
            self.showErrorMessage("error: url is not valid")
            return

        parseUrl = urlparse(urlToParse)

        self.scanner = Scanner(urlToParse, parseUrl.netloc)

        sitemapScanner = SitemapScanner(urlToParse)
        if sitemapScanner.isSitemap():
            sitemapScanner.addSitemapUrlsToScan(self.scanner)
            self.scanner.setCanCrawlUrls(False)

        self.startScanBtn.config(text = "Restart Scan")

        self.startScanBtn["state"] = "normal"
        self.reportBtn["state"] = "disabled"
        self.pauseScanBtn["state"] = "normal"
        self.continueScanBtn["state"] = "disabled"

        self.showLogs.delete("1.0", tk.END)

        self.scanIsActive = True
        self.continueScan()

    def continueScan(self):
        if self.scanIsActive is True and self.scanner.isMoreToScan():
            eventLog = self.scanner.scanNext()
            # update gui
            for event in eventLog:
                self.addToTextBox(event)

            # tkinter does not update the GUI when rate limit is 0
            rateLimitValue = self.rateLimitValue.get()
            if rateLimitValue < 1:
                rateLimitValue = 1

            self.window.after(rateLimitValue, self.continueScan)

        else:

            if self.scanner.isMoreToScan():
                self.startScanBtn["state"] = "normal"
                self.reportBtn["state"] = "normal"
                self.pauseScanBtn["state"] = "disabled"
                self.continueScanBtn["state"] = "normal"

            else:
                self.startScanBtn["state"] = "normal"
                self.reportBtn["state"] = "normal"
                self.pauseScanBtn["state"] = "disabled"
                self.continueScanBtn["state"] = "disabled"
                self.addToTextBox("Scan finished")

            self.showLogs.see(tk.END)
            self.generateReport()

    def addToTextBox(self, text):
        self.showLogs.see(tk.END)
        self.showLogs.insert(tk.END, text+"\n")
        self.showLogs.see(tk.END)

    def pauseScan(self):
        self.scanIsActive = False

        self.startScanBtn["state"] = "normal"
        self.reportBtn["state"] = "normal"
        self.pauseScanBtn["state"] = "disabled"
        self.continueScanBtn["state"] = "normal"

        self.addToTextBox("Scan paused")

    def unpauseScan(self):
        self.scanIsActive = True
        self.continueScan()

        self.startScanBtn["state"] = "normal"
        self.reportBtn["state"] = "disabled"
        self.pauseScanBtn["state"] = "normal"
        self.continueScanBtn["state"] = "disabled"

        self.addToTextBox("Scan unpaused")

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



#TkinterGui().showGui()
