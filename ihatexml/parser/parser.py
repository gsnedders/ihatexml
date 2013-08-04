import ply.yacc as yacc

from . import ast
from .lexer import lexer, tokens


precedence = (
    ('left', 'QUESTION', 'PLUS', 'ASTERISK'),
    ('left', 'HYPHEN'),
)

def p_error(p):
    print("Parse error")
    while True:
        tok = yacc.token()
        if not tok or tok.type == 'NEWLINE':
            break
    yacc.restart()

def p_definition_list_base(p):
    'definitionList : definition'
    name, value = p[1]
    p[0] = ast.DefinitionDict([(name, value)])

def p_definition_list_recurse(p):
    'definitionList : definitionList NEWLINE definition'
    name, value = p[3]
    p[0] = p[1]
    p[0][name] = value

def p_definition(p):
    'definition : SYMBOL DEFINE expression'
    p[0] = (p[1], p[3])    

def p_expression_base(p):
    'expression : expressionFollows'
    p[0] = p[1]

def p_expression_alternation(p):
    'expression : expression BAR expressionFollows'
    if isinstance(p[1], ast.Alternation):
        p[0] = p[1]
    else:
        p[0] = ast.Alternation([p[1]])
    p[0].options.append(p[3])

def p_expression_follows_base(p):
    'expressionFollows : expressionPrimary'
    p[0] = p[1]

def p_expression_follows_recurse(p):
    'expressionFollows : expressionFollows expressionPrimary'
    if isinstance(p[1], ast.Follows):
        p[0] = p[1]
    else:
        p[0] = ast.Follows([p[1]])
    p[0].order.append(p[2])

def p_expression_list_wrapped(p):
    'expressionPrimary : LPAREN expression RPAREN'
    p[0] = p[2]

def p_expression_except(p):
    'expressionPrimary : expressionPrimary HYPHEN expressionPrimary'
    p[0] = ast.Difference(p[1], p[3])

def p_expression_repetition(p):
    '''expressionPrimary : expressionPrimary QUESTION
                  | expressionPrimary ASTERISK
                  | expressionPrimary PLUS'''
    if p[2] == '?':
        min, max = 0, 1
    elif p[2] == '*':
        min, max = 0, float('inf')
    elif p[2] == '+':
        min, max = 1, float('inf')
    else:
        assert False, "unreachable"

    p[0] = ast.Repetition(p[1], min, max)

def p_expression_symbol(p):
    'expressionPrimary : SYMBOL'
    p[0] = ast.SymbolRef(p[1])

def p_expression_literal(p):
    '''expressionPrimary : QUOTE_STRING
                  | DQUOTE_STRING
                  | ESCAPECHAR'''
    p[0] = ast.Literal(p[1])

def p_expression_charclass(p):
    '''expressionPrimary : LSQUARE char_class_list RSQUARE
                  | LSQUARE CARET char_class_list RSQUARE'''
    # Get the right offset
    if len(p) == 4:
        cclist = p[2]
        negated = False
    else:
        cclist = p[3]
        negated = True
    
    # Split up char_class_list
    ranges = []
    chars = set()
    for x in cclist:
        if isinstance(x, tuple):
            ranges.append(x)
        else:
            chars.add(x)
    p[0] = ast.CharClass(negated, chars, ranges)

def p_char_class_list(p):
    'char_class_list : char_class_list char_class'
    p[0] = p[1]
    p[0].append(p[2])

def p_char_class_list_base(p):
    '''char_class_list : HYPHEN
                       | char_class'''
    p[0] = [p[1]]

def p_char_class_char(p):
    '''char_class : CLASSCHAR
                  | ESCAPECHAR'''
    p[0] = p[1]

def p_char_class_range(p):
    '''char_class : ESCAPECHAR HYPHEN ESCAPECHAR
                  | CLASSCHAR HYPHEN CLASSCHAR'''
    p[0] = (p[1], p[3])

parser = yacc.yacc()


if __name__ == '__main__':
    try:
        input = raw_input
    except NameError:
        pass
    try:
        import readline
    except ImportError:
        pass
    while True:
        try:
            s = input('parser > ')
        except EOFError:
            print()
            break
        t = yacc.parse(s)
        if t:
            for k, v in t.items():
                print("%s ::= %s" % (k, v))
