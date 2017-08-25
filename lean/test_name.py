import lean

n0 = lean.name()
n1 = lean.name("hello")
n2 = lean.name(n1, "goodbye")
n3 = lean.name(n2, 5)

print("should be 'hello.goodbye.5':")
print(n3)

d = {n3 : 4, n2 : 7}

print("should be '4':")
print(d[n3])

print("should be '7':")
print(d[n2])

print("should be 'False':")
print(n2 == n3)

print("should be 'True':")
print(lean.name(n2, 5) == n3)

def name_to_list(n):
    l = []
    while not n.is_anonymous():
        if n.is_string():
            l.insert(0, n.get_string())
        elif n.is_numeral():
            l.insert(0, n.get_numeral())
        n = n.get_prefix()
    return l

print("should be '[hello, goodbye, 5]':")
print(name_to_list(n3))

ln1 = lean.list_name()
ln2 = lean.list_name(lean.name("head-of-list"), ln1)
print("should be 'head-of-list':")
print(ln2.head())
print("should be 'True':")
print(ln2.tail().is_nil())
