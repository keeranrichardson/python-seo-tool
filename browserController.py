import subprocess
import os
import webbrowser

#https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python
#https://stackoverflow.com/questions/29823028/attributeerror-module-object-has-no-attribute-startfile

class BrowserController:
    """Opens the browser to display a file

    The method open() is cross platform between Windows, Mac and Linux.
    open() trys multiple methods to open the default browser.

    Typical usage example:

    BrowserController().open(fileNameString)
    """

    def __init__(self):
        ''

    def open(self, file):
        try:
            webbrowser.open(file)
        except AttributeError:
            try:
                os.startfile(file) #opens file in default viewer for filetype
            except:
                try:
                    subprocess.call(['open', file])
                except Exception as e:
                    print("Exception when opening report")
                    print(e)
                    print('your HTML report is here: '+str(file))
                    