# Global Var
strName = "Not Class Member"

class DemoString:
    def __init__(self):
        # Instance Local Var
        self.strName = "" 
    def set(self, msg):
        self.strName = msg
    def print(self):
        print(self.strName)

d = DemoString()
d.set("First Message")
d.print()
