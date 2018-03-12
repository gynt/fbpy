import json
from fbpy.tokens import TokenManager
import urllib
import urllib.request as R
import urllib.error as E

class Result(object):

    def __init__(self, code, content):
        self.code=code
        self.content=content

class AccessManager(object):

    def __init__(self):
        self.token_manager = TokenManager()
        self.token_manager.next_token()

    def build_url(self, url):
        nurl = url
        try:
            if nurl[-1]!="?" and nurl[-1]!="&":
                if "?" in nurl:
                    nurl+="&"
                else:
                    nurl+="?"
            nurl += "access_token=" + self.token_manager.get_current_token()
        except Exception as e:
            if "Out of tokens" in e.args:
                return Result(400, {})
        return nurl

    def make_request(self, url):
        nurl = self.build_url(url)

        conn = None
        error = None
        
        try:
            conn = R.urlopen(nurl)
            return Result(200, json.loads(conn.read()))
        except E.HTTPError as e:
            # Return code error (e.g. 404, 501, ...)
            # ...
            error = e
        except E.URLError as e:
            # Not an HTTP-specific error (e.g. connection refused)
            # ...
            raise e

        if error.code == 400:            
            error = json.loads(error.read())
            if error["error"]["code"] <= 341:
                print(error)
                self.token_manager.on_timeout()
                #Try again
                return self.make_request(url)
            else:
                raise Exception(json.dumps(error))
        else:
            error = json.loads(error.read())
            if error["error"]["code"] <= 341:
                print(error)
                self.token_manager.on_timeout()
                #Try again
                return self.make_request(url)
            else:
                raise Exception(json.dumps(error))

