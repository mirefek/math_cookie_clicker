import sys
from ordinals import *

class Clickers:
    def __init__(self):
        self.num_cookies = 0
        self.auto_clickers = set()

    def click(self, o):
        mul = 1
        if o not in self.auto_clickers:
            self.auto_clickers.add(o)
        while o.is_successor:
            o = o.prev()
            if o not in self.auto_clickers:
                self.auto_clickers.add(o)
            mul *= 2
        if o.is_zero:
            self.num_cookies += mul
        elif o.is_limit:
            for _ in range(mul):
                n = 0
                prev = None
                while True:
                    cur = o.limit_n(n)
                    if cur not in self.auto_clickers:
                        break
                    prev = cur
                    n += 1
                self.click(cur)

clickers = Clickers()
for _ in sys.stdin:
    # clickers.click(s(w(2)))
    clickers.click(s(w(1,2)))
    print(clickers.num_cookies, "Cookies")
    print("AutoClickers:", sorted(clickers.auto_clickers))
