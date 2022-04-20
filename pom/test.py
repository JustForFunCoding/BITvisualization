from tester import assertRaises

def makebold(fn):
    def wrapped(*args, **kwargs):
        return "<b>" + fn(*args,**kwargs) + "</b>"
    return wrapped

def makeitalic(fn):
    def wrapped(*args, **kwargs):
        return "<i>" + fn(*args, **kwargs) + "</i>"
    return wrapped

@makebold
def hello1():
    return "hello world"
assert hello1() == "<b>hello world</b>"

@makebold
@makeitalic
def hello2(x):
    return "hello world"+ x

assert hello2(x="a") == "<b><i>hello world</i></b>"
