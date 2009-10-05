from factor_graph import *

RV('x1',('H','L'))
RV('x2',('F','S'))
RV('x3',('H','L'))



table1 = {	('H',):0.5,
			('L',):0.5,
			}
table2 = {	('H','F'):0.9,
			('H','S'):0.1,
			('L','F'):0.1,
			('L','S'):0.9,
			}
table3 = {	('H','H'):0.9,
			('H','L'):0.1,
			('L','H'):0.1,
			('L','L'):0.9,
			}

CPT1 = CPT(['x1'],table1)
CPT2 = CPT(['x1','x2'],table2)
CPT3 = CPT(['x1','x3'],table3)


Gr = FactorGraph()
node(Gr,'x1')
node(Gr,'x2')
node(Gr,'x3')

factor(Gr,CPT1)
factor(Gr,CPT2)
factor(Gr,CPT3)


#CPT1.show()
#CPT2.show()
#CPT3.show()

#multiply(CPT([],{}),CPT3).show()
#multiply(CPT([],{}),CPT([],{})).show()

#evid = {'x3':'H'}
evid = {'x1':'H'}

G2 = sum_product(Gr,evidences=evid)



#for node in G2.nodes:
#	print node.prob.show()



