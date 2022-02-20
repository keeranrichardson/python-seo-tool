from validateUrl import ValidateUrl

class TestValidateUrl:
    
    def testCanUrlBeScanned(self):
        # A full url is valid
        assert True is ValidateUrl("https://keeranrichardson.com").canUrlBeScanned()
        # A url without a scheme is invalid
        assert False is ValidateUrl("keeranrichardson.com").canUrlBeScanned()
        # A url without a netloc is invalid
        assert False is ValidateUrl("https://").canUrlBeScanned()
        # A url without a netloc or a scheme is invalid
        assert False is ValidateUrl("").canUrlBeScanned()

    def testTryAndMakeValidUrl(self):
        # Adds scheme to url without scheme
        assert "https://keeranrichardson.com" == ValidateUrl("keeranrichardson.com").tryAndMakeValidUrl()
        # Adds https:// to relative link
        assert "https://keeranrichardson.com" == ValidateUrl("/keeranrichardson.com").tryAndMakeValidUrl()
        # Adds https:// to type of links returned in sitemap
        assert "https://keeranrichardson.com" == ValidateUrl("//keeranrichardson.com").tryAndMakeValidUrl()
        # Do not add https:// to already valid links
        assert "https://keeranrichardson.com" == ValidateUrl("https://keeranrichardson.com").tryAndMakeValidUrl()
        