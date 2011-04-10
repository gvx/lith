#!/usr/bin/python
# -*- coding: utf-8 -*-

class ParseError(Exception):
	pass

class Special(object):
	def __init__(self, name, stack, args=None):
		self.name = name
		self.stack = stack
		self.args = args or []
	def append(self, item):
		self.args.append(item)
		self.stack[-2].append(self.stack.pop())
		self.stack = self.stack[-1]
	def __getitem__(self, _):
		pass
	def __str__(self):
		return self.name + '(' + ', '.join(str(x) for x in self.args) + ')'
	def __repr__(self):
		return str(self)

class Func(list):
	def __repr__(self):
		return 'func'+list.__repr__(self)

special = {'!': 'head', '$': 'tail', '&': 'length', '?': 'test', ':': 'concat', '_': 'flatten', '@': 'subst'}

def parse_tree(text):
	stack = [[]]
	comment = False
	acc = []
	string = False
	for ch in text:
		if comment:
			comment = ch != '\n'
			continue
		if ch == '"':
			if string:
				stack[-1].append(acc)
				acc = []
			string = not string
			continue
		if string:
			acc.append([ord(ch)])
			continue
		if ch.isdigit():
			acc.append(ch)
			continue
		if acc:
			num = int(''.join(acc))
			stack[-1].append(num and [num] or [])
			acc = []
		if ch == 'T': #true
			if stack[-1] and isinstance(stack[-1][-1], int):
				stack[-1][-1] += 1
			else:
				stack[-1].append(1)
		elif ch == '[': #one level deeper
			stack.append([])
		elif ch == '(': #one function deeper
			stack.append(Func())
		elif ch in '])': #go back one level
			if len(stack) > 1:
				stack[-2].append(stack.pop())
			else:
				raise ParseError('Too many closing brackets')
		elif ch == '#':
			comment = True
		elif ch == ':':
			if isinstance(stack[-1], Special):
				raise ParseError('Concatenation character ":" cannot be preceded by another special character')
			if not stack[-1]:
				raise ParseError('Concatenation character ":" must be preceded by an expression')
			p = stack[-1].pop()
			if isinstance(p, int) and p > 1:
				stack[-1].append(p - 1)
				p = 1
			stack.append(Special(special[ch], stack, [p]))
		elif ch in special:
			stack.append(Special(special[ch], stack))
		elif ch not in ' \t\n\r,;|':
			raise ParseError('Unrecognized character ' + ch)
	if len(stack) > 1:
		raise ParseError('Not enough closing brackets')
	return stack[0]

if __name__ == '__main__':
	import sys
	print(str(parse_tree(sys.stdin.read())))
