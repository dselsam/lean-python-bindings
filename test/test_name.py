from nose.tools import assert_equals, assert_not_equals, assert_false, assert_true
import lean

n0 = lean.name()
n1 = lean.name("hello")
n2 = lean.name(n1, "goodbye")
n3 = lean.name(n2, 5)

assert_equals(str(n3), "hello.goodbye.5")

d = {n3 : 4, n2 : 7}

assert_equals(d[n3], 4)

assert_equals(d[n2], 7)

assert_not_equals(n2, n3)

assert_equals(lean.name(n2, 5), n3)

def name_to_list(n):
    l = []
    while not n.is_anonymous():
        if n.is_string():
            l.insert(0, n.get_string())
        elif n.is_numeral():
            l.insert(0, n.get_numeral())
        n = n.get_prefix()
    return l

assert_equals(name_to_list(n3), ["hello", "goodbye", 5])

ln1 = lean.list_name()
ln2 = lean.list_name(lean.name("head-of-list"), ln1)
assert_equals(ln2.head(), lean.name("head-of-list"))
assert_true(ln2.tail().is_nil())
