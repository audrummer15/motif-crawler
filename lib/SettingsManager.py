import os
import ConfigParser

class SettingsManager(object):
    SETTINGS_FILE = os.path.join("config", "settings.cfg")
    SECTION_CREDENTIALS = "Credentials"
    SETTING_EMAIL = "Email"
    SETTING_PASSWORD = "Password"
    SETTING_PHONE = "Phone"

    def __init__(self):
        self.cp = ConfigParser.ConfigParser()

    def getEmail(self):
        self.cp.read(self.SETTINGS_FILE)
        return self.cp.get(self.SECTION_CREDENTIALS, self.SETTING_EMAIL)

    def getPassword(self):
        self.cp.read(self.SETTINGS_FILE)
        return self.cp.get(self.SECTION_CREDENTIALS, self.SETTING_PASSWORD)

    def getPhone(self):
        self.cp.read(self.SETTINGS_FILE)
        return self.cp.get(self.SECTION_CREDENTIALS, self.SETTING_PHONE)
