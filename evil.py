def run_and_destroy(func):
    print("I'm going to kill you!")
    func()
    print("And now I kill you. Bye bye!")
    return None

@run_and_destroy
def hello_world():
    print("Hello, world!")

print("Now we try to run that...")
# hello_world()

def monkeypatch(cls):
    orig = globals()[cls.__name__]
    print("Monkeypatch",id(cls),"into",id(orig))
    for attr in dir(cls):
        if not attr.startswith("_"):
            setattr(orig,attr,getattr(cls,attr))
    return orig

class Foo:
    def method1(self):
        print("I am method 1")

print("Foo is currently",id(Foo))
some_object = Foo()

@monkeypatch
class Foo:
    def method2(self):
        print("I am method 2")

print("Foo is now",id(Foo))

some_object.method1()
some_object.method2()

