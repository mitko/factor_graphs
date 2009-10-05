from utils import *

#CPT table 
#{(values):probability}
def table_function(cpttable):
	"""Creates a function that takes one parameter args
	which is a list of values and checks this in the cpttable"""
	if len(cpttable)==0:
#		print 'CAUTION ZERO FUNCTION',cpttable
		func = lambda args: 1
		return func
	else:
		num_params = len(cpttable.keys()[0])
#		print 'numparams ',num_params
		def func(args):
			if tuple(args) not in cpttable:
#				print 'notfound',tuple(args)
				return 0;
			else:
#				print 'found'
				return cpttable[tuple(args)]
		return func

# Random variables
rvs = {}
#'name':(list of values)

def RV(name,vals):
	# vals > 0
	if len(vals)>0:
		rvs[name]=tuple(vals)
	
	
def next_indices(inds,names):
	n = len(names)
	for i in range(n):
		if inds[-i]==len(rvs[names[-i]])-1:
			inds[-i]=0
		else:
			inds[-i] += 1
			break
	return inds
	
#CPT data structure
#[(list of k 'names'),function]
class CPT():	
	def __init__(self,rv_names,hashtable,function=None):
		self.names = tuple(rv_names)
		if function==None:
			self.prob = table_function(hashtable)
		else:
			self.prob = function
		
	def show(self):
		print self
		names = self.names
		for name in names:
			print name,'\t',
		print '|\t p'
		n = len(names)
		possibilities = product([len(rvs[name]) for name in names])
		indices = [ 0 for i in range(n)]
		for j in range(possibilities):
			values = [rvs[names[i]][indices[i]] for i in range(len(names))]
			for value in values:
				print value,'\t',
			print '|\t', self.prob(values)
			indices = next_indices(indices,names)
				
				

class FactorGraph():
	def __init__(self,nodes=[],factors=[]):
		self.nodes = nodes
		self.factors = factors
		
	def neib(self,entry):
		if isinstance(entry,Node):
			return filter(lambda x: entry.name in x.cpt.names, self.factors)			
		if isinstance(entry,Factor):	
			return entry.cpt.names
		return None
		
	def node_named(self,name):
		for node in self.nodes:
			if node.name == name:
				return node
		
			

class Factor():
	def __init__(self,cpt=None):
		self.cpt = cpt
		self.messages_from = {}
	
	def setCPT(self,cpt):
		self.cpt = cpt
	
	

class Node():
	#contains random variable
	def __init__(self,randv_name):
		self.name = randv_name
		self.messages_from = {}
		self.prob = None
		
def uniformCPT(names):
	unif = CPT(names,{})
	product = 1
	def cptprob(args):
		correct_args = True
		for i in range(len(args)):
			if args[i] not in rvs[names[i]]:
				correct_args = False
				break;
		if correct_args:
			return 1.0 
		else:
			return 0.0
	unif.prob = cptprob
	return unif


def multiply(cpt1,cpt2):
#	print cpt1.names
#	print cpt2.names	
#	if len(cpt1)==0 or len(cpt2.names)==0
			
	new_names = list( filter(lambda x: x in cpt2.names, cpt1.names ) )
	new_names2= list( filter(lambda x: x not in cpt2.names, cpt1.names) )
	new_names3= list( filter(lambda x: x not in cpt1.names, cpt2.names) )
	
#	print 'new_names ',new_names
#	print 'new_names2 ',new_names2
#	print 'new_names3 ',new_names3		
	names1 = cpt1.names
	names2 = cpt2.names
	
	prob1 = cpt1.prob
	prob2 = cpt2.prob	
				
	all_names =  new_names +new_names2 + new_names3
	
	def product_prob(args):
		args1 = [args[all_names.index(names1[i])] for i in range(len(names1))]
		args2 = [args[all_names.index(names2[i])] for i in range(len(names2))]			
				
		p1 = prob1(args1)
		p2 = prob2(args2)
		return p1*p2
	mult = CPT(all_names,{})
	mult.prob = product_prob
	return mult
	
	
def get_marginal(cpt,rv_name):

	names = cpt.names
	prob = cpt.prob
	
	if rv_name not in names:
		return cpt
	
	marg_names = filter(lambda x: x!=rv_name,names)
	position = names.index(rv_name)#+1 #TODO +1 is test
		
	def marg_prob(args):
		p_sum = 0.0
#		full_args = args[:position].append(None).extend(args[position:])
		full_args = args[:position] + ['.'] + args[position:]
		for value in rvs[rv_name]:
			full_args[position]=value
			p_sum += prob(full_args)
		return p_sum
	
	marg = CPT(marg_names,{})
	marg.prob = marg_prob
	return marg
	

# Creates the cpt table and records it
def cache_cpt(cpt):
	# To be used when the prob function of the cpt gets relatively complicated wrt to just having a CPT table. Also good for marginalizing.
	table = {}
	names = cpt.names
#	print 'namessss ',names
	possibilities = product([len(rvs[name]) for name in names])
	indices = [ 0 for i in range(len(names))]
	for j in range(possibilities+1):
		values = [rvs[names[i]][indices[i]] for i in range(len(names))]
		indices = next_indices(indices,names)
		table[tuple(values)]=cpt.prob(values)
	print 'cached table is:',table
	cached = CPT(names,table)
	print "cached: ",
	cached.show()
	return cached




