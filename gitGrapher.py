import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path', metavar='P', help='A path to a directory which contains a Git repo')

args = parser.parse_args()


