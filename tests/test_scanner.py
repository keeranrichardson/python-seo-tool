from scanner import Scanner

class TestConfigParams:
    
    def testUrlAddsHttps(self):
        scanner = Scanner("keeranrichardson.com","keeranrichardson.com")
        assert "https://keeranrichardson.com" == scanner.getUrlFromQueue("keeranrichardson.com").getURL()