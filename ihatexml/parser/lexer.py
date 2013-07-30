import ply.lex as lex

try:
    chr = unichr
except NameError:
    pass

__all__ = ["lexer", "tokens"]

tokens = ['DQUOTE_STRING', 'RSQUARE', 'PLUS', 'CARET', 'CLASSCHAR',
          'LSQUARE', 'BAR', 'LPAREN', 'ESCAPECHAR', 'ASTERISK',
          'COMMENT', 'HYPHEN', 'QUOTE_STRING', 'RPAREN', 'QUESTION', 'SYMBOL', 'DEFINE', 'NEWLINE']

states = (
    ('charclass', 'exclusive'),
)

def t_ANY_error(t):
    raise SyntaxError("Parse error, unexpected character '%s'" % t.value[0])

def t_WFC(t):
    r'\[[\x20\t]*[wW][fF][cC][\x20\t]*\:[^\]]+\]'
    pass

def t_VC(t):
    r'\[[\x20\t]*[vV][cC][\x20\t]*\:[^\]]+\]'
    pass

def t_INITIAL_charclass_ESCAPECHAR(t):
    r'\#x[0-9A-Fa-f]+'
    try:
        v = int(t.value[2:], 16)
    except ValueError:
        assert False, "Unreachable"
        raise
    try:
        c = chr(v)
    except ValueError:
        # XXX: handle narrow build case
        raise
    t.value = c
    return t

def t_LSQUARE(t):
    r'\['
    t.lexer.begin('charclass')
    return t

def t_charclass_RSQUARE(t):
    r'\]'
    t.lexer.begin('INITIAL')
    return t

def t_COMMENT(t):
    r'/\*(.|\n)*?\*/'
    pass

t_charclass_CLASSCHAR = r'([^\-\#\]]|\#(?!x))'
t_charclass_CARET = r'\^'
t_charclass_ignore = r''

t_INITIAL_charclass_HYPHEN = r'\-'

t_SYMBOL = r'[A-Za-z]+'
t_DEFINE = r'::='
t_DQUOTE_STRING = r'"[^"]*"'
t_QUOTE_STRING = r"'[^']*'"
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_QUESTION = r'\?'
t_BAR = r'\|'
t_PLUS = r'\+'
t_ASTERISK = r'\*'
t_NEWLINE = r'(\r?\n)+'

t_ignore = '\x20\t'

lexer = lex.lex()

if __name__ == '__main__':
    lex.runmain()
