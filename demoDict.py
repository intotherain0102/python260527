# demoDict.py

# dictionary test
colors = {'apple':'red','banana':'yellow'}
print(len(colors))

# insert
colors['cherry']='red'

# modify
colors['apple'] = 'blue'
print(colors)

# delete
del colors['apple']

# for
for item in colors.items():
    print(item)

# select
print(colors['banana'])


print("=====================================")

