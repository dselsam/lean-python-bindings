import lean

n0 = lean.name()
n1 = lean.name("hello")
n2 = lean.name(n1, "goodbye")
n3 = lean.name(n2, 5)

print "should be 'hello.goodbye.5':"
print(n3.to_string())
print "should be: 'hello::goodbye::5'"
print(n3.to_string("::"))
