class A(object):
    def __init__(slef,name=None,models=None):
        slef.name = name
        slef.models = models or "default"

    def function(slef):
        print(slef.name)
        print(slef.models )

class B(A):
    def __init__(slef):
        #A.__init__(slef)
        super(B,slef).__init__()
        slef.models = "modify"

if __name__ == "__main__":
    a = A()
    a = a.function()

    b = B()
    b.function()