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
        self.debug = None 

    def parse(self, tokens):
        self.debug = list(tokens)+[(self.op)]
        self.l = parse(tokens)
        self.r = parse(tokens)
 
class Add(Binary):
    def __init__(self):
        super().__init__("+")

    def evaluate(self):
        try:
            return self.l.evaluate() + self.r.evaluate()
        except Exception as e:
            print(f"error in {self.debug}")
            raise e
    
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
Stack = list()

# todo: this is not an expression
class Define(Expression):
    def __init__(self):
        self.stub = None
        self.function = None
        
    def parse(self, tokens):
        self.stub = Stub()
        self.stub.parse(tokens)
        self.function = parse(tokens)

        SymbolTable[self.stub.symbol] = (self.stub, self.function)

class Stub():
    def __init__(self):
        self.symbol = None
        self.parameters = list()
    
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

class Reference(Expression):
    def __init__(self, symbol):
        self.symbol = symbol
        self.arguments = dict()
    
    def parse(self, tokens):
        if self.symbol not in SymbolTable:
            # shouldn't we throw an exception?
            return
        stub, _ = SymbolTable[self.symbol]
        for p in stub.parameters:
            self.arguments[p] = parse(tokens)

    def evaluate(self):
        for key, value in self.arguments.items():
            self.arguments[key] = value.evaluate()
        
        toEvaluate = None

        for s in Stack[::-1]:
            if self.symbol in s:
                toEvaluate = s[self.symbol]

        if self.symbol in SymbolTable:
            _, toEvaluate = SymbolTable[self.symbol]

        if toEvaluate is None:
            raise Exception(f"symbol {self.symbol} not found")

        Stack.append(self.arguments)
        if isinstance(toEvaluate, int):
            return toEvaluate
        return toEvaluate.evaluate()

def createExpression(op) -> Expression:
    if op == "+":
        return Add()
    elif op == "if":
        return If()
    elif op == "define":
        return Define()
    else:
        return Reference(op)

def parse(tokens):
    if tokens[-1].isdigit():
        return Integer(int(tokens.pop()))

    l = tokens.pop()
    assert l == "(", f'"{l}" != "("'
    op = tokens.pop()
    e = createExpression(op)
    e.parse(tokens)
    r = tokens.pop()
    assert r == ")", f'"{r}" != ")" in string {tokens.append(r)}'

    return e

i = "( define ( hello a ) ( + 10 ( a ) ) ) ( if 0 ( + ( + 32 8 ) ( + 12 ( + 3 ( + 7 8 ) ) ) ) ( hello 5 ) )"

tokens = i.split(" ")
tokens.reverse()
root = []
while tokens:
    root.append(parse(tokens))
for s in root:
    print(f"{i} == {s.evaluate()}")