#def sum_product_single_pass(name,G,evidences={}):
#	# assume the name is in the graph
#	P = CPT([],{})		# empty CPT
#	print 'evidences',evidences.keys()
#	for neim in evidences.keys():
#		#TODO for each corresponding factor, replace its cpt with evidences[name]
#		a = 1
#	for factor in G.neib(name):
#		P = multiply(P,collect_f(name,factor,G))
##	P = normalizeCPT(P) #TODO later
#	return P
		
			
debug = True
			
def collect_f(nodeN,factor,Gr):
	if debug: 
		print "COLLECT F:",nodeN,factor.cpt.names
	F = factor.cpt
#	if debug:
#		print "Initial...."
#		F.show()
	for noudN in Gr.neib(factor):
		if noudN != nodeN:
#			print 'multiplying ', F.names,factor.cpt.names, noudN, nodeN #for debug
			F = multiply(F,collect_g(factor,noudN,Gr))
	for noudN in Gr.neib(factor):
		if noudN != nodeN:
			F = cache_cpt(get_marginal(F,noudN))
	node = Gr.node_named(nodeN)
#	factor.messages_from[node]= F
	node.messages_from[factor]= F
	if debug:
#		print 'message ',nodeN,'->',factor.cpt.names
		print 'message ',factor.cpt.names,'->',nodeN
		F.show()
	return F


def collect_g(factor,nodeN,Gr):
	if debug: 
		print "COLLECT G:",factor.cpt.names,nodeN
	G = uniformCPT([nodeN])
	node = Gr.node_named(nodeN)
	for fct in Gr.neib(node):
		if fct != factor:
			G = cache_cpt(multiply(G,collect_f(nodeN,fct,Gr)))
	factor.messages_from[node]= G
#	node.messages_from[factor]= G	
	if debug:
		print 'message ',nodeN,'->',factor.cpt.names
		G.show()
#		print 'message ',factor.cpt.names,'->',nodeN
	return G
	
	

def distribute_f(nodeN,factor,Gr):
	if debug: 
		print "DISTRIBUTE F:",nodeN,factor.cpt.names
	G = factor.cpt
	node = Gr.node_named(nodeN)
#	print 'msgs::',node.messages_from, node.name
	for fctr in Gr.neib(node):
		if fctr != factor:
#			print factor.cpt.show()
#			print fctr.cpt.show()
			#TODO check if this is correct			
			G = multiply(G,node.messages_from[fctr])
#			G = multiply(G,fctr.messages_from[node])
	factor.messages_from[node]=G
	if debug:
		print 'message ',nodeN,'->',factor.cpt.names
		G.show()
	for noudN in Gr.neib(factor):
		if noudN != nodeN:
			distribute_g(factor,noudN,Gr)
	
	
	
def distribute_g(factor,nodeN,Gr):
	if debug: 
		print "DISTRIBUTE G:",factor.cpt.names,nodeN
	F = uniformCPT([nodeN])
	node = Gr.node_named(nodeN)
	for noudN in Gr.neib(factor):
		if noudN != nodeN:
			F = multiply(F,factor.messages_from[Gr.node_named(noudN)])
#			F = multiply(F,node.messages_from[factor])
	for noudN in Gr.neib(factor):
		if noudN != nodeN:
#			print 'abaN,babaN:',noudN,nodeN
			F = cache_cpt(get_marginal(F,noudN))
	node.messages_from[factor]=F
	if debug:
		print 'message ',factor.cpt.names,'->',nodeN
		F.show()
	for fctr in Gr.neib(node):
		if fctr != factor:
			distribute_f(nodeN,fctr,Gr)

def set_var_val(evar,val,Gr):
	for fctr in Gr.neib(Gr.node_named(evar)):
		old_fun = cache_cpt(fctr.cpt).prob
		var_index = fctr.cpt.names.index(evar)
		def new_fun(args):
			az = 1
			if val == args[var_index]:
				az = old_fun(args)
			else:
				az = 0
			return az
		new_CPT = CPT(fctr.cpt.names,{})
		new_CPT.prob = new_fun
		new_CPT = cache_cpt(new_CPT)
		fctr.setCPT(new_CPT)

			
def sum_product(Gr,evidences={}):
	#TODO for evidences ....
	print 'evidences',evidences.keys(),[evidences[k] for k in evidences.keys()]
	for evar in evidences.keys():
		set_var_val(evar,evidences[evar],Gr)
		[zyb.cpt.show() for zyb in Gr.neib(Gr.node_named(evar))]
	for root_node in Gr.nodes:
		print 'root_name',root_node.name
		if root_node.name not in evidences.keys():
			break
#	root_node = Gr.nodes[0]	#picks a root node
	for fctr in Gr.neib(root_node):
		collect_f(root_node.name,fctr,Gr)
	for fctr in Gr.neib(root_node):
		distribute_f(root_node.name,fctr,Gr)	
	for node in Gr.nodes:
		node.prob = CPT([],{})
		print 'msssgs ',node.messages_from, node.name
		for factor in Gr.neib(node):
##			node.prob = multiply(node.prob,factor.messages_from[node])
			node.prob = multiply(node.prob,node.messages_from[factor])
	for node in Gr.nodes:
		print '----------------'
		print node.prob.show()
	return Gr
	

		
		
def node(G,name):
	G.nodes.append(Node(name))
def factor(G,cpt):
	G.factors.append(Factor(cpt))	
			

