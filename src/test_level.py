import lean

lk1 = lean.level_kind.Zero
lk2 = lean.level_kind.Succ

print "should be 'False':"
print lk1 == lk2

print "should be 'True':"
print lk1 != lk2

l0 = lean.mk_level_zero()
l1 = lean.mk_level_one()
l2 = lean.mk_succ(l1)
l3 = lean.mk_param_univ(lean.name("hello"))
l4 = lean.mk_max(l2, l3)

print "should be 'True':"
print l4.is_max()

print "should be 'False':"
print l4.is_imax()

print "should be '2':"
print l4.max_lhs()

print "should be 'hello':"
print l4.max_rhs()


ln1 = lean.list_level()
ln2 = lean.list_level(lean.mk_param_univ(lean.name("head-of-list")), ln1)
print "should be 'head-of-list':"
print ln2.head()
print "should be 'True':"
print ln2.tail().is_nil()
