#coding=utf-8
# <expression>  ::= <name> | <function> | <application>
# <function>    ::= lambda <name>.<body>
# where <body>  ::= <expression>
# <application> ::= (<function expression> <argument expression>)
# where
# <function expression> :: = <expression>
# <argument expression> :: = <expression>
# apply <=> beta reduction
# error eval  <=> alpha conversion
# alpha conversion <=> 解决命名冲突
# eta reduction <=> 化简 但不求值 
# ; eta conv ,eta reduction
# lambda a: ,args is (a,) a 是 该抽象函数的绑定变量( bound variable )
# 函数的参数 就是 bound variable 
# beta reduction 规约 Just 替换绑定变量
# cons <=> lambda a.lambda b.lambda func:( (func a)  b)
# func where :: car cdr
# car  <=> lambda a.lambda b.a
# cdr  <=> lambda a.lambda b.b
'Free and bound variables'
# lambda f.lambda s.(f (s s))
# bound variable f is in scope in lambda s.(f (s s))
# 绑定变量的范围

# Notations for naming functions and β reduction
# def <name> = <function>
# usage :
"""
def identity   = lambda x.x
def self_apply = lambda s.(s s)
def apply      = lambda func.lambda arg.(func arg)
"""
# (<name> <argument>) <=> (<function> <argument>)
# (<function> <argument>) => <expression>

class Error(Exception):pass
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

class Lambda(object):
    def __init__(self):
        # var == name
        self.privates = ['lambda','beta']
    def isName(self,exp):
        #return isinstance(exp,list) and isinstance(exp[0],str) and exp[0] not in self.privates
        return isinstance(exp,str) and exp not in self.privates

    def Name(self,exp,env):
        print 'isName',exp
        return env.get(exp)

    def isLambda(self,exp):
        return isinstance(exp,list) and exp[0] == 'lambda'

    def Lambda(self,exp,env):
        print 'isLambda'
        _,boundVars,body = exp
        print "Lambda:",boundVars,body,env
        #return body#[env.get(b) for b in body]
        return [_,boundVars,body]

    def isBeta(self,exp):
        return isinstance(exp,list) and exp[0] == 'beta'

    def Beta(self,exp,env):
        print 'isBeta',exp
        _,function,argument = exp
        #print self.eval(function,env)
        # not is lambda then calc it
        if self.isLambda(function):
            _,bound_v,body = function
            if argument in env.keys():
                temp = env.get(argument)
            else:
                temp = argument
            # 这里判断是不是绑定变量或自由变量 基于文本替换的形式... emmm
            tempStr = str(body)
            print bound_v,type(bound_v)
            #if isinstance(bound_v,str):
            try:
                tempStr = tempStr.replace(repr(bound_v),'{}') 
                #else:
                tempStr =  tempStr.format(temp)
                body    = eval(tempStr)
            except NameError:
                #tempStr = temp
                #body    = eval(tempStr)
                body     = temp
            if self.isBeta(body):
                return self.Beta(body,env)
            else:
                return body
        else:
            function = self.Beta(function,env)
            return self.Beta([_,function,argument],env)

    def eval(self,exp,env):
        print "eval:",exp,env
        return Match(exp) <= [
            [self.isName,lambda :self.Name(exp,env)],
            [self.isLambda,lambda:self.Lambda(exp,env)],
            [self.isBeta,lambda:self.Beta(exp,env)]]
        
if __name__ == '__main__':
    l = Lambda()
    e = {'a':"a"}
    r= l.eval(
        ['beta',['beta',['lambda','func',['lambda','arg',['beta','func','arg']]],['lambda','fn','fn']],'a'],
        #['beta',['lambda','func',['beta','func','a']],['lambda','x','x']],
        e
    )
    print r
    print e
