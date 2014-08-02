import sys
import argparse
import git
import networkx
import matplotlib.pyplot as plt

# Set up a repo with the passed in path
parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', metavar='P', help='A path to a directory which contains a Git repo')

args = parser.parse_args()

repo = git.Repo(args.path)

graph = networkx.Graph()

# Get all the branches
branches = repo.heads

def add_parent_commits_to_graph(commit):
    try:
        graph.add_node(commit.parents[0])
        graph.add_edge(commit, commit.parents[0])
        add_parent_commits_to_graph(commit.parents[0])
    except:
        pass

# Add all the commits to the graph
for branch in branches:
    graph.add_node(branch.commit)
    add_parent_commits_to_graph(branch.commit)

# Draw the graph
networkx.draw_networkx(graph)

plt.show()
