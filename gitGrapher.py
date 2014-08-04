import sys
import argparse
import git
import networkx
import matplotlib.pyplot as plt

def add_commit(commit):
    graph.add_node(commit, {
        'parents': len(commit.parents)
    })

def add_commit_with_parents(commit):
    add_commit(commit)
    for parent_commit in commit.parents:
        add_commit_with_parents(parent_commit)
        # Add an edge between a commit and its parent commit
        graph.add_edge(commit, parent_commit)

def get_commits_with_n_parents(n_parents):
    nodes = []
    for node in graph.nodes_iter():
        if graph.node[node]['parents'] == n_parents:
            nodes.append(node)
    return nodes

# Set up a repo with the passed in path
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', metavar='P', help='A path to a directory which contains a Git repo')

args = parser.parse_args()

repo = git.Repo(args.path)

graph = networkx.DiGraph()

# Get all the branch head commits
heads = repo.heads

# Add all the commits to the graph
for head in heads:
    add_commit_with_parents(head.commit)

pos = networkx.graphviz_layout(graph, prog='neato')

# Draw only initial commits
networkx.draw_networkx_nodes(graph, pos, nodelist=get_commits_with_n_parents(0),  node_color='c')

# Draw only normal commits
networkx.draw_networkx_nodes(graph, pos, nodelist=get_commits_with_n_parents(1), node_color='g')

# Draw only merge commits
networkx.draw_networkx_nodes(graph, pos, nodelist=get_commits_with_n_parents(2), node_color='r')

networkx.draw_networkx_edges(graph, pos)

plt.show()
