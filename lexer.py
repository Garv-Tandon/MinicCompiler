import re

# Token specification
token_specification = [
    ('MULTILINE_COMMENT', r'/\*[\s\S]*?\*/'),       # Multi-line comments (non-greedy)
    ('COMMENT',           r'//.*'),                 # Single-line comments
    ('TYPE',              r'\bint\b|\bfloat\b|\bchar\b'),  # Data types
    ('ID',                r'[A-Za-z_][A-Za-z0-9_]*'),      # Identifiers
    ('NUMBER',            r'\d+'),                         # Numbers
    ('ASSIGN',            r'='),                           # Assignment
    ('END',               r';'),                           # Semicolon
    ('LPAREN',            r'\('),                          # Left parenthesis
    ('RPAREN',            r'\)'),                          # Right parenthesis
    ('COMMA',             r','),                           # Comma
    ('STRING',            r'"[^"\n]*"'),                   # String literals
    ('PLUS',              r'\+'),                          # Addition
    ('MINUS',             r'-'),                           # Subtraction
    ('TIMES',             r'\*'),                          # Multiplication
    ('DIVIDE',            r'/'),                           # Division
    ('SKIP',              r'[ \t]+'),                      # Whitespace
    ('NEWLINE',           r'\n'),                          # Newline
    ('MISMATCH',          r'.'),                           # Any other character
]

# Combine into one big pattern
token_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specification)

def tokenize(code):
    tokens = []
    line_num = 1
    line_start = 0

    for mo in re.finditer(token_regex, code):
        kind = mo.lastgroup
        value = mo.group()
        column = mo.start() - line_start

        if kind in {'COMMENT', 'MULTILINE_COMMENT', 'SKIP'}:
            continue  # Ignore comments and spaces
        elif kind == 'NEWLINE':
            line_num += 1
            line_start = mo.end()
        elif kind in {'TYPE', 'ID', 'NUMBER', 'ASSIGN', 'END', 'LPAREN', 'RPAREN',
                      'COMMA', 'STRING', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE'}:
            tokens.append((kind, value))
        elif kind == 'MISMATCH':
            raise SyntaxError(f'Unexpected character {value!r} at line {line_num}, column {column}')
    
    return tokens
