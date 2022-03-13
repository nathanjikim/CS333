from __future__ import division
import copy
from heapq import nlargest

nodes = []
edges = {}
incoming_edges = {}
prevpagerank = {}
n = 0
outdegree = {}

def create_edge_graph(filename):
    with open(filename, 'r') as f:
        for line in f:
            split = line.split(" ")
            firstnum = int(split[0])
            secondnum = int(split[1])
            if(firstnum not in edges):
                edges[firstnum] = list()
            edges[firstnum].append(secondnum)
            if(firstnum not in outdegree):
                outdegree[firstnum] = 0
            outdegree[firstnum] += 1
            if(secondnum not in incoming_edges):
                incoming_edges[secondnum] = 0
            incoming_edges[secondnum] = incoming_edges[secondnum] + 1

def create_node_map(filename):
    with open(filename, 'r') as f:
        for line in f:
            nodes.append(line.strip())

def initialize_pagerank():
    global n
    n = len(nodes)
    for node_index in range(len(nodes)):
        prevpagerank[node_index] = 1 / n

def total_var_distance(d1, d2):
    global n
    sum = 0
    for node in d1:
        sum += abs(d2[node] - d1[node])
    return sum / 2

def iterate():
    global n
    global prevpagerank
    for i in range(100):
        newpagerank = {}
        for node_index in range(len(nodes)):
            past_rank = prevpagerank[node_index]
            # print(prevpagerank[node_index])
            # has edges
            if node_index in edges:
                outgoing_nodes = edges[node_index]
                for node in outgoing_nodes:
                    if node not in newpagerank:
                        newpagerank[node] = 0
                    newpagerank[node] += past_rank * (0.85 / len(outgoing_nodes) + 0.15 / n)
                # random walk
                for node in range(len(nodes)):
                    if node not in outgoing_nodes:
                        if node not in newpagerank:
                            newpagerank[node] = 0
                        newpagerank[node] += past_rank * 0.15 / n
            # has no edges
            else:
                for node in range(len(nodes)):
                    if node not in newpagerank:
                        newpagerank[node] = 0
                    newpagerank[node] += past_rank * 1 / n
            # print(prevpagerank[node_index])
        if(total_var_distance(prevpagerank, newpagerank) < 0.0001):
            print(i)
            return newpagerank
        prevpagerank = copy.deepcopy(newpagerank)
    return prevpagerank

def searchengine(searchquery, nodefile, edgefile):
    searchresults = []
    indextracker = 0
    with open(nodefile, 'r') as f:
        for line in f:
            if str(searchquery) in line:
                global output
                if output.get(indextracker) is not None:
                    searchresults.append([output.get(indextracker), line.strip()])
            indextracker += 1
        sortedsearchresults = sorted(searchresults, reverse = True)
        top5 = sortedsearchresults[:5]
        return top5


create_edge_graph('test_edges.txt')
create_node_map('test_nodes.txt')

initialize_pagerank()
output = iterate()



five_highest = nlargest(5, output, key=output.get)
for val in five_highest:
    print(f'{nodes[val]}: {output.get(val)}')
    # print(incoming_edges[val])


#Tests searchengine function on test_nodes.txt and test_edges.txt files. Works properly as intended
practice_results = searchengine("B", 'test_nodes.txt', 'test_edges.txt')
print(practice_results)

#Recreates the edge graph and node map for finding the results for quantum and neutrino from the papers.txt and cite.txt files.
create_edge_graph('cite.txt')
create_node_map('papers.txt')

initialize_pagerank()
output = iterate()

test_results = searchengine("quantum", 'papers.txt', 'cite.txt')
print(test_results)
answerforC = searchengine("neutrino", 'papers.txt', 'cite.txt')
print(answerforC)


