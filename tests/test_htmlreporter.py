from htmlreporter import HTMLReporter
from scanner import ScannerResults
from urlResult import UrlResult

class TestHTMLReporter:
    
    def testATag(self):
        
        assert "<a href = 'keeranrichardson.com' target='_blank'>mywebsite</a>" == HTMLReporter('').aTag("keeranrichardson.com", "mywebsite")

    def testMakeReport(self):

        scannerResults = ScannerResults()
        scannerResults.add(UrlResult("keeranrichardson.com", "200", "keeranrichardson.com"))
        scannerResults.add(UrlResult("keeranrichardson.com/bob", "404", "keeranrichardson.com"))

        report = HTMLReporter(scannerResults).makeReport()

        assert "keeranrichardson.com" in report 
        assert "keeranrichardson.com/bob" in report 
        assert "200" in report 
        assert "404" in report 
     