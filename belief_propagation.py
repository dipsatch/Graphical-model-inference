import networkx as nx

# returns node potential of adjacent nodes
def phi(xi,xj):		
	return 0.95 if xi==xj else 0.05
	
# returns node potential of the a single node
def phi_node(node,xi):
	if int(node)==1:
		return 0.95 if xi==1 else 0.05
	else:
		return 1.0

# Algorithm driver
def sum_product(evidence,root,find):
	f=root
	for e in list(dg.successors(str(f))):
		collect(int(f),int(e))
	for e in list(dg.successors(str(f))):
		distribute(int(f),int(e))
	sol=compute_marginal(root,find)
	print(round(sol,5), "\n")

# collecting messages from leaf nodes to root
def collect(i,j):
	for k in list(dg.successors(str(j))) + list(dg.predecessors(str(j))):
		if int(k)!=i:
			collect(int(j),int(k))
	send_message(int(j),int(i))

# distributing messages from root to leaf nodes
def distribute(i,j):
	send_message(int(i),int(j))
	for k in  list(dg.successors(str(j))) + list(dg.predecessors(str(j))):
		if int(k)!=i:
			distribute(int(j),int(k))

''' sending messages considering cases:
1. both nodes are evidence nodes
2. only the sender is an evidence node
3. only the receiver is an evidence node
4. none of the nodes are evidence nodes
'''
def send_message(j,i):

	if j in evidence:
		if i in evidence:
			res=phi(evidence[i],evidence[j])*phi_node(j,evidence[j])
			for k in list(dg.successors(str(j))) + list(dg.predecessors(str(j))) :
				if int(k) != int(i):
					prod=(m[str(k)+ "," + str(j)][evidence[j]])
					res*=prod
			if (str(j)+ "," + str(i)) not in m:
				m[str(j) + "," + str(i)]={}
			m[str(j)+ "," + str(i)][evidence[i]]=res
			
		else:
			for ix in [0,1]:
				res=phi(ix,evidence[j])*phi_node(j,evidence[j])
				for k in list(dg.successors(str(j))) + list(dg.predecessors(str(j))):
					if int(k) != int(i):
						prod=(m[str(k)+ "," + str(j)][evidence[j]])
						res*=prod
				if (str(j)+ "," + str(i)) not in m:
					m[str(j) + "," + str(i)]={}
				m[str(j)+ "," + str(i)][ix]=res
	else:
		if i in evidence:
			res=0.0
			for ij in [0,1]:
				res1=phi(evidence[i],ij)*phi_node(j,ij)
				for k in list(dg.successors(str(j))) + list(dg.predecessors(str(j))):
					if int(k) != int(i):
						prod=(m[str(k)+ "," + str(j)][ij])
						res1*=prod
				res+=res1
			if (str(j)+ "," + str(i)) not in m:
				m[str(j)+ "," + str(i)]={}
			m[str(j) + "," + str(i)][evidence[i]]=res
		else:
			for ix in [0,1]:
				res=0.0
				for ij in [0,1]:
					res1=phi(ix,ij)*phi_node(j,ij)
					for k in list(dg.successors(str(j))) + list(dg.predecessors(str(j))):
						if int(k) != int(i):
							prod=(m[str(k)+ "," + str(j)][ij])
							res1*=prod
					
					res+=res1
				if (str(j)+ "," + str(i)) not in m:
					m[str(j)+ "," + str(i)]={}
				m[str(j) + "," + str(i)][ix]=res

# Calculating probability
def compute_marginal(root,find):
	node=find[0]
	val=find[1]
	res=phi_node(node,val)
	denom=0.0
	for j in list(dg.predecessors(str(node))) + list(dg.successors(str(node)))  :
		res*=m[str(j)+ "," + str(node)][val]
	for i in [0,1]:
		prod=phi_node(node,i)
		for j in list(dg.predecessors(str(node))) + list(dg.successors(str(node)))  :
			prod*=m[str(j)+ "," + str(node)][i]
		denom+=prod
	return res/denom

#creating a chain graph	
def chain_graph(n):
	chain=nx.DiGraph()
	for i in range(1,n):
		chain.add_edge(str(i),str(i+1))
	return chain

# creating a tree
def trees(l,n):
	tree=nx.DiGraph()
	i=1
	while ((2*i)+1)<=n:
		tree.add_edge(str(i),str(2*i))
		tree.add_edge(str(i),str((2*i)+1))
		i+=1
	return tree

# main driver function
if __name__=='__main__':
	

	print('-------------------------------------')
	print('CHAIN')
	print('-------------------------------------')
	# creating chain graph for 15 nodes
	dg=chain_graph(15)
	root=1
	m={}
	print('P(X5=1)=', end=" ")
	evidence={}
	m={}
	sum_product(evidence,root,[5,1])

	print('P(X5=1 | X1=1)=', end=" ")
	evidence={1:1}
	m={}
	sum_product(evidence,root,[5,1])

	print('P(X5=1 | X1=1, X10=1)=', end=" ")
	evidence={1:1, 10:1}
	m={}
	sum_product(evidence,root,[5,1])

	print('P(X5=1 | X1=1, X10=1, X15=0)=', end=" ")
	evidence={1:1, 10:1,15:0}
	m={}
	sum_product(evidence,root,[5,1])
	print('-------------------------------------')

	
	print("")
	print('-------------------------------------')
	print('SMALL TREE')
	print('-------------------------------------')
	# creating a tree with 4 layers and 15 nodes
	dg=trees(4,15)
	print('P(X8=1)=', end=" ")
	evidence={}
	m={}
	sum_product(evidence,root,[8,1])

	print('P(X8=1 | X12=1)=', end=" ")
	evidence={12:1}
	m={}
	sum_product(evidence,root,[8,1])
	
	print('P(X8=1 | X12=1, X7=1)=', end=" ")
	evidence={12:1, 7:1}
	m={}
	sum_product(evidence,root,[8,1])
	
	print('P(X8=1 | X12=1, X7=1, X15=0)=', end=" ")
	evidence={12:1, 7:1, 15:0}
	m={}
	sum_product(evidence,root,[8,1])
	
	
	print("")
	print('-------------------------------------')
	print('LARGE TREE')
	print('-------------------------------------')
	# Creating a tree with 6 layers and 63 nodes
	dg=trees(6,63)
	evidence={}
	print('P(X32=1)=', end=" ")
	m={}
	sum_product(evidence,root,[32,1])
	
	print('P(X32=1 | X45=1)=', end=" ")
	evidence={45:1}
	m={}
	sum_product(evidence,root,[32,1])
	
	print('P(X32=1 | X45=1, X31=1)=', end=" ")
	evidence={45:1,31:1}
	m={}
	sum_product(evidence,root,[32,1])
	
	print('P(X32=1 | X45=1, X31=1, X63=0)=', end=" ")
	evidence={45:1,31:1, 63:0}
	m={}
	sum_product(evidence,root,[32,1])