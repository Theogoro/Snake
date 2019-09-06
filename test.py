"""import random

lista = [
    {'f':random.randint(1,25)}
]
while True:
    print(lista)
    input()
    if len(lista) > 1:
        for i in range(len(lista)-1,1):
            print('Update')
            print(lista[i]['f'])
            lista[i]['f']=lista[-1]['f']
    lista.append({'f':0})
    lista[0]['f'] = random.randint(1,25)"""

"""f = [1,2,3,4,5]
for d in f[::-1]:
    print(d)"""

body = [
    {'d':1},
    {'d':2},
    {'d':3}
]
"""
copy = body

copy.pop()

copy.insert(0,{'Example':55})
print(body)
print(copy)
import random
me = [
    {'d':random.randint(1,10)},
    {'d':random.randint(1,10)},
    {'d':random.randint(1,10)},
    {'d':random.randint(1,10)},
    {'d':random.randint(1,10)}
]
print(me)
while True:
    if len(me) > 1:
        me.pop()
        me.insert(0,{'d':random.randint(1,10)})
        input()
        print(me)"""


Lista = [
    3,
    2,
    1
]

while True: 
    Lista.insert(0,Lista[0])
    Lista[0]+=1
    Lista.pop()
    print(Lista)
    input()
