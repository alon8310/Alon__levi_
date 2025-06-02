# Installation:
(Assuming you have pip, otherwise use [pip](https://pip.pypa.io/en/stable/))

To install the required python packages use 
```bash
pip install -r requirements.txt
```
# Question 1:
We were asked to find all motifs in a graph of size $n$.  
to implement that we divided the process into a few steps:
- we used combinations, permutations from `itertools` to generate all of the combinations for the subgraphs.
- converted all of the lists to DiGraphs from `networkx` since these are connected graphs.
- for each subgraph, we checked if:
1. it is weakly connected.
2. if it's unique since in the question we were asked to only include unique motifs. 
- returned all of the subgraphs that match these criteria.

to run the program, simply run   
```bash
py ./Q1.py <n>
```
on windows or the following for linux
```bash
python3 ./Q1.py <n>
```

# Question 2:
In this question, we were asked to get two things as input:  
1. $n$ the size of the subgraphs to look for.
2. pairs of number representing the edges.

and output all subgraphs of size $n$, count how many instances appear of each motif.

to accomodate the requirements, we wrote the following algorithm:
1.  first, read the edges using stdin and convert it into graphs from `networkx`
2. second, we generate all connected motifs of size `n` using `itertools.permutations` keep only those that are weakly connected and convert them into `networkx` DiGraphs.
3. then, we extract all connected subgraphs of size `n` from the input graph using `itertools.combinatorics`, keep those that are weakly connected.
4.  for each subgraph extracted from the input, we compare it to all motifs using `networkx.DiGraphMatcher` to check isomorphism, if there is a match, increment the counter.
5. return the count of the motifs.

running this question is a bit more comlicated,
first use:
```bash
py ./Q2.py <n>
```
afterwards the user is prompted to enter pairs of numbers to represent edges, at the end use `Control+Z->Enter`.

to use with linux, start with
```bash
python3 ./Q2.py <n>
```
and the end char should be `Control+D->Enter`.