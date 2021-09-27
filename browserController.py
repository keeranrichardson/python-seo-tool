import subprocess
import os

#https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python

class BrowserController:
    def __init__(self):
        ''

    def open(self, file):
        try: 
            os.startfile(file) #opens file in default viewer for filetype
        except AttributeError: #https://stackoverflow.com/questions/29823028/attributeerror-module-object-has-no-attribute-startfile
            try: 
                subprocess.call(['open', file]) 
            except:
                print('Could not open '+str(file))