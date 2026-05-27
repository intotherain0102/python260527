# class test.py

class Person:
    def __init__(self):
        self.name = "default name"
    def print(self):
        print("My Name is {0}".format(self.name))

# create instance p1
p1 = Person()
p1.print()

# create instance p2
p2 = Person()
p2.name = "Nice Guy"
p2.print()