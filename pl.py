class Expression:
    def parse(self, tokens):
        return

    def evaluate(self):
        return

class Integer(Expression):
    def __init__(self, integer):
        self.integer = integer

    def evaluate(self):
        return self.integer

class Binary(Expression):
    def __init__(self, op):
        self.op = op
        self.l = None
        self.r = None

    def parse(self, tokens):
        self.l = parse(tokens)
        self.r = parse(tokens)

class Add(Binary):
    def __init__(self):
        super().__init__("+")

    def evaluate(self):
        return self.l.evaluate() + self.r.evaluate()
    
class If(Expression):
    def __init__(self):
        self.cond = None
        self.l = None
        self.r = None
    
    def parse(self, tokens):
        self.cond = parse(tokens)
        self.l = parse(tokens)
        self.r = parse(tokens)
    
    def evaluate(self):
        if self.cond.evaluate():
            return self.l.evaluate()
        else:
            return self.r.evaluate()

SymbolTable = dict()

# todo: this is not an expression
class Define(Expression):
    def __init__(self):
        self.stub = None
        self.function = None
        
    def parse(self, tokens):
        self.stub = Stub()
        self.stub.parse(tokens)
        self.function = parse(tokens)

        SymbolTable[self.stub.symbol] = self.function

class Stub():
    def __init__(self):
        self.symbol = None
        self.parameters = []
    
    def parse(self, tokens):
        l = tokens.pop()
        assert l == "(", f'"{l}" != "("'
        self.symbol = tokens.pop()
        next = None
        while True:
            next = tokens.pop()
            if next == ")":
                break
            self.parameters.append(next)
        assert next == ")", f'"{next}" != ")"'

def createExpression(op) -> Expression:
    if op == "+":
        return Add()
    elif op == "if":
        return If()
    elif op == "define":
        return Define()
    else:
        raise Exception(f"{op} op does not exist")

def parse(tokens):
    if tokens[-1].isdigit():
        return Integer(int(tokens.pop()))

    if tokens[-1] in SymbolTable:
        return SymbolTable[tokens.pop()]

    l = tokens.pop()
    assert l == "(", f'"{l}" != "("'
    op = tokens.pop()
    e = createExpression(op)
    e.parse(tokens)
    r = tokens.pop()
    assert r == ")", f'"{r}" != ")"'

    return e

i = "( define ( hello ) 10 ) ( if 0 ( + ( + 32 8 ) ( + 12 ( + 3 ( + 7 8 ) ) ) ) hello )"

tokens = i.split(" ")
tokens.reverse()
root = []
while tokens:
    root.append(parse(tokens))
for s in root:
    print(f"{i} == {s.evaluate()}")
