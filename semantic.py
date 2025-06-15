class SymbolTable:
    def __init__(self):
        self.symbols = {}

    def declare(self, name):
        self.symbols[name] = 'int'

    def exists(self, name):
        return name in self.symbols

    def display(self):
        print("\n=== Symbol Table ===")
        for name, type_ in self.symbols.items():
            print(f"{name}: {type_}")

class SemanticAnalyzer:
    def __init__(self):
        self.symbols = SymbolTable()
        self.errors = []

    def analyze(self, ast):
        for node in ast:
            if node[0] == 'declaration':
                self.symbols.declare(node[1])
            elif node[0] == 'assign':
                if not self.symbols.exists(node[1]):
                    self.errors.append(f"Undeclared variable {node[1]}")
            elif node[0] == 'print':
                if not self.symbols.exists(node[1]):
                    self.errors.append(f"Undeclared variable {node[1]}")
