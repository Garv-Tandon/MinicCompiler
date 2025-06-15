from compiler.lexer import tokenize
from compiler.parser import Parser
from compiler.semantic import SemanticAnalyzer
from compiler.icg import IntermediateCodeGenerator
from compiler.optimizer import Optimizer
from compiler.codegen import CodeGenerator

def main():
    code = """
    //Sum
    int x;
    int y;
    int z;
    x = 10;
    y = 20;
    z = x + y * 2;
    print z;"""
    # Main C code
    print("=== Source Code ===")
    print(code.strip())

    #Lexical Analysis
    tokens = tokenize(code)
    print("\n=== Tokens ===")
    for t in tokens:
        print(t)


    #Syntax Analysis
    parser = Parser(tokens)
    ast = parser.parse()
    if parser.errors:
        print("\nSyntax Errors Detected:")
        for e in parser.errors:
            print("Parsing Error:", e)
        print("Compilation halted due to syntax errors.")
        return

    print("\n=== AST ===")
    for node in ast:
        print(node)

    semantic = SemanticAnalyzer()
    semantic.analyze(ast)
    if semantic.errors:
        print("\nSemantic Errors Detected:")
        for e in semantic.errors:
            print("Semantic Error:", e)
        return
    #Symbol Table 
    semantic.symbols.display()

    # Intermediate Code
    icg = IntermediateCodeGenerator()
    ir = icg.generate(ast)
    print("\n=== Intermediate Code ===")
    for line in ir:
        print(line)

    # Code Optimization
    optimizer = Optimizer()
    optimized = optimizer.optimize(ir)
    print("\n=== Optimized Code ===")
    for line in optimized:
        print(line)

    #Code Generator
    codegen = CodeGenerator()
    assembly = codegen.generate(optimized)
    print("\n=== Assembly Code ===")
    for line in assembly:
        print(line)

if __name__ == '__main__':
    main()
