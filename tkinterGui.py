import tkinter as tk
from scanner import Scanner
from urllib.parse import urlparse


class TkinterGui:
    def __init__(self):
        ''
    def showGui(self):
        window = tk.Tk()
        window.title('link checker')
        window.geometry("300x200+10+10")

        tk.Label(text="Enter URL:").pack()

        self.txtfld=tk.Entry(window)
        self.txtfld.pack()

        btn=tk.Button(window, text="Start Scan", command = self.startScan)
        btn.pack()

        text=tk.Text(window, height = 5)
        text.pack()

        btn2=tk.Button(window, text="show report")
        btn2.pack()

        window.mainloop()

    def startScan(self):
        urlToParse = self.getUrlToParse()
        parseUrl = urlparse(urlToParse)
        #todo: add url validation, needs to have netloc and scheme
        scanner = Scanner(urlToParse, parseUrl.netloc)
        scanner.scan()

    def getUrlToParse(self):
        return self.txtfld.get()



#TkinterGui().showGui()
