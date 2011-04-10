#!/usr/bin/python
# -*- coding: utf-8 -*-
from eval_tree import eval_tree, parse_tree

def write_tree(node):
	if isinstance(node, list):
		return ''.join(['['] + [write_tree(item) for item in node] + [']'])
	return 'T' * node

if __name__ == '__main__':
	import sys
	print(''.join(write_tree(item) for item in eval_tree(parse_tree(sys.stdin.read()))))
