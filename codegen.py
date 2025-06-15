class CodeGenerator:
    def generate(self, ir):
        return [f"ASM: {line}" for line in ir]