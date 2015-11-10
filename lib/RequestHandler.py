import pycurl
from StringIO import StringIO

class RequestHandler(object):
    USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.80 Safari/537.36"

    def __init__(self):
        self.stringbuf = StringIO()
        self.c = pycurl.Curl()
        self.c.setopt(pycurl.VERBOSE, 0) # don't show request info
        self.c.setopt(pycurl.COOKIEJAR, "cookies.txt")
        self.c.setopt(pycurl.COOKIEFILE, "cookies.txt")
        self.c.setopt(pycurl.ENCODING, 'gzip,deflate')
        self.c.setopt(pycurl.USERAGENT, self.USER_AGENT)
        self.c.setopt(pycurl.CONNECTTIMEOUT, 5)
        self.c.setopt(pycurl.TIMEOUT, 5)

    def __curl_callback(self, buf):
        self.stringbuf.write(buf)

    def gethtml(self, url, headers=None):
        self.c.setopt(pycurl.URL , url)
        self.c.setopt(pycurl.WRITEFUNCTION, self.__curl_callback)
        self.c.setopt(pycurl.HEADERFUNCTION, self.__curl_callback)
        self.c.perform()

        statusCode = int(self.c.getinfo(pycurl.HTTP_CODE))
        self.c.close()

        return [statusCode, self.stringbuf.getvalue()]
