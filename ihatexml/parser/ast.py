class Node(object):
    def dfs(self):
        """Depth first-search from a node, preorder"""
        stack = [self]
        while stack:
            cur = stack.pop()
            yield cur
            if isinstance(cur, (CharClass, Literal, SymbolRef)):
                pass
            elif isinstance(cur, DefinitionDict):
                stack.extend(cur.values())
            elif isinstance(cur, Definition):
                stack.append(cur.name)
                stack.append(cur.value)
            elif isinstance(cur, Repetition):
                stack.append(cur.expression)
            elif isinstance(cur, Alternation):
                stack.extend(cur.options)
            elif isinstance(cur, Difference):
                stack.append(cur.base)
                stack.append(cur.comparison)
            elif isinstance(cur, Follows):
                stack.extend(cur.order)
            else:
                assert False, "Unknown node"

class DefinitionDict(dict):
    def is_acyclic(self, start_symbol):
        seen_symbols = set()
        to_check = [self[start_symbol]]
        while to_check:
            symbol = to_check.pop()
            seen_symbols.add(symbol)
            for n in symbol.dfs():
                if not isinstance(n, SymbolRef):
                    continue
                if n.name in seen_symbols:
                    return False
                seen_symbols.add(n.name)
                to_check.append(n)
        return True

        
class Definition(Node):
    __slots__ = ["name", "value"]
    def __init__(self, name, value):
        self.name = name
        self.value = value

class Literal(Node):
    __slots__ = ["value"]
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

class Repetition(Node):
    __slots__ = ["expression", "min", "max"]
    def __init__(self, expression, min, max):
        self.expression = expression
        self.min = min
        self.max = max

class CharClass(Node):
    __slots__ = ["negated", "chars", "ranges"]
    def __init__(self, negated, chars, ranges):
        self.negated = negated
        self.chars = chars
        self.ranges = ranges

class Alternation(Node):
    __slots__ = ["options"]
    def __init__(self, options):
        self.options = options

    def __str__(self):
        return "(%s)" % (" | ".join(map(lambda x: "(%s)" % x, self.options)))

class SymbolRef(Node):
    __slots__ = ["name"]
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

class Difference(Node):
    __slots__ = ["base", "comparison"]
    def __init__(self, base, comparison):
        self.base = base
        self.comparison = comparison

    def __str__(self):
        return "%s - %s" % (self.base, self.comparison)

class Follows(Node):
    __slots__ = ["order"]
    def __init__(self, order):
        self.order = order

    def __str__(self):
        assert len(self.order) > 1
        return " ".join(map(str, self.order))
