# 반복구문.py

# while
value = 5
while value > 0:
    print(value)
    value = value -1

print("====================================")

for i in [1,2,3]:
    print(i)

print("====================================")

# dictionary
d = {'name':"jay", 'age':30, "addr":"선릉"}
for item in d.items():
    print(item)

print("====================================")

print( list(range(2000,2027)) )
print( list(range(1,32)) )
print( list(range(1,11,2)) )

for i in range(5):
    print(i)

print("====================================")

lst = [1,2,3,4,5,6,7,8,9,10]
print( [i**2 for i in lst if i > 5] )
tp = ('apple','kiwi')
print( [len(i) for i in tp] )
d = {100:'apple', 200:'kiwi'}
print( [v.upper() for v in d.values()] )

print("[filter]====================================")
lst = [10,25,30]
itemL = filter(None, lst)
for item in itemL:
    print(item)

print("[filter]====================================")
def getBiggerThan20(i):
    return i>20

lst = [10,25,30]
itemL = filter(getBiggerThan20, lst)
for item in itemL:
    print(item)

print("[lambda]====================================")    
itemL = filter(lambda x:x>20, lst)
for item in itemL:
    print(item)