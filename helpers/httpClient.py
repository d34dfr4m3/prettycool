import requests
import random

httpStatusCodes = {
    "400": "Maximum value for parameter exceeded / invalid or missing required parameters.",
    "402": "Request limit exceeded",
    "403": "Missing or invalid required parameter api_token.",
    "500": "Internal server error. We are aware of the error and are already working on fixing it. Sorry for inconvenience."
}

userAgent = [
    "AppleWebKit/537.36 (KHTML, like Gecko)",
    "Links (2.2; FreeBSD 8.1-RELEASE i386; 196x84)",
    "Mozilla/5.0 (BlackBerry; U; BlackBerry 9900; en) AppleWebKit/534.11+ (KHTML, like Gecko) Version/7.1.0.346 Mobile Safari/534.11+",
    "Mozilla/4.0 (compatible; MSIE 7.0; America Online Browser 1.1; Windows NT 5.1; (R1 1.5); .NET CLR 2.0.50727; InfoPath.1)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows Phone OS 7.5; Trident/5.0; IEMobile/9.0)",
    "Mozilla/5.0 (Macintosh; U; PPC; en-US; mimic; rv:9.3.0) Gecko/20120117 Firefox/3.6.25 Classilla/CFM",
    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X Mach-O; en-US; rv:1.0.1) Gecko/20021216 Chimera/0.6",
    "Mozilla/5.0 (Linux; U; Android 4.0.3; ko-kr; LG-L160L Build/IML74K) AppleWebkit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30"
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/534.10 (KHTML, like Gecko) Chrome/8.0.552.224 Safari/534.10 ChromePlus/1.5.2.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
    "NokiaC7-00/SymbianOS/9.1 Series60/3.0 3gpp-gba",
    "Opera/12.02 (Android 4.1; Linux; Opera Mobi/ADR-1111101157; U; en-US) Presto/2.9.201 Version/12.02",
    "Opera/9.80 (X11; Linux i686; Ubuntu/14.10) Presto/2.12.388 Version/12.16",
]


# ToDo: Create mobile preference and concat with other UA lists
def UserAgentRandom(mobile=True):
    return "".join(random.sample(userAgent, 1))


methods = {
    "GET": requests.get,
    "POST": requests.post,
    "PATCH": requests.patch
}


def CreateHeaders():
    return {
        "User-Agent": UserAgentRandom(),
        "Referrer": "www.google.com"
    }


def Request(url, body=None, method="GET", isJson=False):
    response = methods.get(method)(url, headers=CreateHeaders(), body=body)
    if isJson:
        return {"data": response.json(), "response": response}
    return {"response": response, "data": response.content()}


def Get(url, isJson=False):
    return Request(url, body=None, isJson=isJson)


def Post(url, body, isJson=False):
    return Request(url, body=body, method="POST", isJson=isJson)
