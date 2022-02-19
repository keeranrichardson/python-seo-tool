# python-seo-tool

You can install all the dependencies using the requirements.txt file.

'''shell
pip install -r requirements.txt
'''

You may not have tkinter installed. If you get error messages about tkinter not being installed, then install it. See this link for more details.
 
https://tkdocs.com/tutorial/install.html

## Run the application

to run the application:

```shell
python main.py
```
By default it will show the GUI.

You can run it from the command line with the parameter `-cmd=True`

The command line options are:

```shell
usage: main.py [-h] [-url URL] [-filename FILENAME] [-cmd CMD] [-reportPath REPORTPATH] [-rateLimit RATELIMIT] [-openReport OPENREPORT]

Scan site for URLs

options:
  -h, --help             show this help message and exit
  -url URL               the url to scan
  -filename FILENAME     the filename of the html report output file
  -cmd CMD               run the program from the command line
  -reportPath REPORTPATH path where HTML report will be stored              
  -rateLimit RATELIMIT   milliseconds to wait between scans
  -openReport OPENREPORT automatically opens report when finished              
```

For example:

To scan keeranrichardson.com from the command line with rate limiting then use the command

```shell
python main.py -url=https://keeranrichardson.com -rateLimit=1000 -cmd=True
```

or

```shell
python main.py -url https://keeranrichardson.com -rateLimit 1000 -cmd True
```

By default the report will open in your default browser when run from the command line.

To change this use the option `-openReport=False`

If you do not add a `-url` option when running from the command line, the tool will prompt you to enter a url.

## Run the tests

To run the tests you require `pytest`

To install pytest:

```shell
pip install pytest
```

To run the tests:

```shell
pytest
```

