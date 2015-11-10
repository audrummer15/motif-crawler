import os
import subprocess
import pycurl

from bs4 import BeautifulSoup
from bs4 import SoupStrainer

from lib.MotifAuthorizationManager import MotifAuthorizationManager
from lib.RequestHandler import RequestHandler

COOKIEJAR = "cookies.txt"

mam = MotifAuthorizationManager()
if not mam.isUserAuthorized():
    mam.setUsername(str(raw_input("Enter Motif Username: ")))
    mam.setPassword(str(raw_input("Enter Motif Password: ")))
    mam.setCookieJar(COOKIEJAR)
    mam.authorizeUser()
else:
    print "User Authorized"

rh = RequestHandler()
