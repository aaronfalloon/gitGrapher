import sys
import argparse
import git
import networkx
import matplotlib
import matplotlib.pyplot as plt
import math
import matplotlib.transforms

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

fig = plt.figure()
ax = fig.add_subplot(111)
plt.subplot(111)

repo = git.Repo(args.path)

graph = networkx.DiGraph()

# Get all the branch head commits
heads = repo.heads

# Add all the commits to the graph
for head in heads:
    add_commit_with_parents(head.commit)

pos = networkx.graphviz_layout(graph, prog='neato')

# Draw only initial commits
initial_commit_positions = networkx.draw_networkx_nodes(graph, pos, nodelist=get_commits_with_n_parents(0),  node_color='c', node_size=800)

# Draw only normal commits
normal_commit_positions = networkx.draw_networkx_nodes(graph, pos, nodelist=get_commits_with_n_parents(1), node_color='g', node_size=800)

# Draw only merge commits
merge_commit_positions = networkx.draw_networkx_nodes(graph, pos, nodelist=get_commits_with_n_parents(2), node_color='r', node_size=800)

networkx.draw_networkx_edges(graph, pos)

# Group the branch names by commit
refs = {}
for head in heads:
    if head.commit not in refs:
        refs[head.commit] = []
        refs[head.commit].append(head)
    elif head.commit in refs:
        refs[head.commit].append(head)

# Annotate with branch names
annotation_positions = {}
for ref_commit in refs:
    # Position each annotation around a circle
    circle = matplotlib.patches.Circle(xy=pos[ref_commit], radius=80)
    circle_verts = circle.get_verts()

    bbox_props = dict(boxstyle='round, pad=0.2', fc='yellow', alpha=0.5)
    arrow_props = dict(arrowstyle='-|>', connectionstyle='arc3, rad=0.2', color='#333333')

    for index, ref in enumerate(refs[ref_commit]):
        # Work out the position around the circle
        circle_pos = math.floor(len(circle_verts) / (index + 1)) - 1

        annotation_positions[ref] = circle_verts[circle_pos]

        plt.annotate(ref, xy=pos[ref_commit], xytext=circle_verts[circle_pos], bbox=bbox_props, arrowprops=arrow_props)

# Add the HEAD to the graph
head_position = annotation_positions[repo.head.reference]

plt.annotate("HEAD", xy=(head_position[0], head_position[1]), xytext=(20, -10), bbox=dict(boxstyle='round, pad=0.2', fc='#eeeeee', alpha=0.7), textcoords='offset points')

# The axis mean nothing
plt.axis('off')

plt.show()
