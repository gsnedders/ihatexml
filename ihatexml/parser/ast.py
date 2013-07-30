class Literal(object):
    __slots__ = ["value"]
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Repetition(object):
    __slots__ = ["expression", "min", "max"]
    def __init__(self, expression, min, max):
        self.expression = expression
        self.min = min
        self.max = max

class CharClass(object):
    __slots__ = ["negated", "chars", "ranges"]
    def __init__(self, negated, chars, ranges):
        self.negated = negated
        self.chars = chars
        self.ranges = ranges

class Alternation(object):
    __slots__ = ["options"]
    def __init__(self, options):
        self.options = options

    def __str__(self):
        return " | ".join(map(lambda x: "(%s)" % x, self.options))

class SymbolRef(object):
    __slots__ = ["symbol"]
    def __init__(self, symbol):
        self.symbol = symbol

    def __str__(self):
        return self.symbol

class Difference(object):
    __slots__ = ["base", "comparison"]
    def __init__(self, base, comparison):
        self.base = base
        self.comparison = comparison

    def __str__(self):
        return "%s - %s" % (self.base, self.comparison)

class Follows(object):
    __slots__ = ["order"]
    def __init__(self, order):
        self.order = order

    def __str__(self):
        assert len(self.order) > 1
        return " ".join(map(str, self.order))
