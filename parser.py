class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.errors = []

    def current(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ('EOF', '')

    def eat(self, token_type):
        if self.current()[0] == token_type:
            self.pos += 1
        else:
            self.errors.append(f"Expected {token_type} but got {self.current()}")

    def parse(self):
        statements = []
        while self.pos < len(self.tokens):
            token = self.current()
            if token[0] == 'TYPE':
                statements.append(self.declaration())
            elif token[0] == 'ID' and token[1] == 'print':
                statements.append(self.print_stmt())
            elif token[0] == 'ID':
                statements.append(self.assignment())
            else:
                self.errors.append(f"Unexpected token {token}")
                self.pos += 1
        return statements

    def declaration(self):
        self.eat('TYPE')
        id_token = self.current()
        self.eat('ID')
        self.eat('END')
        return ('declaration', id_token[1])

    def assignment(self):
        id_token = self.current()
        self.eat('ID')
        self.eat('ASSIGN')
        expr = self.expr()
        self.eat('END')
        return ('assign', id_token[1], expr)

    def print_stmt(self):
        self.eat('ID')  # 'print'
        id_token = self.current()
        self.eat('ID')
        self.eat('END')
        return ('print', id_token[1])

    def expr(self):
        node = self.term()
        while self.current()[0] in ('PLUS', 'MINUS'):
            op = self.current()
            self.eat(op[0])
            node = ('binop', op[1], node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.current()[0] in ('TIMES', 'DIVIDE'):
            op = self.current()
            self.eat(op[0])
            node = ('binop', op[1], node, self.factor())
        return node

    def factor(self):
        token = self.current()
        if token[0] == 'NUMBER':
            self.eat('NUMBER')
            return ('num', int(token[1]))
        elif token[0] == 'ID':
            self.eat('ID')
            return ('var', token[1])
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.expr()
            self.eat('RPAREN')
            return node
        else:
            self.errors.append(f"Unexpected token {token}")
            self.pos += 1
            return ('error', token)
