import subprocess
import os
import webbrowser

#https://stackoverflow.com/questions/40905703/how-to-open-an-html-file-in-the-browser-from-python

class BrowserController:
    def __init__(self):
        ''

    def open(self, file):
        try: 
            webbrowser.open(file)
        except AttributeError: #https://stackoverflow.com/questions/29823028/attributeerror-module-object-has-no-attribute-startfile
            try: 
                os.startfile(file) #opens file in default viewer for filetype
            except:
                try:
                    subprocess.call(['open', file]) 
                except Exception as e:
                    print(e)
                    print('your HTML report is here: '+str(file))