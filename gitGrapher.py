import sys
import argparse
import git
import networkx

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', metavar='P', help='A path to a directory which contains a Git repo')

args = parser.parse_args()

repo = git.Repo(args.path)

# Get all the branches
print repo.heads
