class Expression:
    def __init__(self):
        self.debug = None 
        self.op = None

    def parse(self, tokens):
        self.debug = list(tokens)+[(self.op)]
        self._parse(tokens)
        return

    def _parse(tokens):
        return

    def evaluate(self):
        try:
            return self._evaluate()
        except Exception as e:
            print(f"error in {reassemble_str(self.debug)}")
            raise e
    
    def _evaluate(self):
        return

class Print(Expression):
    def __init__(self):
        self.value = None
        self.op = "print"

    def _parse(self, tokens):
        self.value = parse(tokens)

    def _evaluate(self):
        t = self.value.evaluate()
        print(t)
        return t

class Integer(Expression):
    def __init__(self, integer):
        self.integer = integer
        self.op = "integer"

    def _evaluate(self):
        return self.integer

class Binary(Expression):
    def __init__(self, op):
        self.op = op
        self.l = None
        self.r = None

    def _parse(self, tokens):
        self.l = parse(tokens)
        self.r = parse(tokens)
 
class Add(Binary):
    def __init__(self):
        super().__init__("+")

    def _evaluate(self):
        return self.l.evaluate() + self.r.evaluate()

class Subtract(Binary):
    def __init__(self):
        super().__init__("-")

    def _evaluate(self):
        return self.l.evaluate() - self.r.evaluate()
   
class If(Expression):
    def __init__(self):
        self.op = "if"
        self.cond = None
        self.l = None
        self.r = None
    
    def _parse(self, tokens):
        self.cond = parse(tokens)
        self.l = parse(tokens)
        self.r = parse(tokens)
    
    def _evaluate(self):
        if self.cond.evaluate():
            return self.l.evaluate()
        else:
            return self.r.evaluate()

SymbolTable = dict()
Stack = list()

# todo: this is not an expression
class Define(Expression):
    def __init__(self):
        self.op = "define"
        self.stub = None
        self.function = None
        
    def _parse(self, tokens):
        self.stub = Stub()
        self.stub.parse(tokens)
        SymbolTable[self.stub.symbol] = (self.stub, None) 
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
        self.op = "reference"
        self.symbol = symbol
        self.arguments = dict()
    
    def _parse(self, tokens):
        if self.symbol not in SymbolTable:
            # shouldn't we throw an exception?
            return
        stub, _ = SymbolTable[self.symbol]
        for p in stub.parameters:
            self.arguments[p] = parse(tokens)

    def _evaluate(self):
        toEvaluate = None

        for s in Stack[::-1]:
            if self.symbol in s:
                toEvaluate = s[self.symbol]
                break

        if self.symbol in SymbolTable:
            _, toEvaluate = SymbolTable[self.symbol]

        if toEvaluate is None:
            raise Exception(f"symbol {self.symbol} not found")

        toPushOntoStack = dict()
        for key, value in self.arguments.items():
            toPushOntoStack[key] = value.evaluate()
        Stack.append(toPushOntoStack)
        if isinstance(toEvaluate, int):
            return toEvaluate
        r = toEvaluate.evaluate()
        Stack.pop()
        return r

def createExpression(op) -> Expression:
    if op == "+":
        return Add()
    elif op == "-":
        return Subtract()
    elif op == "if":
        return If()
    elif op == "define":
        return Define()
    elif op == "print":
        return Print()
    else:
        return Reference(op)

def reassemble_str(str):
    str.reverse()
    return " ".join(str)

def parse(tokens):
    if tokens[-1].isdigit():
        return Integer(int(tokens.pop()))

    l = tokens.pop()
    assert l == "(", f'"{l}" != "("'
    op = tokens.pop()
    e = createExpression(op)
    e.parse(tokens)
    r = tokens.pop()
    assert r == ")", f'"{r}" != ")" in string {reassemble_str(tokens + [r])}'

    return e

example = "( define ( countDown v ) ( if ( print ( v ) ) ( countDown ( - ( v ) 1 ) ) 0 ) ) ( countDown 10 )"
example1 = "( define ( hello a ) ( + 10 ( a ) ) ) ( print ( if 0 ( + ( + 32 8 ) ( + 12 ( + 3 ( + 7 8 ) ) ) ) ( hello 5 ) ) )"
example2 = "( print ( - 2 1 ) )"

tokens = example.split(" ")
tokens.reverse()
root = []
while tokens:
    root.append(parse(tokens))
for s in root:
    s.evaluate()
