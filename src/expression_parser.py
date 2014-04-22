import re

class Stack(object):
	def __init__(self):
		self.data_set = []
		
	def __call__(self):
		return self.data_set

	def push(self, data):
		self.data_set.append(data)

	def pop(self):
		return self.data_set.pop()

	def peek(self):
		if self.data_set:
			return self.data_set[len(self.data_set)-1]

	def size(self):
		return len(self.data_set)

	def get_data(self):
		return self.data_set

	def clean_data(self):
		self.data_set = []

parser = re.compile('(\d+\.\d+[eE][-+]?\d+|\d+\.\d+|[0-9]\d*|0[0-7]+|0x[0-9a-fA-F]+|[a-zA-Z_]\w*|>>|<<|::|->|\.|\+=|\-=|\*=|/=|%=|>=|<=|==|!=|&&|\|\||\+|\-|\*|/|=|>|<|!|^|%|~|\?|:|,|;|\(|\)|\[|\]|\{|\}|\'|\")')
priorities = {"(": 0, ")": 0, "*": 5, "/": 5, "%": 5, "+": 1, "-": 1}
comparison_operators = ["<", ">", "=", ">=", "<=", "!="]

def parse_expression(expression):
	elements = parser.findall(expression)
	return elements

def post_expression(elements):
	expression_parts = []
	post_elements = Stack()
	sign_stack = Stack()
	for e in elements:
		if priorities.has_key(e):
			if e == "(":
				sign_stack.push("(")
			elif e == ")":
				while sign_stack.peek() != "(":
					post_elements.push(sign_stack.pop())
				sign_stack.pop()
			else:
				s = 0
				while s == 0:
					if sign_stack.size() == 0 or priorities[e] > priorities[sign_stack.peek()]:
						sign_stack.push(e)
						s = 1
					else:
						post_elements.push(sign_stack.pop())
		elif e in comparison_operators:
			while sign_stack.size() != 0:
				post_elements.push(sign_stack.pop())
			sign_stack.clean_data()
			expression_parts.append(post_elements.get_data())
			post_elements.clean_data()
			expression_parts.append(e)
		else:
			post_elements.push(e)
	while sign_stack.size() != 0:
		post_elements.push(sign_stack.pop())
	expression_parts.append(post_elements.get_data())
	post_elements.clean_data()
	return expression_parts

def cal_expression(exp_list):
	new_list = []
	p = 0
	s = 0
	while p < len(exp_list):
		if s == 0 and len(exp_list) >=3 and priorities.has_key(exp_list[p+2]):
			new_list.append(cal_module(exp_list[p], exp_list[p+1], exp_list[p+2]))
			p += 3
			s = 1
		else:
			new_list.append(exp_list[p])
			p += 1
	if len(new_list) > 2:
		return cal_expression(new_list)
	else:
		return new_list[0]
	
def cal_module(f_e, s_e, sign):
	f_e = float(f_e)
	s_e = float(s_e)
	if sign == "+":
		return str(f_e + s_e)
	elif sign == "-":
		return str(f_e - s_e)
	elif sign == "*":
		return str(f_e * s_e)
	elif sign == "/":
		return str(f_e / s_e)
	elif sign == "%":
		return str(f_e % s_e)
	else:
		return None
	
def cal_comparison(expression_parts):
	result = True
	for index, e in enumerate(expression_parts):
		if e in comparison_operators:
			f_p = expression_parts[index-1]
			s_p = expression_parts[index+1]
			f_n = cal_expression(f_p)
			s_n = cal_expression(s_p)
			if result == True:
				result = compare_module(f_n, s_n, e)
	return result
			
def compare_module(f_n, s_n, comparison):
	if comparison == ">":
		return float(f_n) > float(s_n)
	elif comparison == "<":
		return float(f_n) < float(s_n)
	elif comparison == ">=":
		return float(f_n) >= float(s_n)
	elif comparison == "<=":
		return float(f_n) <= float(s_n)
	elif comparison == "=":
		return float(f_n) == float(s_n)
	elif comparison == "!=":
		return float(f_n) != float(s_n)
	else:
		return None

def cal_me(equation):
    elements = parse_expression(equation)
    p_exp = post_expression(elements)
    result = cal_comparision(p_exp)

if __name__ == "__main__":
    ele = parse_expression('1+(2-(3+4))*5<=3+5<9')
    p_exp = post_expression(ele)
    print cal_comparison(p_exp)
	#prfloat calComparison(p_exp)
	#prfloat calExpression(['1', '2', '3', '4', '+', '-', '5', '*', '+'])
