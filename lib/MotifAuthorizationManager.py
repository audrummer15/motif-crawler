import subprocess
from StringIO import StringIO

import pycurl
from bs4 import BeautifulSoup

class MotifAuthorizationManager(object):
    URL_AUTH_STEP1 = "https://auth.motifinvesting.com/authenticate"
    URL_AUTH_STEP2 = "https://trader.motifinvesting.com/two-factor-auth?next=%2F5jt2aa7b%2Fhome"
    URL_AUTH_STEP3 = "https://trader.motifinvesting.com/two-factor-auth/send"
    URL_AUTH_STEP4 = "https://trader.motifinvesting.com/two-factor-auth/confirm"
    URL_SETTINGS = "https://trader.motifinvesting.com/account/settings"


    def __init__(self, username=None, password=None, phone=None, cookieJar="cookies.txt"):
        if username != None:
            if isinstance(username, str):
                self.username = username
            else:
                raise ValueError("MotifAuthorizationManager.__init__:  Username must be a string.")
        else:
            self.username = ""

        if password != None:
            if isinstance(password, str):
                self.password = password
            else:
                raise ValueError("MotifAuthorizationManager.__init__:  Password must be a string.")
        else:
            self.password = ""

        if phone != None:
            if isinstance(phone, str):
                self.phone = phone
            else:
                raise ValueError("MotifAuthorizationManager.__init__:  Phone must be a string.")
        else:
            self.phone = ""

        if cookieJar != "cookies.txt":
            if isinstance(cookieJar, str):
                self.cookieJar = cookieJar
            else:
                raise ValueError("MotifAuthorizationManager.__init__:  cookieJar must be a string.")
        else:
            self.cookieJar = cookieJar



    def setUsername(self, username=None):
        if username != None:
            if isinstance(username, str):
                self.username = username
            else:
                raise ValueError("MotifAuthorizationManager.setUsername:  Username must be a string.")
        else:
            raise ValueError("MotifAuthorizationManager.setUsername:  Username not optional.")



    def getUsername(self):
        return self.username



    def setPassword(self, password=None):
        if password != None:
            if isinstance(password, str):
                self.password = password
            else:
                raise ValueError("MotifAuthorizationManager.setPassword:  Password must be a string.")
        else:
            raise ValueError("MotifAuthorizationManager.setPassword:  Password not optional.")



    def setPhone(self, phone=None):
        if phone != None:
            if isinstance(phone, str):
                self.phone = phone
            else:
                raise ValueError("MotifAuthorizationManager.setPhone:  Phone must be a string.")
        else:
            raise ValueError("MotifAuthorizationManager.setPhone:  Phone not optional.")



    def getPhone(self):
        return self.phone



    def setCookieJar(self, cookieJar=None):
        if cookieJar != None:
            if isinstance(cookieJar, str):
                self.cookieJar = cookieJar
            else:
                raise ValueError("MotifAuthorizationManager.setCookieJar:  cookieJar must be a string.")
        else:
            raise ValueError("MotifAuthorizationManager.setCookieJar:  cookieJar not optional.")



    def getCookieJar(self):
        return self.cookieJar



    def _getNonceFromSoup(self, soup):
        scriptResults = soup('script',{'type' : 'text/javascript'})

        for line in scriptResults:
            for result in line.stripped_strings:
                result = result.split('\n')
                for tag in result:
                    if "nonce" in tag:
                        return tag.split("\"")[1].strip()



    def authorizeUser(self):
        ########### STEP 1 ############
        try:
            curlOut = subprocess.check_output(["curl",
                "-c", self.cookieJar,
                "-d", "email=" + self.username + "&password=" + self.password,
                self.URL_AUTH_STEP1])
        except Exception, e:
            raise ValueError("MotifAuthorizationManager.authorizeUser:  Step 1 Failed With \"" + str(e) + "\"" )

        ########### STEP 2 ###########
        nonce = None
        try:
            curlOut = subprocess.check_output(["curl",
                "-b", self.cookieJar,
                self.URL_AUTH_STEP2])

            soup = BeautifulSoup(curlOut, "html.parser")
            nonce = self._getNonceFromSoup(soup)
        except Exception, e:
            raise ValueError("MotifAuthorizationManager.authorizeUser:  Step 2 Failed With \"" + str(e) + "\"" )

        if nonce == None:
            raise ValueError("MotifAuthorizationManager.authorizeUser:  Failed to get Nonce" )

        ############ STEP 3 ############
        try:
            curlOut = subprocess.check_output(["curl",
                "-b", self.cookieJar,
                "-H", "X-Motif-Page: TWO_FACTOR_AUTH",
                "-H", "Origin: https://trader.motifinvesting.com",
                "-H", "X-Requested-With: XMLHttpRequest",
                "-H", "X-Motif-Nonce: " + nonce + "",
                "-H", "X-FirePHP-Version: 0.0.6",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
                "-e", "https://trader.motifinvesting.com/two-factor-auth?auth=1&next=%2Fhome",
                "--data-raw", "phoneNumber=" + self.phone + "&authType=text&Nonce=" + nonce + "&Page=TWO_FACTOR_AUTH",
                self.URL_AUTH_STEP3])
        except Exception, e:
            raise ValueError("MotifAuthorizationManager.authorizeUser:  Step 3 Failed With \"" + str(e) + "\"" )

        pin = str(input("Enter Authorization Pin: "))

        try:
            curlOut = subprocess.check_output(["curl",
                "-b", self.cookieJar, "-c", self.cookieJar,
                "-H", "X-Motif-Page: TWO_FACTOR_AUTH",
                "-H", "Origin: https://trader.motifinvesting.com",
                "-H", "X-Requested-With: XMLHttpRequest",
                "-H", "X-Motif-Nonce: " + nonce + "",
                "-H", "X-FirePHP-Version: 0.0.6",
                "-A", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36",
                "-e", "https://trader.motifinvesting.com/two-factor-auth?auth=1&next=%2Fhome",
                "--data-raw", "confirmCode=" + pin + "&Nonce=" + nonce + "&Page=TWO_FACTOR_AUTH",
                self.URL_AUTH_STEP4])
        except Exception, e:
            raise ValueError("MotifAuthorizationManager.authorizeUser:  Step 3 Failed With \"" + str(e) + "\"" )

    def isUserAuthorized(self):
        buf = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, self.URL_SETTINGS)
        c.setopt(pycurl.COOKIEJAR, self.cookieJar)
        c.setopt(pycurl.COOKIEFILE, self.cookieJar)
        c.setopt(pycurl.WRITEFUNCTION, buf.write)
        c.perform()

        statusCode = int(c.getinfo(pycurl.HTTP_CODE))
        c.close()

        if statusCode >= 200 and statusCode < 300:
            return True
        else:
            return False
