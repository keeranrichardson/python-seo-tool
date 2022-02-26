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
    """The tkinter GUI for the application

    This class creates the tkinter GUI for the tool and handles the scan
    through the tool.

    Typical usage example:

    gui = TkinterGui(configParams)
    gui.showGui()

    Attributes:
        configParams: A ConfigParams object
    """

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

        # creates tkinter window
        self.window = tk.Tk()
        self.window.title("link checker")

        tk.Label(text="Enter domain or sitemap URL:").pack()

        entryFrame = tk.Frame(self.window)

        # adds a text field to the entry frame
        # by default add the url to scan configured
        # from the command line to the text field
        self.txtfld = tk.Entry(entryFrame)
        self.txtfld.insert(0, self.configParams.getUrlToParse())

        # have the text field fill the x axis
        self.txtfld.pack(fill="x")

        entryFrame.pack(padx=20, fill="x")

        # create configuration of rate limit value from GUI using a dropdown
        tk.Label(text="Select rate limiting value (milliseconds):").pack()
        self.rateLimitValue = tk.IntVar()
        self.rateLimitValue.set(self.configParams.getRateLimit())
        rateLimitMenu = tk.OptionMenu(
            self.window, self.rateLimitValue, 2000, 1000, 500, 0
        )
        rateLimitMenu.pack()

        # input for filename of HTML report
        enterFileNameFrame = tk.Frame(self.window)
        tk.Label(enterFileNameFrame, text="Enter file name of HTML report:").pack()

        # by default adds the report file name configured from the command line to
        # the entry where user can configure filename from the GUi
        self.enterPath = tk.Entry(enterFileNameFrame)
        self.enterPath.insert(0, self.configParams.getHTMLReportFileName())
        self.enterPath.pack(fill="x")

        enterFileNameFrame.pack(padx=20, fill="x")

        # button to show file dialog to select path to write HTML report
        choosePathButton = tk.Button(
            self.window, text="select path for HTML report", command=self.choosePath
        )
        choosePathButton.pack()

        # show the HTML path in the GUI as a label
        self.pathLabel = tk.Label(
            text="Path for HTML report = " + self.getCurrentHTMLReportPath()
        )
        self.pathLabel.pack()

        buttonFrame = tk.Frame(self.window)

        # button to start a new scan
        self.startScanBtn = tk.Button(
            buttonFrame, text="Start Scan", command=self.startScan
        )
        self.startScanBtn.pack(side=tk.LEFT)

        # button to pause a scan as it is running to
        # allow creating a report for an unfinished scan
        self.pauseScanBtn = tk.Button(
            buttonFrame, text="Pause Scan", command=self.pauseScan
        )
        self.pauseScanBtn.pack(side=tk.LEFT)
        self.pauseScanBtn["state"] = "disabled"

        # button to continue a paused scan
        self.continueScanBtn = tk.Button(
            buttonFrame, text="Continue Scan", command=self.unpauseScan
        )
        self.continueScanBtn.pack(side=tk.LEFT)
        self.continueScanBtn["state"] = "disabled"

        buttonFrame.pack()

        scrolledTextFrame = tk.Frame(self.window)

        # button to generate and open a report
        self.reportBtn = tk.Button(
            self.window, text="open report", command=self.openReport
        )
        self.reportBtn.pack()
        self.reportBtn["state"] = "disabled"

        # a text area which shows the progress of a scan
        # it will scroll as more items are added
        self.showLogs = scrolledtext.ScrolledText(scrolledTextFrame)
        self.showLogs.pack(fill="both", expand=True)

        scrolledTextFrame.pack(padx=20, pady=20, fill="both", expand=True)

        self.window.mainloop()

    def startScan(self):
        """
        To start a scan we get the report path from the config
        then check the url is valid. Create a scanner object
        and get the initial set of URLs to scan.
        """
        self.configParams.setReportFileName(self.enterPath.get())
        urlToParse = self.getUrlToParse()
        urlValidator = ValidateUrl(urlToParse)

        if not urlValidator.canUrlBeScanned():
            self.showErrorMessage("error: url is not valid")
            return

        parseUrl = urlparse(urlToParse)

        self.scanner = Scanner(urlToParse, parseUrl.netloc)

        # if the URL the user entered was a sitemap.xml then
        # use the SitemapScanner to get the initial set of URLs
        sitemapScanner = SitemapScanner(urlToParse)
        if sitemapScanner.isSitemap():
            sitemapScanner.addSitemapUrlsToScan(self.scanner)
            self.scanner.setCanCrawlUrls(False)

        # Configure the button to start the
        # scan from the beginning again
        self.startScanBtn.config(text="Restart Scan")

        # set all the button states to allow pausing
        self.startScanBtn["state"] = "normal"
        self.reportBtn["state"] = "disabled"
        self.pauseScanBtn["state"] = "normal"
        self.continueScanBtn["state"] = "disabled"

        # clear the progress log
        self.showLogs.delete("1.0", tk.END)

        # mark the scan as active and start scanning
        self.scanIsActive = True
        self.continueScan()

    def continueScan(self):
        """
        This is the main scanning loop. The next item in the loop
        is controlled by triggered by the tkInter `after` event method.
        The scan is controlled by the Scanner object, this loop
        reports progress into the text area.
        """

        if self.scanIsActive is True and self.scanner.isMoreToScan():

            # scan the next item in the Scanner scan list
            eventLog = self.scanner.scanNext()

            # update gui with all log items
            # returned by the scanNext call
            for event in eventLog:
                self.addToTextBox(event)

            # tkinter does not update the GUI when rate limit is 0
            # so ensure the rate limit is never set to 0
            rateLimitValue = self.rateLimitValue.get()
            if rateLimitValue < 1:
                rateLimitValue = 1

            # schedule the scan loop using the `after` method
            self.window.after(rateLimitValue, self.continueScan)

        else:

            # if there is nothiing more to scan then
            # set the buttons depending on if we are finished or paused
            if self.scanner.isMoreToScan():
                # there is more to scan so we are paused
                self.startScanBtn["state"] = "normal"
                self.reportBtn["state"] = "normal"
                self.pauseScanBtn["state"] = "disabled"
                self.continueScanBtn["state"] = "normal"

            else:
                # the scan is finished so allow it to be restarted
                self.startScanBtn["state"] = "normal"
                self.reportBtn["state"] = "normal"
                self.pauseScanBtn["state"] = "disabled"
                self.continueScanBtn["state"] = "disabled"
                self.addToTextBox("Scan finished")

            # scroll the event logs text area to the end
            self.showLogs.see(tk.END)

            # generate an HTML report even if we are just paused
            self.generateReport()

    def addToTextBox(self, text):
        """
        Add a line of text to the end of
        the text area and scroll the area.
        """
        self.showLogs.see(tk.END)
        self.showLogs.insert(tk.END, text + "\n")
        self.showLogs.see(tk.END)

    def pauseScan(self):
        """
        Pause the scan by setting scanIsActive to False
        and configure the buttons to allow continue,
        restart or reporting
        """
        self.scanIsActive = False

        self.startScanBtn["state"] = "normal"
        self.reportBtn["state"] = "normal"
        self.pauseScanBtn["state"] = "disabled"
        self.continueScanBtn["state"] = "normal"

        self.addToTextBox("Scan paused")

    def unpauseScan(self):
        """
        Continue the scan by setting scanIsActive to True
        and configure the buttons to allow pause or restart
        """
        self.scanIsActive = True
        self.continueScan()

        self.startScanBtn["state"] = "normal"
        self.reportBtn["state"] = "disabled"
        self.pauseScanBtn["state"] = "normal"
        self.continueScanBtn["state"] = "disabled"

        self.addToTextBox("Scan unpaused")

    def openReport(self):
        """
        Open the report in the default browser
        """
        BrowserController().open(self.report.getPathAndFileName())

    def generateReport(self):
        """
        Use the ReportGenerator to create the HTML report file
        """
        self.report = ReportGenerator(self.configParams, self.scanner)
        self.report.generateReport()

    def getUrlToParse(self):
        """
        Get the url value entered by the user
        """
        return self.txtfld.get()

    def showErrorMessage(self, errorMessage):
        """
        Show an alert box with an error message
        """
        tk.messagebox.showerror(title="error", message=errorMessage)

    def choosePath(self):
        """
        Show a file dialog to the user so they can select a directory
        to write the report to. When the user chooses a directory
        then display it on the GUI.
        """
        reportPath = filedialog.askdirectory()
        if len(reportPath) == 0:
            return

        self.configParams.setReportPath(reportPath)
        self.pathLabel.config(
            text="Path for HTML report = " + self.getCurrentHTMLReportPath()
        )

    def getCurrentHTMLReportPath(self):
        """
        Get the path the ReportGenerator will write the report to.
        """
        return ReportGenerator(self.configParams, None).getPath()
