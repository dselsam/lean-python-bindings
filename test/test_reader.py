import lean
lean.initialize()

r1 = lean.reader("data_bools.out")

b1 = r1.read_bool()
b2 = r1.read_bool()
b3 = r1.read_bool()
b4 = r1.read_bool()

print(b1, b2, b3, b4)

r2 = lean.reader("data_infer_type.out")

infer_types = {}
while not r2.eof():
    e1 = r2.read_expr()
    e2 = r2.read_expr()
    print(e1, " ==> ", e2)
    infer_types[e1] = e2

print("read")

for e in infer_types:
    print(e, " ==> " , infer_types[e])

r3 = lean.reader("data_is_def_eq.out")
def_eqs = {}
while not r3.eof:
    e1 = r3.read_expr()
    e2 = r3.read_expr()
    b = r3.read_bool()
    b2 = r3.read_bool()
    print(e1, " =?= ", e2, " ==> ", b, b2)
    def_eqs[(e1, e2)] = b

print("read")

for (e1, e2) in def_eqs:
    print(e1, " =?= " , e2, " ==> ", def_eqs[(e1, e2)])
