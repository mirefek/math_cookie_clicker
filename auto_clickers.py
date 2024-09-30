import sys
from ordinals import *

class Clickers:
    def __init__(self):
        self.num_cookies = 0
        self.auto_clickers = set()

    def click(self, o):
        if o not in self.auto_clickers:
            self.auto_clickers.add(o)
        if o.is_successor:
            prev = o.prev()
            self.click(prev)
            self.click(prev)
        if o.is_zero:
            self.num_cookies += 1
        elif o.is_limit:
            n = 0
            prev = None
            while True:
                cur = o.limit_n(n)
                if cur not in self.auto_clickers:
                    break
                prev = cur
                n += 1
            self.click(cur)

    def display(self):
        print(clickers.num_cookies, "Cookies")
        print("AutoClickers:", sorted(clickers.auto_clickers))

clickers = Clickers()
for _ in sys.stdin:
    clickers.click(s(w(2)))
    # clickers.click(s(w(1,2)))
    clickers.display()
