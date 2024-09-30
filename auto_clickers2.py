from ordinals import *
import math
import sys

class Clickers:
    def __init__(self):
        self.num_cookies = 0
        self.auto_clickers = dict()

    @staticmethod
    def split_limit_const(o):
        c = 0
        while o.is_successor:
            c += 1
            o = o.prev()
        return o,c
        
    def click(self, o):
        o,c = self.split_limit_const(o)
        if o in self.auto_clickers:
            self.auto_clickers[o] = max(c+1, self.auto_clickers[o])
        else:
            self.auto_clickers[o] = c+1

        if c < 200:
            mul = 2**c
        else:
            mul = math.inf

        if o.is_zero:
            self.num_cookies += mul
        else:
            self.click_on_limit(o,mul)

    def has_ordinal(self, o):
        o,c = self.split_limit_const(o)
        return self.auto_clickers.get(o, 0) > c

    def click_on_limit(self, o, mul):
        if o.is_zero:
            self.num_cookies += mul
            return
        o1 = o.monomials[-1]
        if o1.exponent == ordinal_one:
            if o1.coef == 1:
                prev = Ordinal(o.monomials[:-1])
            else:
                prev = Ordinal(o.monomials[:-1] + (OrdMonomial(o1.exponent, o1.coef-1),))
            c = self.auto_clickers.get(prev, 0)
            self.auto_clickers[prev] = c+mul
            if c+mul >= 200:
                next_mul = math.inf
            else:
                next_mul = 2**(c+mul) - 2**c
            self.click_on_limit(prev, next_mul)
        else:
            if mul > 10**6:
                raise Exception(f"Clicking on {o} over milion-times is not feasible")

            n = 0
            prev = None
            while True:
                if not self.has_ordinal(o.limit_n(n)):
                    break
                n += 1

            for _ in range(mul):
                self.click(o.limit_n(n))
                n += 1

    def display(self):
        print(clickers.num_cookies, "Cookies")
        for o,num in sorted(clickers.auto_clickers.items()):
            print(o, ':', num)

clickers = Clickers()
for _ in sys.stdin:
    clickers.click(s(w(w(1))))
    # clickers.click(s(w(1,2)))
    clickers.display()
