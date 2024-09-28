import itertools

class OrdMonomial:
    def __init__(self, exponent, coef):
        assert isinstance(exponent, Ordinal)
        assert isinstance(coef, int)
        assert coef > 0
        self.exponent = exponent
        self.coef = coef

    def __eq__(self, other):
        return self.coef == other.coef and self.exponent == other.exponent
    def __hash__(self):
        return hash((self.coef, self.exponent))

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        if self.exponent.is_zero: return str(self.coef)
        exp = str(self.exponent)
        if self.exponent.needs_brackets_in_exp():
            exp = '('+exp+')'
        if self.exponent == ordinal_one:
            omega_exp = "ω"
        else:
            omega_exp = "ω^"+exp
        if self.coef == 1: return omega_exp
        else: return f"{omega_exp}*{self.coef}"

class Ordinal:
    def __init__(self, monomials):
        assert all(
            a.exponent > b.exponent
            for a,b in itertools.pairwise(monomials)
        )
        self.monomials = tuple(monomials)

    def __eq__(self, other):
        return self.monomials == other.monomials
    def __hash__(self):
        return hash(self.monomials)

    def cmp(self, other):
        i = 0
        while True:
            if i >= len(self.monomials) and i >= len(other.monomials): return 0
            if i >= len(other.monomials): return 1
            if i >= len(self.monomials): return -1
            mon1 = self.monomials[i]
            mon2 = other.monomials[i]
            if mon1.exponent > mon2.exponent: return 1
            if mon2.exponent > mon1.exponent: return -1
            if mon1.coef > mon2.coef: return 1
            if mon2.coef > mon1.coef: return -1
            i += 1
        return 0
    def __lt__(self, other):
        return self.cmp(other) < 0

    @property
    def is_zero(self):
        return not self.monomials
    @property
    def is_successor(self):
        return self.monomials and self.monomials[-1].exponent.is_zero
    @property
    def is_limit(self):
        return self.monomials and not self.monomials[-1].exponent.is_zero

    def prev(self):
        assert self.is_successor
        monomials = list(self.monomials)
        const = monomials.pop()
        if const.coef > 1:
            monomials.append(OrdMonomial(const.exponent, const.coef-1))
        return Ordinal(monomials)

    def limit_n(self, n):
        assert self.is_limit
        monomials = list(self.monomials)
        last = monomials.pop()
        if last.coef > 1:
            monomials.append(OrdMonomial(last.exponent, last.coef-1))
        exponent = last.exponent
        if exponent.is_successor:
            prev = exponent.prev()
            if n > 0:
                monomials.append(OrdMonomial(prev, n))
            return Ordinal(monomials)
        else:
            exponent2 = exponent.limit_n(n)
            monomials.append(OrdMonomial(exponent2, 1))
            return Ordinal(monomials)

    def limit_seq(self):
        n = 0
        while True:
            yield self.limit_n(n)
            n += 1

    def __repr__(self):
        return self.__str__()
    def __str__(self):
        if not self.monomials: return '0'
        return ' + '.join(map(str, self.monomials))
    def needs_brackets_in_exp(self):
        if not self.monomials: return False
        if len(self.monomials) > 1: return True
        [mon] = self.monomials
        if mon.exponent.is_zero: return False
        if mon.coef == 1: return False
        return True

def s(*args):
    monomials = []
    for arg in args:
        if isinstance(arg, OrdMonomial):
            monomials.append(arg)
        elif isinstance(arg, int):
            monomials.append(OrdMonomial(ordinal_zero, arg))
        else:
            raise Exception(f"Unexpected ordinal sum argument: {arg}")
    return Ordinal(monomials)

def w(exp, coef = 1):
    if isinstance(exp, int):
        exp = s(exp)
    elif isinstance(exp, OrdMonomial):
        exp = Ordinal([exp])
    assert isinstance(exp, Ordinal)
    return OrdMonomial(exp, coef)

ordinal_zero = Ordinal(())
ordinal_one = s(1)

if __name__ == "__main__":
    def check_ordinal(o):
        print()
        print(o)
        if o.is_zero: print("ZERO")
        elif o.is_successor: print(f"SUCC of {o.prev()}")
        else:
            assert o.is_limit
            print("LIMIT of", list(itertools.islice(o.limit_seq(), 6)), "...")
    check_ordinal(s(w(w(2)), w(w(1))))
