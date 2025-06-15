class IntermediateCodeGenerator:
    def __init__(self):
        self.temp_count = 0
        self.code = []

    def new_temp(self):
        self.temp_count += 1
        return f"t{self.temp_count}"

    def generate(self, ast):
        for node in ast:
            if node[0] == 'assign':
                result = self.gen_expr(node[2])
                self.code.append(f"{node[1]} = {result}")
            elif node[0] == 'print':
                self.code.append(f"print {node[1]}")
        return self.code

    def gen_expr(self, node):
        if node[0] == 'num':
            return str(node[1])
        elif node[0] == 'var':
            return node[1]
        elif node[0] == 'binop':
            left = self.gen_expr(node[2])
            right = self.gen_expr(node[3])
            temp = self.new_temp()
            self.code.append(f"{temp} = {left} {node[1]} {right}")
            return temp