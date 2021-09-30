from htmlreporter import HTMLReporter

class TestHTMLReporter:
    
    def testATag(self):
        
        assert "<a href = 'keeranrichardson.com' target='_blank'>mywebsite</a>" == HTMLReporter('').aTag("keeranrichardson.com", "mywebsite")