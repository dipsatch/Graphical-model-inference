Exploring Graphical model inference algorithms: Brute Force, Belief Propagation (Sum-Product) & Directed Sampling on 3 kinds of models: Chain, Binary Tree & Grid Graph.


###Brute Force
In the Brute Force algorithm, all permutations of the possible values for all the random variables (nodes) are generated first. The conditional probability, P(Xf | Xe), is calculated by taking the joint probability of P(Xf, Xe) upon P(Xe). The joint probability P(Xr) is calculated by plugging in the permutations with Xr and summing them over. The joint probability formula, along with the related probabilities are different for different models, and they are inside each of the model functions.

_Functions:_
genCombs(n): Generates all the permutations of the possible values (0 & 1) for n random variables, using Recursion.
calcJoint(combs, trgt, model): Calculates the joint probability value for the given model with the trgt using all permutations.
chain(conf): Gives the joint probability of Chain model for a particular permutation conf using the given probability values.
tree(conf): Gives the joint probability of Tree model for a particular permutation conf using the given probability values.
grid(conf): Gives the joint probability of Grid model for a particular permutation conf using the given probability values.
main(): Driver function that gets the permutations & computes the conditional probability P(Xf | Xe) = P(Xf, Xe) / P(Xe).
This algorithm's time complexity is exponential (2^n), where n is the number of nodes & 2 is the number of values for each node. Therefore, it is infeasible to run it on Large Tree & Large Grid, where n = 63 & n = 64, since in that case, this algorithm will try to generate atleast 2^63 = 9223372036854775808 permutations.


###Belief Propagation
Belief Propagation algorithm was implemented for chain graph and trees (both small and large). We have developed a generic program that works for all chain graphs and trees.
We used the networkx library in python to define this model and find the predecessors and successors. X1 is chosen as the root node for the purpose of this algorithm.
  
The algorithm passes messages in two rounds. In the first round, we send messages from the root to the leaf nodes. In the second round, we send messages from the leaf nodes to the root, taking into the account the messages from the first round. We have used nested dictionaries to store these messages.

The code defines the following functions:
Phi: returns potential for two node. Set as 0.95 if the two nodes have the same value (Xi) and 0.05, if different. Phi_node: returns potential (0.95/0.05) if node is 1 else 1.0
Sum_product: drives the algorithm
Collect: Sends messages from leaf nodes to the root
Distribute: Sends messages from root to leaf nodes
Send_message: to compute the value of the message sent from one node to another and store it in a dictionary. Compute_marginal: to get the probability
Chain_graph: to generate the chain with 15 nodes.
Trees: to generate the trees- small tree with 4 layers and 15 nodes, and large tree with 6 layers and 63 nodes.
This algorithm cannot be implemented for grids because a deadlock gets created due to the cycles. This happens since a node can send a message only after it has received the messages from its neighbours. This algorithm, in general, cannot be implemented for any model that has cycles.


###Directed Sampling
In the Directed Sampling method, we first draw and assign a value to the node without any dependencies according to given probability distribution. Subsequently, we visit the nodes in a topological ordering, and assign them values depending on the values assigned to their parent nodes and the corresponding conditional probability table. We draw 10^5 samples in this fashion. Then, to calculate the marginal or conditional probabilities as given, we see how many samples satisfy both the query and evidence, and divide it by either the number of samples satisfying the evidence or total number of samples to find the conditional or marginal probability as required.
Since this algorithm has running time in order of O(S*N), where S are number of samples drawn and N are number of variables/nodes in the graph, it can run for all the given models. However, since it is randomly sampling from the given CPTs, the results are approximate with some margin of error.
Implementation:
The calc_<model> functions are driver functions.
The constructors in respective classes initialize values and sample the value of the root node for all samples. The Sampling() functions in respective classes visit the nodes in topological order, check the state(s) of parent node(s) (indices of which are found according to graph structure, eg for chain it is the previous node), and then draws a sample for the current node according to the CPTs. This process is repeated for all samples.
