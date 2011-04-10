#!/usr/bin/python
# -*- coding: utf-8 -*-
from parse_tree import parse_tree, Special

def canon_len(lst):
	length = 0
	for item in lst:
		if isinstance(item, int):
			length += item
		else:
			length += 1
	return length

def flatten(tree):
	if isinstance(tree, int):
		return tree
	return sum(flatten(item) for item in tree)

def singleton(f):
	return f()

@singleton
class SpecialMethod(object):
	def apply(self, node):
		return self.__class__.__dict__[node.name](self, node)

	def head(self, node):
		s = node.args[0]
		if s and isinstance(s, list):
			if isinstance(s[0], list):
				return s[0]
			else:
				return 1
		return s

	def tail(self, node):
		s = node.args[0]
		if isinstance(s, list):
			if s and isinstance(s[0], int) and s[0] > 1:
				return [s[0]-1] + s[1:]
			return s[1:]
		return 1

	def length(self, node):
		s = node.args[0]
		if isinstance(s, list) and canon_len(s):
			return [canon_len(s)]
		return []

	def test(self, node):
		s = node.args[0]
		if isinstance(s, list):
			return s and 1 or []
		return 1

	def concat(self, node):
		s = node.args[0]
		b = node.args[1]
		if b == 1:
			return s
		if b and s == 1 and isinstance(b[0], int):
			b[0] += 1
		else:
			b.insert(0, s)
		return b

	def flatten(self, node):
		return [flatten(node.args[0])]
	
	def subst(self, node):
		s = node.args[0]
		t = node.stack
		while True:
			if not s:
				if isinstance(t[0], int):
					return 1
				return t[0]
			if isinstance(s[0], int):
				j = s[0]
				for i in t:
					j -= i if isinstance(i, int) else 1
					if j < 0:
						t = i if isinstance(i, list) else 1
						break
				s = s[1:]
				if not s:
					return eval_tree(t)
			else:
				s = s[0]
				t = t[0]

def eval_tree(node):
	if isinstance(node, Special):
		node.args = eval_tree(node.args)
		return SpecialMethod.apply(node)
	elif isinstance(node, list):
		return [eval_tree(item) for item in node]
	return node

if __name__ == '__main__':
	import sys
	print(str(eval_tree(parse_tree(sys.stdin.read()))))
