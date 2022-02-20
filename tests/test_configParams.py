from configParams import ConfigParams
import datetime

class TestConfigParams:

    def testIsGuiDefaultIsTrue(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        assert True is configParams.isGui()

    def testDefaultFilenameHasCurrentDate(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        assert year in configParams.getHTMLReportFileName()
        assert month in configParams.getHTMLReportFileName()
        assert day in configParams.getHTMLReportFileName()

    def testDefaultRateLimit(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        assert 0 is configParams.getRateLimit()

    def testOpenReportByDefault(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        assert True is configParams.getOpenReport()

    def testEnsureBooleanValueConvertsStrings(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        assert True is configParams.ensureBooleanValue("true")
        assert True is configParams.ensureBooleanValue("True")
        assert True is configParams.ensureBooleanValue("TRue")
        assert False is configParams.ensureBooleanValue("false")
        assert False is configParams.ensureBooleanValue("False")
        assert False is configParams.ensureBooleanValue("FAlse")

    def testEnsureBooleanValueConvertsBoolean(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        assert True is configParams.ensureBooleanValue(True)
        assert False is configParams.ensureBooleanValue(False)

    def testGetCurrentDateString(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        year = datetime.datetime.now().strftime("%Y")
        month = datetime.datetime.now().strftime("%m")
        day = datetime.datetime.now().strftime("%d")
        starts = year + "-" + month + "-" + day
        assert configParams.getCurrentDateString().startswith(starts)

    def testHtmlFileNaming(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        
        # adds .html if necessary
        assert "name.html" == configParams.getAsHtmlFileName("name")
        assert "name.html" == configParams.getAsHtmlFileName("name.html")
        # removes spaces
        assert "abc.html" == configParams.getAsHtmlFileName("a b c")
        # allow capitals lowercase numbers and some punctuation
        assert "AZaz-_.09.html" == configParams.getAsHtmlFileName("AZaz-_.09")
        # trim out invalid characters
        assert "A.html" == configParams.getAsHtmlFileName("A@£$%^&*()+={}[]:;'~`?<>,")
        # adds date if empty given
        year = datetime.datetime.now().strftime("%Y")
        assert configParams.getAsHtmlFileName("").startswith(year)
        assert configParams.getAsHtmlFileName("").endswith(".html")

    def testNoUrlByDefault(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        
        assert "" == configParams.getUrlToParse()

    def testCanConfigureParams(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        configParams.setRateLimit(3000)
        configParams.setReportFileName("filename.html")
        configParams.setReportPath("/folder/")
        assert 3000 is configParams.getRateLimit()
        assert "filename.html" is configParams.getHTMLReportFileName()
        assert "/folder/" == configParams.getReportPath()
