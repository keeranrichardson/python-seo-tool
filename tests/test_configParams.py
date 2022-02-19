from configParams import ConfigParams

class TestConfigParams:
    
    def testIsGuiDefaultIsTrue(self):
        configParams = ConfigParams()
        configParams.getDefaultConfigParams()
        assert True == configParams.isGui()
