#coding=utf-8
class Match(object):
    # useage: Match(exp) <= [
    #                        [symbol?,lambda:xxx],]
    def __repr__(self):
        return "Case({})".format(self.expression)
    def __init__(self,expression):
        self.expression = expression
    def __le__(self,tup):
        #print tup
        for current,then in tup:
            #if self.expression == current:
            if current(self.expression):
                #return then(current)
                return then()

class AST(object):
    def __repr__(self):
        return "AST({})".format(self.name)
    def __init__(self,NodeName):
        self.name = NodeName

class AbstractAST(AST):
    name = "Lambda"
    def __repr__(self):
        return self.name+"({},{})".format(self.arg,self.body)
    def __init__(self,arg,body):
        self.arg = arg
        self.body = body
    def setBody(self,body):
        self.body = body

class SymbolAST(AST):
    name = "Symbol"#"Variable"
    def __repr__(self):
        return self.name+"({})".format(self.symbol)
    def __init__(self,VarName):
        self.symbol = VarName
    def setSym(self,symbol):
        self.symbol = symbol
class ApplyAST(AST):
    name = "Apply"
    def __repr__(self):
        return self.name+"({},{})".format(self.function,self.argument)
    def __init__(self,function,argument):
        # <name> <=> <function>
        # <args> <=> <argument>
        self.function = function
        self.argument = argument

def makeSym(char):
    return SymbolAST(char)

#symbolTable = {}

class Lambda(object):
    def __init__(self):
        for temp in 'abcdefghizklmnopqrstuvwxyz':
            setattr(self,temp,makeSym(temp))
    def parse2AST(self,src):
        # (lambda a.a)b
        id = AbstractAST(self.e,self.e)
        self_apply = AbstractAST(self.s,ApplyAST(self.s,self.s))
        apply      = AbstractAST(self.f,AbstractAST(self.a,ApplyAST(self.f,self.a)))
        #expression = ApplyAST(id,self.c)
        #expression = ApplyAST(ApplyAST(apply,id),id)
        #expression = ApplyAST(self_apply,id)
        return expression
    def eval(self,code):
        print 'eval:',code
        return Match(code) <= [
            (self.isSymbol,lambda:self.Symbol(code) ),
            (self.isAbsAST,lambda:self.AbsAST(code) ),
            (self.isAppAST,lambda:self.AppAST(code) ),
            ]
    def isSymbol(self,node):
        return isinstance(node,SymbolAST)
    def Symbol(self,node):
        return node
    def isAbsAST(self,node):
        return isinstance(node,AbstractAST)
    def AbsAST(self,node):
        return node#AbstractAST(node.arg,self.eval(node.body))
    def isAppAST(self,node):
        return isinstance(node,ApplyAST)
    def substitute(self,node,x,v):
        print node,x,v
        if self.isSymbol(node):
            # node.symbol 
            if node.symbol == x.symbol:
                return v
        elif self.isAppAST(node):
            node.function = self.substitute(node.function,x,v)
            node.argument = self.substitute(node.argument,x,v)
        elif self.isAbsAST(node):
            if node.arg == x:
                node.arg = self.substitute(node.arg,x,v)
            node.body = self.substitute(node.body,x,v)
        return node
    def beta_reduction(self,node):
        if self.isSymbol(node):
            return node
        elif self.isAbsAST(node):
            return node
        elif self.isAppAST(node):
            if self.isAbsAST(node.function):
                return self.substitute(node.function.body,
                                       node.function.arg,
                                       node.argument)
            else:
                temp = self.eval(node.function)
                print 'appAST:',temp
                print 'appAST:',node.function
                if temp != node.function:
                    node.function = temp
                    return node
                else:
                    node.argument = self.eval(node.argument)
                    return node
    def AppAST(self,node):
        temp = self.beta_reduction(node)
        while self.isAppAST(temp):
            temp = self.beta_reduction(temp)
        else:
            return temp


if __name__ == '__main__':
    l = Lambda()
    temp = l.parse2AST(233)
    print 'temp:',temp
    r    = l.eval(temp)
    print 'result:',r
    #print temp
    
