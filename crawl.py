import os
import subprocess
import pycurl

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from lib.MotifAuthorizationManager import MotifAuthorizationManager
from lib.RequestHandler import RequestHandler
from lib.SettingsManager import SettingsManager

COOKIEJAR = os.path.join("build", "cookie.txt")

sm = SettingsManager()
mam = MotifAuthorizationManager(sm.getEmail(), sm.getPassword(), COOKIEJAR)
if not mam.isUserAuthorized():
    mam.authorizeUser()
else:
    print "User Authorized"

rh = RequestHandler()
