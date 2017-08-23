import lean

bi1 = lean.binder_info()
bi2 = lean.mk_implicit_binder_info()

print "should be 'False':"
print bi1.is_implicit()

print "should be 'False':"
print bi2.is_inst_implicit()

print "should be 'True':"
print bi2.is_implicit()

b1 = lean.binder(lean.name("x"), lean.expr(), bi2)
print "should be 'x':"
print b1.get_name()

v1 = lean.mk_var(1)
v2 = lean.mk_var(2)

c_foo = lean.mk_constant(lean.name("foo"))
c_bar = lean.mk_constant(lean.name("bar"),
                         lean.list_level(lean.mk_level_one(),
                                         lean.list_level(lean.mk_level_zero(), lean.list_level())))

print "should be 'foo':"
print c_foo.const_name()

print "should be '[1, 0]':"
print c_bar.const_levels()

lam = lean.mk_lambda(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
print "should be 'fun (x : #1), (bar.{1 0} x)':"
print lam

pi = lean.mk_pi(lean.name("x"), v1, lean.mk_app(c_bar, lean.mk_var(0)))
print "should be 'Pi (x : #1), (bar.{1 0} x)':"
print pi
