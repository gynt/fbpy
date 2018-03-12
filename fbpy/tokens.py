
import datetime
import random

class TokenManager(object):

    def __init__(self):
        self.tokens = self.fetch_tokens()
        self.tracker = {i: datetime.datetime.strptime("0", "%S") for i in self.tokens}
        self.index = 0
        self.current = None
        self.dirty=True

    def fetch_tokens(self):
        with open(".tokens.txt",'r') as f:
            return [line.replace("\r","") for line in f.read().split("\n") if line]

    def pick(self):
        now = datetime.datetime.now()
        available = [i for i in self.tokens if (self.tracker[i]-now).seconds > 60]
        if len(available) == 0:
            print("Out of tokens")
            c = [(self.tracker[i]-now).seconds for i in self.tokens]
            import time
            time.sleep(min(c))
            return self.pick()
            
        i = random.randrange(0, len(available))
        return self.tokens[i]

    def on_timeout(self):
        if not self.current:
            raise Exception
        self.tracker[self.current] = datetime.datetime.now()
        self.dirty=True

    def next_token(self):
        if not self.current:
            self.current = self.tokens[random.randrange(0, len(self.tokens))]
        else:
            self.current = self.pick()
        self.dirty=False

    def get_current_token(self):
        if self.dirty:
            self.current = self.next_token()
        return self.current
