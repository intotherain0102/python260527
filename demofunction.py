# demofunction.py

# 1 define function
def setValue(newValue):
    # local val
    x = newValue
    print("local value:", x)

retValue = setValue(5)
print(retValue)

print("========================================")

def swap(a,b):
    return b,a

retValue = swap(3,4)
print(retValue)

print("========================================")

x = 5

def func(a):
    return a+x

print(func(1))

def func2(a):
    x = 1
    return a+x

print(func2(1))


print("========================================")

# default value
def times(a=10, b=20):
    return a*b

print(times())
print(times(5))
print(times(5,6))

# keyword
def connectURI(server, port):
    strURL = "https://"+server+":"+port
    return strURL

print(connectURI("multi.com","80"))
print(connectURI(port="8080", server="naver.com"))

print("========================================")

# debug code
def union(*ar):
    result = []
    for item in ar:
        for x in item:
            if x not in result:
                result.append(x)
    return result

print(union("HAM","EGG"))
print(union("HAM","EGG","SPAM"))

print("========================================")

g = lambda x,y:x*y
print(g(3,4))
print(g(5,6))
print ( ( lambda x:x*x )(3) )
print( dir() )
print( globals() )
